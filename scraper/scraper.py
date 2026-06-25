#!/usr/bin/env python3
"""
Underterra Inventory Sync
Scrapes MachineryTrader dealer page and adds new listings to index.html
Run: python3 scraper/scraper.py
"""

import os
import re
import sys
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

# ── Config ─────────────────────────────────────────────────────────────────────
DEALER_BASE_URL = "https://www.machinerytrader.com/listings/search?DSCompanyID=101734"

INDEX_FILE = "index.html"

# ── Helpers ─────────────────────────────────────────────────────────────────────

def get_machine_type(title, category):
    t = (title + " " + category).lower()
    if "excavat" in t:                                  return "excavator"
    if "backhoe" in t:                                  return "backhoe"
    if "wheel loader" in t:                             return "loader"
    if "skid steer" in t or "track skid" in t:         return "skidsteer"
    if "dozer" in t or "bulldozer" in t:               return "dozer"
    if "grader" in t:                                   return "grader"
    if "telehandler" in t or "telescopic" in t:        return "telehandler"
    if "forklift" in t or "lift truck" in t:           return "forklift"
    return "other"


def get_brand(title):
    t = title.lower()
    for brand, keywords in [
        ("cat",      ["caterpillar", " cat "]),
        ("case",     ["case "]),
        ("deere",    ["john deere", " deere"]),
        ("komatsu",  ["komatsu"]),
        ("bobcat",   ["bobcat"]),
        ("jlg",      ["jlg"]),
        ("skytrak",  ["sky trak", "skytrak"]),
        ("toyota",   ["toyota"]),
    ]:
        if any(k in t for k in keywords):
            return brand
    return "other"


def friendly_category(category_raw):
    """Convert MT category string to friendly display name."""
    c = category_raw.lower()
    if "track skid" in c:   return "Track Skid Steer"
    if "wheel skid" in c:   return "Wheel Skid Steer"
    if "skid steer" in c:   return "Skid Steer"
    if "excavat" in c:      return "Excavator"
    if "backhoe" in c:      return "Backhoe Loader"
    if "wheel loader" in c: return "Wheel Loader"
    if "dozer" in c:        return "Dozer"
    if "grader" in c:       return "Motor Grader"
    if "telehandler" in c:  return "Telehandler"
    if "forklift" in c:     return "Forklift"
    return category_raw.strip().title()


def listing_id_from_url(url):
    m = re.search(r'/(\d{8,})', url)
    return m.group(1) if m else ""


def fetch_og_image(listing_url):
    """Fetch the og:image URL from an MT listing detail page using real browser."""
    try:
        html = fetch_page_html(listing_url)
        m = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', html)
        if not m:
            m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']', html)
        if m:
            return m.group(1).replace("&amp;", "&")
    except Exception as e:
        print(f"  ⚠ Could not fetch og:image for {listing_url}: {e}")
    return None

# ── Scraper ──────────────────────────────────────────────────────────────────────

def fetch_page_html(url):
    """Fetch a single page using real Chrome to bypass bot protection."""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"],
        )
        ctx = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 900},
        )
        page = ctx.new_page()
        page.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
        page.goto(url, wait_until="load", timeout=30000)
        page.wait_for_timeout(4000)
        html = page.content()
        browser.close()
        return html


def scrape_all_pages():
    """Fetch all pages of the MT dealer listing."""
    all_html_pages = []
    page_num = 1

    while page_num <= 10:  # safety cap
        if page_num == 1:
            url = DEALER_BASE_URL
        else:
            url = f"{DEALER_BASE_URL}&page={page_num}"

        print(f"  Fetching page {page_num}...")
        try:
            html = fetch_page_html(url)
        except Exception as e:
            print(f"  ⚠ Could not fetch page {page_num}: {e}")
            break

        if "/listing/for-sale/" not in html:
            print(f"  Page {page_num} has no listings — stopping.")
            break

        page_ids = set(re.findall(r'/listing/for-sale/(\d+)/', html))
        if not page_ids:
            print(f"  Page {page_num} returned no listing IDs — stopping.")
            break

        all_html_pages.append((page_num, html))
        print(f"  Page {page_num}: {len(page_ids)} listings found")

        # Always try next page — stop only when it returns no new IDs
        page_num += 1
        time.sleep(1)

    return all_html_pages


