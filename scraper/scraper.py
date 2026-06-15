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
import requests
from bs4 import BeautifulSoup

# ── Config ─────────────────────────────────────────────────────────────────────
DEALER_PAGES = [
    "https://www.machinerytrader.com/listings/for-sale/underterra/construction-equipment/?DSCompanyID=101734",
    "https://www.machinerytrader.com/listings/for-sale/underterra/construction-equipment/?DSCompanyID=101734&pg=2",
]

# ScraperAPI key (set as GitHub secret SCRAPER_API_KEY)
# Sign up free at https://www.scraperapi.com  — free tier: 1,000 requests/month
SCRAPER_API_KEY = os.environ.get("SCRAPER_API_KEY", "")

INDEX_FILE = "index.html"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

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


def sandhills_img_url(listing_id, index=0):
    """Build a Sandhills CDN image URL for a given listing."""
    return (
        f"https://media.sandhills.com/img.axd"
        f"?id={listing_id}&wid=&w=640&h=480&t=&lp={index}&c=True&wt=False&sz=Max&rt=0"
    )

# ── Scraper ──────────────────────────────────────────────────────────────────────

def fetch_url(url):
    """Fetch a URL, routing through ScraperAPI proxy if key is configured."""
    if SCRAPER_API_KEY:
        proxy_url = (
            f"http://api.scraperapi.com"
            f"?api_key={SCRAPER_API_KEY}"
            f"&url={requests.utils.quote(url, safe='')}"
            f"&render=true"
            f"&country_code=us"
        )
        return requests.get(proxy_url, timeout=120)
    else:
        return requests.get(url, headers=HEADERS, timeout=30)


def scrape_all_listings():
    """Return list of dicts with all current MT listings."""
    listings = []
    for url in DEALER_PAGES:
        try:
            resp = fetch_url(url)
            resp.raise_for_status()
        except Exception as e:
            print(f"  ⚠ Could not fetch {url}: {e}")
            continue

        soup = BeautifulSoup(resp.text, "html.parser")

        # Each listing is anchored by an <h2> containing a link to /listing/for-sale/
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

        time.sleep(1)  # polite delay between pages

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
    """Generate the HTML for a new machine card using Sandhills CDN images."""
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

    # Build image tags (fetch up to 8 images from Sandhills CDN)
    imgs = []
    for i in range(8):
        img_url = sandhills_img_url(lid, i)
        css_class = "carousel-img active" if i == 0 else "carousel-img"
        imgs.append(f'      <img src="{img_url}" class="{css_class}" alt="" loading="lazy" onerror="this.style.display=\'none\'">')

    imgs_html = "\n".join(imgs)
    img_count = len(imgs)

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

    # Insert before closing </div> of catalog-grid
    catalog_close = '</div>\n\n  </section>'
    if catalog_close not in html:
        # fallback: find the grid closing tag
        catalog_close = '  </div>\n\n  </section>'

    # Try a different approach: insert before the last </div> that closes catalog-grid
    # Find the catalog-grid div and insert before its closing tag
    grid_pattern = re.compile(
        r'(<div class="catalog-grid" id="catalog-grid">)(.*?)(</div>\s*\n\s*</section>)',
        re.DOTALL
    )

    def replacer(m):
        return m.group(1) + m.group(2) + new_cards_html + "\n\n  " + m.group(3)

    new_html, count = grid_pattern.subn(replacer, html, count=1)

    if count == 0:
        print("  ⚠ Could not locate catalog-grid in HTML. Aborting.")
        return False

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
