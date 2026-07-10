#!/usr/bin/env python3
"""
Mark machines as SOLD in index.html so all visitors (mobile + desktop) see it.

Usage:
  python3 scraper/mark_sold.py m40              # mark m40 as sold
  python3 scraper/mark_sold.py m40 m12 m07      # mark multiple
  python3 scraper/mark_sold.py --list            # show current sold list
  python3 scraper/mark_sold.py --unmark m40      # restore to available

After running, commit and push:
  git add index.html
  git commit -m "Mark [machine] as sold"
  git push
"""

import re
import sys

INDEX_FILE = "index.html"
PATTERN = re.compile(r"(var SOLD_IDS\s*=\s*)\[([^\]]*)\];")


def get_sold_ids(html):
    m = PATTERN.search(html)
    if not m:
        return []
    content = m.group(2).strip()
    if not content:
        return []
    return [x.strip().strip("'\"") for x in content.split(",") if x.strip()]


def set_sold_ids(html, ids):
    unique = list(dict.fromkeys(ids))  # preserve order, remove dupes
    ids_str = ", ".join(f"'{i}'" for i in unique)
    return PATTERN.sub(f"\\g<1>[{ids_str}];", html)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    current = get_sold_ids(html)

    if "--list" in args:
        if current:
            print(f"Currently marked as SOLD: {', '.join(current)}")
        else:
            print("No machines currently marked as SOLD.")
        return

    if "--unmark" in args:
        to_unmark = [a for a in args if a != "--unmark"]
        if not to_unmark:
            print("Specify machine ID(s) to unmark. Example: --unmark m40")
            sys.exit(1)
        new_list = [i for i in current if i not in to_unmark]
        html = set_sold_ids(html, new_list)
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ Unmarked: {', '.join(to_unmark)}")
        print(f"   SOLD_IDS now: {new_list if new_list else '(empty)'}")
        print(f"\n→ Next: git add index.html && git commit -m 'Unmark {' '.join(to_unmark)} as sold' && git push")
        return

    # Default: mark as sold
    to_mark = args
    new_list = current + [i for i in to_mark if i not in current]
    html = set_sold_ids(html, new_list)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Marked as SOLD: {', '.join(to_mark)}")
    print(f"   SOLD_IDS now: {new_list}")
    print(f"\n→ Next: git add index.html && git commit -m 'Mark {' '.join(to_mark)} as sold' && git push")


if __name__ == "__main__":
    main()