def scrape_all_listings():
    """Return list of dicts with all current MT listings across all pages."""
    listings = []
    seen_lids = set()

    try:
        html_pages = scrape_all_pages()
    except Exception as e:
        print(f"  ⚠ Scraping failed: {e}")
        return listings

    for page_num, html in html_pages:
        soup = BeautifulSoup(html, "html.parser")

        # Each listing is anchored by an <h2> containing a link to /listing/for-sale/
        page_count = 0
        for h2 in soup.find_all("h2"):
            a = h2.find("a", href=re.compile(r"/listing/for-sale/"))
            if not a:
                continue

            href = a.get("href", "")
            full_url = "https://www.machinerytrader.com" + href if href.startswith("/") else href
            title = a.get_text(strip=True)
            lid = listing_id_from_url(href)

            # Category: appears in the h2 itself or a sibling span
            category_raw = ""
            span = h2.find("span")
            if span:
                category_raw = span.get_text(strip=True)
            if not category_raw:
                # sometimes it's the text after the link
                category_raw = h2.get_text(strip=True).replace(title, "").strip()

            # Walk up to find the containing block for price/hours
            block = h2
            for _ in range(6):
                block = block.find_parent()
                if block and block.get_text(strip=True):
                    text = block.get_text(" ", strip=True)
                    if "USD" in text or "Hours" in text:
                        break

            text = block.get_text(" ", strip=True) if block else ""

            # Price
            pm = re.search(r'USD\s*\$?([\d,]+)', text)
            price = "$" + pm.group(1) if pm else "Call for Price"

            # Hours
            hm = re.search(r'Hours[:\s]+([\d,]+)', text)
            hours = hm.group(1) if hm else ""

            # Year (first 4-digit year in title)
            ym = re.search(r'\b(19|20)\d{2}\b', title)
            year = ym.group(0) if ym else ""

            # Machine name = title minus year prefix
            name = re.sub(r'^\d{4}\s+', '', title).strip()

            # Skip duplicates (same listing may appear on multiple pages during transition)
            if lid and lid in seen_lids:
                continue
            if lid:
                seen_lids.add(lid)

            listings.append({
                "title":    title,
                "name":     name,
                "year":     year,
                "url":      full_url,
                "lid":      lid,
                "category": friendly_category(category_raw or title),
                "price":    price,
                "hours":    hours,
                "type":     get_machine_type(title, category_raw),
                "brand":    get_brand(title),
            })
            page_count += 1

        print(f"  Page {page_num}: parsed {page_count} unique listings")

    return listings

# ── HTML generation ──────────────────────────────────────────────────────────────

MT_BTN_SVG = (
    '<svg width="10" height="10" viewBox="0 0 10 10" fill="none" '
    'xmlns="http://www.w3.org/2000/svg">'
    '<path d="M5.5 1H9M9 1V4.5M9 1L4 6" stroke="currentColor" stroke-width="1.5" '
    'stroke-linecap="round" stroke-linejoin="round"/>'
    '<path d="M2 2H1.5C1.22 2 1 2.22 1 2.5V8.5C1 8.78 1.22 9 1.5 9H7.5C7.78 9 8 '
    '8.78 8 8.5V8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>'
    '</svg>'
)


