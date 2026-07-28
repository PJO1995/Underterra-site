#!/usr/bin/env python3
"""
Underterra Machine Page Generator
Reads all machine cards from index.html and generates individual HTML pages
in /machines/{stock}.html — clean pages AI can read to generate bills/invoices.

Run standalone:  python3 scraper/generate_pages.py
Called by scraper automatically after adding new machines.
"""

import os
import re
from bs4 import BeautifulSoup

INDEX_FILE  = "index.html"
OUTPUT_DIR  = "machines"
SITE_URL    = "https://underterradelrio.com"
CONTACT     = "ap@underterradelrio.com"
PHONE       = "(830) 488-5594"
COMPANY     = "Underterra LLC"
ADDRESS     = "Del Rio, TX"


def parse_machines(index_path):
    with open(index_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    machines = []
    for card in soup.select(".machine-card"):
        machine_id = card.get("data-machine-id", "")
        stock      = card.get("data-stock", machine_id)
        mtype      = card.get("data-type", "")
        brand      = card.get("data-brand", "")
        mt_url     = card.get("data-mt", "")

        category   = (card.select_one(".machine-category") or card.select_one(".machine-brand") or card.new_tag("x"))
        category   = category.get_text(strip=True)
        name       = (card.select_one(".machine-name") or card.new_tag("x")).get_text(strip=True)

        specs = [s.get_text(strip=True) for s in card.select(".spec") if s.get_text(strip=True)]

        price_el   = card.select_one(".machine-price")
        price      = ""
        if price_el:
            price = price_el.get_text(strip=True).replace("Price", "").strip()

        images = [img["src"] for img in card.select(".carousel-img") if img.get("src")]
        # Make image URLs absolute if they're relative
        images = [
            img if img.startswith("http") else f"{SITE_URL}/{img.lstrip('/')}"
            for img in images
        ]

        machines.append({
            "id":       machine_id,
            "stock":    stock,
            "type":     mtype,
            "brand":    brand,
            "mt_url":   mt_url,
            "category": category,
            "name":     name,
            "specs":    specs,
            "price":    price,
            "images":   images,
        })

    return machines


def generate_page(machine, output_dir):
    stock    = machine["stock"]
    name     = machine["name"]
    category = machine["category"]
    price    = machine["price"]
    specs    = machine["specs"]
    images   = machine["images"]
    mt_url   = machine["mt_url"]
    mtype    = machine["type"]
    brand    = machine["brand"]

    # Build spec rows for the table
    spec_rows = ""
    for spec in specs:
        spec_rows += f"    <tr><td>{spec}</td></tr>\n"

    # Build image list (just URLs, easy for AI to ignore)
    img_tags = ""
    for i, src in enumerate(images[:6]):  # first 6 photos max
        img_tags += f'    <img src="{src}" alt="{name}" style="max-width:100%;margin-bottom:8px;">\n'

    page_url = f"{SITE_URL}/machines/{stock}.html"
    main_url = f"{SITE_URL}/?machine={machine['id']}#catalog"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} — {stock} | {COMPANY}</title>
  <meta name="description" content="{name} for sale. Stock #{stock}. {COMPANY}, {ADDRESS}. {price}.">
  <!-- Machine data for AI/bill generation -->
  <meta name="machine:stock"    content="{stock}">
  <meta name="machine:name"     content="{name}">
  <meta name="machine:category" content="{category}">
  <meta name="machine:type"     content="{mtype}">
  <meta name="machine:brand"    content="{brand}">
  <meta name="machine:price"    content="{price}">
  <meta name="machine:seller"   content="{COMPANY}">
  <meta name="machine:contact"  content="{CONTACT}">
  <meta name="machine:phone"    content="{PHONE}">
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; color: #111; }}
    h1   {{ font-size: 1.8rem; margin-bottom: 4px; }}
    .stock {{ color: #888; font-size: 0.9rem; margin-bottom: 20px; }}
    .price {{ font-size: 1.5rem; font-weight: bold; color: #E8970A; margin: 16px 0; }}
    table  {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
    td     {{ padding: 8px 12px; border-bottom: 1px solid #eee; }}
    tr:nth-child(even) td {{ background: #f9f9f9; }}
    .contact-box {{ background: #f4f4f4; padding: 20px; border-radius: 6px; margin-top: 30px; }}
    .back-link   {{ display: inline-block; margin-bottom: 20px; color: #E8970A; text-decoration: none; }}
    .photos      {{ margin: 20px 0; }}
    .mt-link     {{ color: #555; font-size: 0.85rem; }}
  </style>
</head>
<body>

  <a class="back-link" href="{main_url}">← View on Underterra site</a>

  <!-- MACHINE INFORMATION -->
  <h1>{name}</h1>
  <div class="stock">Stock # {stock} &nbsp;|&nbsp; {category}</div>

  <div class="price">{price}</div>

  <!-- SPECIFICATIONS -->
  <h2>Specifications</h2>
  <table>
    <tr><td><strong>Stock Number</strong></td><td>{stock}</td></tr>
    <tr><td><strong>Equipment Name</strong></td><td>{name}</td></tr>
    <tr><td><strong>Category</strong></td><td>{category}</td></tr>
    <tr><td><strong>Brand</strong></td><td>{brand.upper()}</td></tr>
    <tr><td><strong>Asking Price</strong></td><td>{price}</td></tr>
{spec_rows}  </table>

  <!-- SELLER INFORMATION -->
  <h2>Seller</h2>
  <table>
    <tr><td><strong>Company</strong></td><td>{COMPANY}</td></tr>
    <tr><td><strong>Location</strong></td><td>{ADDRESS}</td></tr>
    <tr><td><strong>Email</strong></td><td>{CONTACT}</td></tr>
    <tr><td><strong>Phone</strong></td><td>{PHONE}</td></tr>
    <tr><td><strong>Website</strong></td><td>{SITE_URL}</td></tr>
    <tr><td><strong>Listing URL</strong></td><td>{page_url}</td></tr>
  </table>

  <!-- PHOTOS -->
  <div class="photos">
    <h2>Photos</h2>
{img_tags}
  </div>

  <!-- CONTACT / REQUEST INFO -->
  <div class="contact-box">
    <h2 style="margin-top:0;">Interested in this machine?</h2>
    <p>Contact us to request a quote, schedule an inspection, or get more information.</p>
    <p><strong>Email:</strong> <a href="mailto:{CONTACT}">{CONTACT}</a></p>
    <p><strong>Phone:</strong> {PHONE}</p>
    <p><a href="{SITE_URL}/#contact">Request a Quote Online →</a></p>
  </div>

  {"<p class='mt-link'>View original listing: <a href='" + mt_url + "' target='_blank'>MachineryTrader</a></p>" if mt_url else ""}

</body>
</html>
"""

    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{stock}.html")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    return filepath


def generate_all(index_path=INDEX_FILE, output_dir=OUTPUT_DIR):
    print(f"📖 Reading machines from {index_path}...")
    machines = parse_machines(index_path)
    print(f"   Found {len(machines)} machines")

    generated = []
    for m in machines:
        if not m["stock"]:
            continue
        path = generate_page(m, output_dir)
        generated.append(path)
        print(f"   ✓ {m['stock']} — {m['name']}")

    print(f"\n✅ Generated {len(generated)} machine pages in /{output_dir}/")
    return generated


def generate_one(machine_data, output_dir=OUTPUT_DIR):
    """Generate a single page — called from scraper.py after adding a new machine."""
    path = generate_page(machine_data, output_dir)
    print(f"   📄 Page generated: {path}")
    return path


if __name__ == "__main__":
    import sys
    index = sys.argv[1] if len(sys.argv) > 1 else INDEX_FILE
    generate_all(index_path=index)
