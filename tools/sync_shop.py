#!/usr/bin/env python3
"""Sync the catalogue with the gallery's Squarespace shop and give every available work a direct checkout link.
For each work: read its product page (price, availability, item id, sku), create a fresh Squarespace cart with the work,
store /checkout?cartToken=... as checkout_url. Run daily (GitHub Action) so the links never go stale."""
import json, re, os, sys, time, urllib.request, http.cookiejar, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); P = os.path.join(ROOT, "data/site.json")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
SITE = "https://www.vivanceart.com"
def session():
    jar = http.cookiejar.CookieJar(); op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar)); op.addheaders = [("User-Agent", UA)]; return op, jar
def crumb(jar): return next((c.value for c in jar if c.name == "crumb"), None)
def product(op, url):
    h = op.open(url, timeout=60).read().decode("utf-8", "replace")
    ld = next((json.loads(m) for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S) if '"Product"' in m), {})
    offers = ld.get("offers"); off = offers if isinstance(offers, dict) else (offers or [{}])[0]
    item = re.search(r'data-item-id="([^"]+)"', h); sku = re.search(r'"sku":"([^"]+)"', h)
    return {"price": off.get("price"), "availability": (off.get("availability") or "").split("/")[-1], "item": item.group(1) if item else None, "sku": sku.group(1) if sku else None, "sold_title": "SOLD" in (ld.get("name") or "").upper()}
def make_cart(op, jar, item, sku, referer):
    c = crumb(jar)
    req = urllib.request.Request(f"{SITE}/api/commerce/shopping-cart/entries?crumb={c}", data=json.dumps({"itemId": item, "sku": sku, "quantity": 1, "additionalFields": "[]"}).encode(),
                                 headers={"Content-Type": "application/json", "X-CSRF-Token": c, "Add-To-Cart-Id": "1", "Referer": referer, "User-Agent": UA}, method="POST")
    d = json.loads(op.open(req, timeout=60).read().decode()); return d.get("shoppingCart", {}).get("cartToken")
D = json.load(open(P, encoding="utf-8")); changed = 0; linked = 0; errors = []
for w in D["works"]:
    try:
        op, jar = session(); info = product(op, w["shop_url"])
        sold = info["availability"] in ("SoldOut", "OutOfStock") or info["sold_title"]
        if info["price"] is not None and float(info["price"]) != float(w.get("price") or 0): w["price"] = float(info["price"]); changed += 1
        if sold != w["sold"]: w["sold"] = sold; changed += 1
        if sold or not info["item"] or not info["sku"]:
            if w.get("checkout_url"): w["checkout_url"] = ""; changed += 1
            continue
        tok = None
        for attempt in range(3):   # a fresh cart every run: the link is never stale; retry on hiccups
            try: tok = make_cart(op, jar, info["item"], info["sku"], w["shop_url"])
            except Exception as e: tok = None
            if tok: break
            time.sleep(2); op, jar = session(); op.open(w["shop_url"], timeout=60).read()
        if tok: w["checkout_url"] = f"{SITE}/checkout?cartToken={tok}"; linked += 1
        elif w.get("checkout_url"): linked += 1   # keep the previous link rather than none
        else: errors.append((w["slug"], "no token"))
        time.sleep(0.6)
    except Exception as e: errors.append((w["slug"], str(e)[:80]))
json.dump(D, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"works {len(D['works'])} | direct checkout links {linked} | price/availability changes {changed} | errors {len(errors)}")
for e in errors[:10]: print("  ERR", e)
sys.exit(1 if linked == 0 else 0)