def build_machine_card(listing, machine_id, stock_num):
    """Generate the HTML for a new machine card using the real og:image from MT."""
    lid = listing["lid"]
    mt_url = listing["url"]
    brand = listing["brand"]
    mtype = listing["type"]
    category = listing["category"]
    name = listing["name"]
    year = listing["year"]
    price = listing["price"]
    hours = listing["hours"]
    title_full = listing["title"]

    # Fetch real image URL from MT listing detail page
    print(f"  Fetching image for {title_full}...")
    og_img = fetch_og_image(mt_url)

    if og_img:
        imgs_html = f'      <img src="{og_img}" class="carousel-img active" alt="" loading="lazy" onerror="this.style.display=\'none\'">'
        img_count = 1
    else:
        # Fallback: no image
        imgs_html = ''
        img_count = 0

    # Specs
    specs_parts = []
    if year:
        specs_parts.append(f'          <div class="spec"><div class="spec-dot"></div>{year}</div>')
    if hours:
        specs_parts.append(f'          <div class="spec"><div class="spec-dot"></div>{hours} hrs</div>')
    specs_html = "\n".join(specs_parts)

    # Price display
    price_display = price

    card = f"""
    <div class="machine-card" data-machine-id="{machine_id}" data-mt="{mt_url}" data-stock="{stock_num}" data-type="{mtype}" onclick="openDetail(this)" style="cursor:pointer" data-brand="{brand}">
      <div class="machine-img">
{imgs_html}
      <button class="mc-btn mc-btn-prev" onclick="carouselNav(this,-1)">&#10094;</button>
      <button class="mc-btn mc-btn-next" onclick="carouselNav(this,1)">&#10095;</button>
      <div class="carousel-counter"><span class="carousel-cur">1</span> / <span class="carousel-tot">{img_count}</span></div>
      </div>
      <div class="machine-body">
        <div class="machine-category">{category}</div>
        <div class="machine-name">{name}</div>
        <div class="machine-specs">
{specs_html}
        </div>
        <div class="machine-footer">
          <div class="machine-price"><span>Price</span>{price_display}</div>
          <button class="quote-btn" onclick="scrollToContact('{title_full}', '{category}')">Request Info</button>
          <a class="mt-btn" href="#" onclick="var u=this.closest('.machine-card').dataset.mt;if(u){{window.open(u,'_blank');}}event.stopPropagation();return false;" title="Ver en MachineryTrader">{MT_BTN_SVG}MT</a>
        </div>
      </div>
    </div>"""
    return card

# ── Index.html updater ────────────────────────────────────────────────────────────

def update_index(listings):
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    # Find all existing MT listing IDs already in the HTML
    existing_ids = set(re.findall(r'/listing/for-sale/(\d+)/', html))
    print(f"  Existing listings in HTML: {len(existing_ids)}")

    # Find highest existing machine-id number (m01, m02, ...)
    ids_found = re.findall(r'data-machine-id="m(\d+)"', html)
    next_id_num = max((int(x) for x in ids_found), default=0) + 1

    # Find highest existing stock number (UT-001, UT-002, ...)
    stocks_found = re.findall(r'data-stock="UT-(\d+)"', html)
    next_stock_num = max((int(x) for x in stocks_found), default=0) + 1

    # Identify new listings
    new_listings = [l for l in listings if l["lid"] and l["lid"] not in existing_ids]
    print(f"  New listings to add: {len(new_listings)}")

    if not new_listings:
        print("  ✓ No new listings — nothing to update.")
        return False

    # Generate cards for new listings
    new_cards_html = ""
    for listing in new_listings:
        machine_id = f"m{next_id_num:02d}"
        stock_num = f"UT-{next_stock_num:03d}"
        new_cards_html += build_machine_card(listing, machine_id, stock_num)
        next_id_num += 1
        next_stock_num += 1

    # Insert cards before the catalog-grid closing div.
    # The grid closes with:  </div>\n\n  <div class="view-all-wrap">
    # We must NOT match the view-all-wrap's closing div (which comes just before </section>).
    GRID_CLOSE = '  </div>\n\n  <div class="view-all-wrap">'
    if GRID_CLOSE not in html:
        print("  ⚠ Could not locate catalog-grid closing marker. Aborting.")
        return False

    new_html = html.replace(GRID_CLOSE, new_cards_html + "\n\n" + GRID_CLOSE, 1)

    # Update catalog count text
    total = len(existing_ids) + len(new_listings)
    new_html = re.sub(
        r'Showing \d+ of \d+ active listings',
        f'Showing {total} of {total} active listings',
        new_html
    )

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(new_html)

    print(f"  ✓ Added {len(new_listings)} new machine card(s) to {INDEX_FILE}")
    return True


# ── Main ──────────────────────────────────────────────────────────────────────────

def main():
    print("🔍 Scraping MachineryTrader...")
    listings = scrape_all_listings()
    print(f"  Found {len(listings)} total listings on MachineryTrader")

    if not listings:
        print("  ✗ No listings found — check if site structure changed.")
        sys.exit(1)

    print("📝 Updating index.html...")
    changed = update_index(listings)

    if changed:
        print("✅ Done — index.html updated with new machines.")
    else:
        print("✅ Done — inventory already up to date.")


if __name__ == "__main__":
    main()
