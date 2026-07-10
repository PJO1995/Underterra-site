#!/usr/bin/env python3
"""
Backfill multi-photo carousel for existing machine cards.
Visits each listing's MT page, extracts all gallery images,
and updates the machine-img section in index.html.

Usage:  python3 scraper/backfill_photos.py
"""

import re
import sys
from playwright.sync_api import sync_playwright

INDEX_FILE = "index.html"

# Machine IDs to backfill → their MT listing URLs
TARGETS = {
    "m47": "https://www.machinerytrader.com/listing/for-sale/256967305/2022-deere-310sl-loader-backhoes",
    "m48": "https://www.machinerytrader.com/listing/for-sale/256966183/2022-deere-310sl-loader-backhoes",
}


def fetch_all_images(listing_url):
    """Open listing page with real Chrome, click carousel Next, collect all photo URLs."""
    try:
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
            page.goto(listing_url, wait_until="load", timeout=30000)
            page.wait_for_timeout(4000)

            seen_ids = set()
            images = []

            def harvest(html_text):
                """Only keep full-size images (w >= 400) to exclude thumbnail strips."""
                for m in re.finditer(
                    r'(https://[^\s"\'<>]*(?:machinerytrader|sandhills|machinery)[^\s"\'<>]*[?&]id=(\d+)[^\s"\'<>]*)',
                    html_text,
                ):
                    url = m.group(1).replace("&amp;", "&")
                    img_id = m.group(2)
                    w_m = re.search(r'[?&]w=(\d+)', url)
                    if w_m and int(w_m.group(1)) < 400:
                        continue
                    if img_id not in seen_ids:
                        seen_ids.add(img_id)
                        images.append(url)
                for m in re.finditer(
                    r'data-src=["\']([^"\']*(?:machinerytrader|sandhills)[^"\']*)["\']',
                    html_text,
                ):
                    url = m.group(1).replace("&amp;", "&")
                    w_m = re.search(r'[?&]w=(\d+)', url)
                    if w_m and int(w_m.group(1)) < 400:
                        continue
                    img_id_m = re.search(r'id=(\d+)', url)
                    if img_id_m:
                        img_id = img_id_m.group(1)
                        if img_id not in seen_ids:
                            seen_ids.add(img_id)
                            images.append(url)

            initial_html = page.content()
            print(f"    Page HTML length: {len(initial_html)} chars")

            # Debug: print first image-like URL found
            any_img = re.search(r'https://[^\s"\'<>]*(?:jpg|jpeg|png|webp|id=\d)[^\s"\'<>]*', initial_html)
            if any_img:
                print(f"    Sample img URL: {any_img.group(0)[:120]}")
            else:
                print("    ⚠ No image URL patterns detected in initial HTML")

            harvest(initial_html)

            for _ in range(30):
                clicked = False
                for sel in [
                    'button[aria-label*="Next" i]',
                    'button[aria-label*="next" i]',
                    '.slick-next',
                    '[class*="next-photo"]',
                    '[class*="nextPhoto"]',
                    '[class*="photo-next"]',
                    '[class*="PhotoNext"]',
                ]:
                    try:
                        btn = page.query_selector(sel)
                        if btn and btn.is_visible():
                            btn.click()
                            page.wait_for_timeout(600)
                            harvest(page.content())
                            clicked = True
                            break
                    except Exception:
                        pass
                if not clicked:
                    break

            browser.close()
            return images if images else None

    except Exception as e:
        print(f"  ⚠ Error fetching {listing_url}: {e}")
    return None


def build_imgs_html(img_list):
    lines = []
    for i, url in enumerate(img_list):
        cls = "carousel-img active" if i == 0 else "carousel-img"
        lines.append(
            f'      <img src="{url}" class="{cls}" alt="" loading="lazy" onerror="this.style.display=\'none\'">'
        )
    return "\n".join(lines)


def find_div_end(html, div_start):
    """Find the index just after the closing </div> that matches the <div> at div_start.
    Counts nested <div> depth to find the correct closing tag."""
    pos = div_start + len('<div')
    depth = 1
    while pos < len(html) and depth > 0:
        open_pos = html.find('<div', pos)
        close_pos = html.find('</div>', pos)
        if close_pos == -1:
            return -1  # unmatched
        if open_pos != -1 and open_pos < close_pos:
            depth += 1
            pos = open_pos + 4
        else:
            depth -= 1
            pos = close_pos + 6  # len('</div>') == 6
    return pos  # points to character after </div>


def update_card_photos(html, machine_id, img_list):
    """Replace the entire <div class="machine-img">…</div> block for the given machine_id.
    Uses div-depth counting instead of regex to avoid mismatched closing tags."""
    # Find this card
    card_pos = html.find(f'data-machine-id="{machine_id}"')
    if card_pos == -1:
        print(f"  ⚠ Could not find card {machine_id}")
        return html, False

    # Find machine-img div within this card
    img_div_start = html.find('<div class="machine-img">', card_pos)
    if img_div_start == -1:
        print(f"  ⚠ Could not find machine-img for {machine_id}")
        return html, False

    # Find the matching closing </div>
    img_div_end = find_div_end(html, img_div_start)
    if img_div_end == -1:
        print(f"  ⚠ Could not find closing </div> for machine-img in {machine_id}")
        return html, False

    # Build replacement block
    img_count = len(img_list)
    imgs_html = "\n".join(
        f'      <img src="{u}" class="carousel-img{" active" if i == 0 else ""}" '
        f'alt="" loading="lazy" onerror="this.style.display=\'none\'">'
        for i, u in enumerate(img_list)
    )
    new_img_div = (
        f'<div class="machine-img">\n'
        f'{imgs_html}\n'
        f'      <button class="mc-btn mc-btn-prev" onclick="carouselNav(this,-1)">&#10094;</button>\n'
        f'      <button class="mc-btn mc-btn-next" onclick="carouselNav(this,1)">&#10095;</button>\n'
        f'      <div class="carousel-counter">'
        f'<span class="carousel-cur">1</span> / <span class="carousel-tot">{img_count}</span>'
        f'</div>\n'
        f'      </div>'
    )

    new_html = html[:img_div_start] + new_img_div + html[img_div_end:]
    return new_html, True


def main():
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    changed = False
    for machine_id, url in TARGETS.items():
        print(f"\n📷 Fetching photos for {machine_id}: {url}")
        img_list = fetch_all_images(url)
        if not img_list:
            print(f"  ⚠ No images found — skipping {machine_id}")
            continue
        print(f"  → {len(img_list)} photo(s) found")
        html, ok = update_card_photos(html, machine_id, img_list)
        if ok:
            print(f"  ✓ Updated {machine_id} with {len(img_list)} photo(s)")
            changed = True

    if changed:
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            f.write(html)
        print("\n✅ index.html updated. Review locally then git add/commit/push.")
    else:
        print("\n⚠ No changes made.")


if __name__ == "__main__":
    main()
