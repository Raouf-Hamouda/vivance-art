#!/usr/bin/env python3
"""VIVANCE ART site generator. Source = data/site.json + this file. Run: python3 gen.py"""
import json, html, os, datetime
ROOT = os.path.dirname(os.path.abspath(__file__)); D = json.load(open(os.path.join(ROOT, "data/site.json"), encoding="utf-8"))
B = D["brand"]; E = html.escape; STAMP = datetime.datetime.now().strftime("%Y%m%d%H%M"); SITE_URL = "https://raouf-hamouda.github.io/vivance-art/"
ART = {a["slug"]: a for a in D["artists"]}; WORKS = sorted(D["works"], key=lambda w: (w["sold"], D["works"].index(w)))   # available first
NAV = [("Artists", "artists.html"), ("Works", "works.html"), ("Exhibitions", "exhibitions.html"), ("Framing", "framing.html"), ("About", "about.html"), ("Contact", "contact.html")]
CART = "https://www.vivanceart.com/cart"
def price(w): return f"€{int(w['price']):,}".replace(",", " ") if w.get("price") else ""
def head(title, desc, rel="", image=None):
    img = SITE_URL + (image or "media/site/og.png")
    return f'''<!doctype html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="Cache-Control" content="no-store">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="website"><meta property="og:site_name" content="Vivance Art">
<meta property="og:image" content="{img}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{img}">
<link rel="icon" href="{rel}media/site/favicon.svg" type="image/svg+xml"><link rel="icon" href="{rel}media/site/favicon-32.png" sizes="32x32" type="image/png"><link rel="icon" href="{rel}media/site/favicon-192.png" sizes="192x192" type="image/png"><link rel="apple-touch-icon" href="{rel}media/site/favicon-180.png"><meta name="theme-color" content="#faf7ee">
<link rel="stylesheet" href="{rel}css/fonts.css?v={STAMP}"><link rel="stylesheet" href="{rel}css/vivance.css?v={STAMP}">
</head>
<body>'''
def nav(current="", rel="", dark=False):
    items = "".join(f'<a class="link" href="{rel}{h}"{" aria-current=page" if h == current else ""}>{E(t)}</a>' for t, h in NAV)
    menu = "".join(f'<a class="item" href="{rel}{h}"{" aria-current=page" if h == current else ""}>{E(t)}<span class="n">{i+1:02d}</span></a>' for i, (t, h) in enumerate(NAV))
    return f'''<nav class="nav{" on-dark" if dark else ""}" data-nav aria-label="Main">
  <a class="brand" href="{rel}index.html" aria-label="Vivance Art, Paris"><img class="logo" src="{rel}media/site/logo.svg" alt="Vivance Art Gallery" width="601" height="185"><small>Paris</small></a>
  <div class="nav-items">{items}<a class="btn btn-ghost shop" href="{rel}shop.html" data-shop-open{" aria-current=page" if current == "shop.html" else ""}>Shop</a></div>
  <button class="burger" aria-expanded="false" aria-controls="menu">Menu</button>
</nav>
<div class="menu" id="menu" data-lenis-prevent>{menu}<a class="item" href="{rel}shop.html" data-shop-open{" aria-current=page" if current == "shop.html" else ""}>Shop<span class="n">07</span></a><div class="foot"><a href="mailto:{B["email"]}">{B["email"]}</a><a href="{B["instagram"]}" target="_blank" rel="noopener">Instagram</a><span>{E(B["address"])}</span></div></div>'''
def footer(rel=""):
    return f'''<footer class="footer"><div class="container">
  <div class="cols">
    <div class="col wide"><p class="title">The gallery</p><p class="body-l measure-l">{E(D["about"]["lead"])}</p></div>
    <div class="col"><p class="title">Gallery</p>{"".join(f'<a class="link" href="{rel}{h}">{E(t)}</a>' for t, h in NAV)}<a class="link" href="{rel}legal.html">Legal</a></div>
    <div class="col"><p class="title">Visit</p><p>{E(B["address"])}</p><a class="link" href="mailto:{B["email"]}">{B["email"]}</a><a class="link" href="{B["instagram"]}" target="_blank" rel="noopener">Instagram</a><a class="link" href="{rel}shop.html">Shop</a></div>
  </div>
  <div class="big" aria-hidden="true"><img src="{rel}media/site/logo.svg" alt="Vivance Art Gallery" width="601" height="185" loading="lazy"></div>
  <div class="legal"><span>© {datetime.date.today().year} Vivance Art · Paris</span><span>Discover Latin American Art</span><a class="link" href="#top">Back to top</a></div>
</div></footer>'''
def shop_panel(rel=""):
    items = [{"t": w["title"], "a": ART.get(w["artist"], {}).get("name", ""), "as": w["artist"], "p": price(w), "sold": w["sold"], "img": rel + (w["images"][0] if w["images"] else ""), "url": rel + f"works/{w['slug']}.html", "buy": w.get("checkout_url") or w["shop_url"], "direct": bool(w.get("checkout_url")), "y": next((v for k, v in w["details"] if k == "Year"), "")} for w in WORKS]
    arts = [{"s": a["slug"], "n": a["name"]} for a in D["artists"] if any(w["artist"] == a["slug"] for w in WORKS)]
    data = json.dumps({"items": items, "artists": arts}, ensure_ascii=False).replace("</", "<\\/")
    return f'''<div class="shop-panel" id="shop" role="dialog" aria-modal="true" aria-label="Shop" data-lenis-prevent hidden>
  <div class="shop-head"><div><p class="caption">Shop · <span data-shop-count></span> works available</p><p class="h2 serif">Original works, secure checkout.</p></div>
    <div class="row"><button class="btn btn-ghost" data-shop-close>Close</button></div></div>
  <div class="shop-filters filters" data-shop-filters></div>
  <div class="shop-grid" data-shop-grid></div>
  <p class="note caption" style="text-transform:none;letter-spacing:0;padding:var(--s-6) 0 0">Buy now goes straight to our secure checkout with the work. Unique pieces are delivered personally. <a class="ul" href="{rel}framing.html">Framing and mounting</a> on request.</p>
</div>
<script id="shop-data" type="application/json">{data}</script>'''
def scripts(rel=""):
    return shop_panel(rel) + f'<script src="{rel}js/lib/lenis.min.js"></script><script src="{rel}js/lib/gsap.min.js"></script><script src="{rel}js/lib/ScrollTrigger.min.js"></script><script src="{rel}js/site.js?v={STAMP}"></script>\n</body></html>'
def artist_card(a, rel=""):
    n = len([w for w in WORKS if w["artist"] == a["slug"]])
    return f'''<a class="artist-card" href="{rel}artists/{a["slug"]}.html" data-reveal><div class="ph"><img src="{rel}{a["portrait"]}" alt="{E(a["name"])}" loading="lazy"></div><p class="name">{E(a["name"])}</p><p class="place">{E(a["born"])}</p><p class="count">{n} work{"s" if n != 1 else ""}</p></a>'''
def product_card(w, rel=""):
    a = ART.get(w["artist"], {}); img = w["images"][0] if w["images"] else ""; year = next((v for k, v in w["details"] if k == "Year"), "")
    direct = w.get("checkout_url")
    buy = ('<span class="btn is-sold">Sold</span>' if w["sold"] else (f'<a class="btn btn-accent" href="{direct}">Buy now</a>' if direct else f'<a class="btn btn-accent" href="{w["shop_url"]}" target="_blank" rel="noopener">Add to cart ↗</a>')) + f'<a class="btn btn-ghost" href="{rel}works/{w["slug"]}.html">Details</a>'
    return f'''<article class="product" data-artist="{w["artist"]}" data-avail="{"sold" if w["sold"] else "available"}" data-price="{w.get("price") or 0}" data-reveal>
  <a class="frame" href="{rel}works/{w["slug"]}.html"><img src="{rel}{img}" alt="{E(w["title"])}" loading="lazy">{'<span class="pill sold">Sold</span>' if w["sold"] else ""}</a>
  <p class="a">{E(a.get("name",""))}</p><p class="t"><i>{E(w["title"])}</i>{", " + E(year) if year else ""}</p><p class="p{" sold" if w["sold"] else ""}">{"Sold" if w["sold"] else price(w)}</p>
  <div class="buy">{buy}</div></article>'''
def signature(a):
    ws = [w for w in WORKS if w["artist"] == a["slug"]]; ws = sorted(ws, key=lambda w: (w["sold"], -(w.get("price") or 0)))
    return ws[0] if ws else None
def work_card(w, rel="", show_artist=True):
    a = ART.get(w["artist"], {}); img = w["images"][0] if w["images"] else ""
    year = next((v for k, v in w["details"] if k == "Year"), ""); tech = next((v for k, v in w["details"] if k == "Technique"), "")
    return f'''<a class="work" href="{rel}works/{w["slug"]}.html" data-artist="{w["artist"]}" data-avail="{"sold" if w["sold"] else "available"}" data-reveal>
  <div class="frame"><img src="{rel}{img}" alt="{E(w["title"])}, {E(a.get("name",""))}" loading="lazy">{'<span class="pill sold">Sold</span>' if w["sold"] else ""}</div>
  <div class="cap"><div>{f'<p class="artist">{E(a.get("name",""))}</p>' if show_artist else ""}<p class="title"><i>{E(w["title"])}</i>{", " + E(year) if year else ""}</p><p class="meta">{E(tech)}</p></div><span class="price{" sold" if w["sold"] else ""}">{"Sold" if w["sold"] else price(w)}</span></div></a>'''
def contact_form():
    return f'''<form class="form" data-mailto="{B["email"]}" novalidate>
  <div class="field"><label for="f-name">Name</label><input id="f-name" name="name" type="text" required autocomplete="name" placeholder="Your name"></div>
  <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" required autocomplete="email" placeholder="you@example.com"></div>
  <div class="field full"><label for="f-subject">Subject</label><select id="f-subject" name="subject"><option>Acquire a work</option><option>Visit the gallery</option><option>An artist</option><option>Framing and mounting</option><option>Press</option><option>Something else</option></select></div>
  <div class="field full"><label for="f-msg">Message</label><textarea id="f-msg" name="message" placeholder="Tell us about the work, the artist or the project you have in mind."></textarea></div>
  <input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
  <div class="full row between"><span class="caption">Opens your email app, we answer within two days</span><button class="btn btn-ink" type="submit">Send the message</button></div>
</form>'''
# ---------------------------------------------------------------- HOME
def home():
    avail = [w for w in WORKS if not w["sold"]]
    pick = []; seen = set()
    for w in avail:
        if w["artist"] not in seen: pick.append(w); seen.add(w["artist"])
        if len(pick) == 6: break
    rows = "".join(artist_card(a) for a in D["artists"][:8])
    ev = D["events"][0]
    return f'''{head("Vivance Art · Latin American contemporary art gallery, Paris", "Vivance Art is a Paris gallery dedicated to Latin American contemporary art: exhibitions, artists from Colombia, Venezuela and Argentina, and works available to acquire.")}
{nav("index.html", dark=True)}
<main id="top">
<section class="hero"><div class="bg"><img src="{D["hero"]}" alt="" fetchpriority="high"></div>
  <a class="credit" href="works/{D["hero_credit"]["slug"]}.html">{E(D["hero_credit"]["artist"])}, <i>{E(D["hero_credit"]["title"])}</i></a>
  <div class="container stack-l">
    <p class="caption" data-reveal>Contemporary art gallery · Paris 12e</p>
    <h1 class="display-1" data-reveal="0.08">Discover Latin American art.</h1>
    <div class="grid"><p class="body-l span-5" data-reveal="0.16" style="color:rgba(250,247,238,.85)">Painting, sculpture, photography and new media from Colombia, Venezuela and Argentina, shown and sold in Paris.</p>
    <div class="span-7 row" style="justify-content:flex-end;align-self:end" data-reveal="0.24"><a class="btn btn-accent" href="shop.html" data-shop-open>Shop the works</a><a class="btn" style="border-color:rgba(250,247,238,.6);color:var(--paper)" href="artists.html">The artists</a></div></div>
  </div></section>
<section class="section"><div class="container">
  <div class="feature"><div class="img" data-reveal><img src="{ev["image"]}" alt="{E(ev["title"])}" loading="lazy"></div>
  <div class="txt stack" data-reveal="0.1"><p class="caption">Latest exhibition · {E(ev["start"][:4])}</p><h2 class="display-2">{E(ev["title"])}</h2><p class="muted">{E(ev["time"])} · {E(ev["place"])}</p><p>{E(ev["text"])}</p><a class="btn" href="exhibitions.html">All exhibitions</a></div></div>
</div></section>
<section class="section" style="padding-top:0"><div class="container">
  <div class="sec-head"><h2 class="h2">Artists</h2><a class="link body-s" href="artists.html">All {len(D["artists"])} artists</a></div>
  <div class="artist-cards">{rows}</div>
</div></section>
<section class="section" style="background:var(--paper-2)"><div class="container">
  <div class="sec-head"><h2 class="h2">Available works</h2><a class="link body-s" href="works.html">All {len(WORKS)} works</a></div>
  <div class="works">{"".join(work_card(w) for w in pick)}</div>
</div></section>
<section class="section"><div class="container">
  <div class="feature flip"><div class="img" data-reveal><img src="{D["about"]["image"]}" alt="" loading="lazy"></div>
  <div class="txt stack" data-reveal="0.1"><p class="caption">The gallery</p><h2 class="display-2">{E(D["about"]["lead"])}</h2><p>{E(D["about"]["body"][0])}</p><a class="btn" href="about.html">About Vivance</a></div></div>
</div></section>
<section class="section-s" style="border-top:1px solid var(--ink)"><div class="container grid">
  <div class="span-5 stack" data-reveal><p class="caption">Newsletter</p><h2 class="h1">Be the first to hear about new projects, exhibitions and works.</h2></div>
  <div class="span-6 start-7" data-reveal="0.1"><form class="form" data-mailto="{B["email"]}" data-subject="Newsletter" novalidate style="grid-template-columns:1fr"><div class="field"><label for="n-email">Email</label><input id="n-email" name="email" type="email" required placeholder="you@example.com"></div><div class="row between"><span class="caption">Opens your email app</span><button class="btn btn-ink" type="submit">Subscribe</button></div></form></div>
</div></section>
</main>
{footer()}
{scripts()}'''
# ---------------------------------------------------------------- ARTISTS
def artists():
    rows = "".join(artist_card(a) for a in D["artists"])
    return f'''{head("Artists · Vivance Art", "The artists represented by Vivance Art in Paris.")}
{nav("artists.html")}
<main id="top">
<section class="page-hero"><div class="container stack"><p class="caption" data-reveal>Artists · {len(D["artists"])}</p><h1 class="display-2" data-reveal="0.08">Painters, sculptors, photographers and new-media artists from Latin America.</h1></div></section>
<section class="section" style="padding-top:0"><div class="container artist-cards">{rows}</div></section>
</main>
{footer()}
{scripts()}'''
def artist(a):
    rel = "../"; ws = [w for w in WORKS if w["artist"] == a["slug"]]; sig = signature(a)
    idx = [x["slug"] for x in D["artists"]].index(a["slug"]); prev = D["artists"][idx - 1]; nxt = D["artists"][(idx + 1) % len(D["artists"])]
    bio = a["bio"]; lead = bio[0] if bio else ""; rest = "".join(f"<p>{E(p)}</p>" for p in bio[1:])
    links = (f'<a class="btn btn-ghost" href="{a["website"]}" target="_blank" rel="noopener">Website ↗</a>' if a["website"] else "") + (f'<a class="btn btn-ghost" href="{a["instagram"]}" target="_blank" rel="noopener">Instagram ↗</a>' if a["instagram"] else "")
    avail = [w for w in ws if not w["sold"]]; sold = [w for w in ws if w["sold"]]
    seen = {}; 
    for w in ws:
        for k, v in w["details"]:
            if k == "Technique":
                key = v.lower().replace("3d ", "").replace("plexiglas ", "plexiglass ").replace("plexiglas", "plexiglass").strip()
                if key not in seen: seen[key] = v[0].upper() + v[1:]
    disciplines = list(seen.values())[:3]
    sig_html = (f'''<a class="signature" href="{rel}works/{sig["slug"]}.html" data-reveal="0.1"><img src="{rel}{sig["images"][0]}" alt="{E(sig["title"])}"><figcaption><span><i>{E(sig["title"])}</i>{", " + next((v for k, v in sig["details"] if k == "Year"), "") if next((v for k, v in sig["details"] if k == "Year"), "") else ""}</span><span>{"Sold" if sig["sold"] else price(sig)} →</span></figcaption></a>''' if sig and sig["images"] else "")
    return f'''{head(f'{a["name"]} · Vivance Art', (lead or a["name"])[:160], rel, sig["images"][0] if sig and sig["images"] else a["portrait"])}
{nav("artists.html", rel)}
<main id="top">
<section class="artist-hero"><div class="container">
  <p class="caption" data-reveal><a class="link" href="{rel}artists.html">Artists</a> · {idx+1:02d} / {len(D["artists"]):02d}</p>
  <h1 class="display-1" data-reveal="0.05">{E(a["name"])}</h1>
  <div class="artist-facts" data-reveal="0.1"><div><span class="caption">Born</span><p>{E(a["born"])}</p></div>{f'<div><span class="caption">Lives and works</span><p>{E(a["lives"])}</p></div>' if a["lives"] else ""}<div><span class="caption">Practice</span><p>{E(", ".join(disciplines)) if disciplines else "Contemporary art"}</p></div><div><span class="caption">With Vivance</span><p>{len(ws)} work{"s" if len(ws) != 1 else ""}{f", {len(avail)} available" if ws else ""}</p></div></div>
  {sig_html}
</div></section>
<section class="section"><div class="container artist-body">
  <figure class="portrait" data-reveal><img src="{rel}{a["portrait"]}" alt="{E(a["name"])}"><figcaption class="caption">{E(a["name"])}, {E(a["born"].split(",")[-1].strip()) if a["born"] else ""}</figcaption></figure>
  <div class="bio" data-reveal="0.1"><p class="lead serif">{E(lead)}</p>{rest}<div class="links">{links}<a class="btn btn-ink" href="mailto:{B["email"]}?subject={E(a["name"])}">Inquire about {E(a["name"].split()[0])}</a></div></div>
</div></section>
{"<section class='section' style='padding-top:0'><div class='container'><div class='sec-head'><h2 class='h2'>Works</h2><span class='body-s muted'>" + (f"{len(avail)} available · {len(sold)} sold" if sold else f"{len(avail)} available") + "</span></div><div class='works'>" + "".join(work_card(w, rel, False) for w in ws) + "</div></div></section>" if ws else ""}
<section class="section-s" style="border-top:1px solid var(--ink)"><div class="container artist-nav">
  <a class="prevnext" href="{rel}artists/{prev["slug"]}.html"><span class="caption">Previous artist</span><span class="h2 serif">{E(prev["name"])}</span></a>
  <a class="prevnext right" href="{rel}artists/{nxt["slug"]}.html"><span class="caption">Next artist</span><span class="h2 serif">{E(nxt["name"])}</span></a>
</div></section>
</main>
{footer(rel)}
{scripts(rel)}'''
# ---------------------------------------------------------------- WORKS
def works():
    tabs = '<button class="tab" data-f="artist" data-v="all" aria-selected="true">All artists</button>' + "".join(f'<button class="tab" data-f="artist" data-v="{a["slug"]}" aria-selected="false">{E(a["name"])}</button>' for a in D["artists"] if any(w["artist"] == a["slug"] for w in WORKS))
    tabs += '<span class="sep"></span><button class="tab" data-f="avail" data-v="all" aria-selected="true">All</button><button class="tab" data-f="avail" data-v="available" aria-selected="false">Available</button>'
    return f'''{head("Works · Vivance Art", "All works available at Vivance Art: painting, sculpture, photography from Latin American artists.")}
{nav("works.html")}
<main id="top">
<section class="page-hero"><div class="container stack"><p class="caption" data-reveal>Works · {len(WORKS)} · {len([w for w in WORKS if not w["sold"]])} available</p><h1 class="display-2" data-reveal="0.08">Every work is unique.</h1><p class="muted measure-l" data-reveal="0.12">Prices are those of our online shop. Acquisition is completed there, with secure checkout, or directly with the gallery.</p><div class="filters" data-reveal="0.16">{tabs}</div></div></section>
<section class="section" style="padding-top:0"><div class="container"><div class="works four" id="works">{"".join(work_card(w) for w in WORKS)}</div><p class="muted body-s" id="empty" hidden style="padding:var(--s-7) 0">No work matches this selection.</p></div></section>
</main>
{footer()}
{scripts()}'''
def work(w):
    rel = "../"; a = ART.get(w["artist"], {}); others = [x for x in WORKS if x["artist"] == w["artist"] and x["slug"] != w["slug"]][:4]
    gal = "".join(f'<figure><img src="{rel}{im}" alt="{E(w["title"])}" {"" if i == 0 else "loading=lazy"}></figure>' for i, im in enumerate(w["images"]))
    dl = "".join(f"<dt>{E(k)}</dt><dd>{E(v)}</dd>" for k, v in w["details"])
    year = next((v for k, v in w["details"] if k == "Year"), "")
    direct = w.get("checkout_url")
    acquire = ('<span class="btn is-sold">Sold</span>' if w["sold"] else
               (f'<a class="btn btn-accent" href="{direct}">Buy now · {price(w)}</a>' if direct else
                f'<a class="btn btn-accent" href="{w["shop_url"]}" target="_blank" rel="noopener">Add to cart · {price(w)} ↗</a>'))
    return f'''{head(f'{w["title"]} · {a.get("name","")} · Vivance Art', f'{w["title"]} by {a.get("name","")}' + (f', {year}' if year else '') + (f'. {price(w)}.' if w.get("price") and not w["sold"] else ''), rel, w["images"][0] if w["images"] else None)}
{nav("works.html", rel)}
<main id="top">
<section class="section" style="padding-top:calc(var(--nav-h) + var(--s-7))"><div class="container work-page">
  <div class="gallery" data-reveal>{gal}</div>
  <aside class="details stack-l" data-reveal="0.1">
    <div class="stack"><p class="caption"><a class="link" href="{rel}artists/{a.get("slug","")}.html">{E(a.get("name",""))}</a></p><h1 class="h1 serif"><i>{E(w["title"])}</i>{", " + E(year) if year else ""}</h1></div>
    <dl>{dl}</dl>
    <p class="price">{"Sold" if w["sold"] else price(w)}</p>
    <div class="actions">{acquire}<a class="btn" href="mailto:{B["email"]}?subject={E(w["title"])} · {E(a.get("name",""))}">Inquire</a>
      <p class="note">Buy now takes you straight to our secure checkout with this work. Unique pieces are delivered personally. Unique pieces: delivery is arranged personally with the buyer. <a class="ul" href="{rel}framing.html">Framing and mounting</a> on request.</p></div>
  </aside>
</div></section>
{"<section class='section' style='padding-top:0'><div class='container'><div class='sec-head'><h2 class='h2'>More by " + E(a.get("name","")) + "</h2><a class='link body-s' href='" + rel + "artists/" + a.get("slug","") + ".html'>Artist page</a></div><div class='works four'>" + "".join(work_card(x, rel, False) for x in others) + "</div></div></section>" if others else ""}
</main>
{footer(rel)}
{scripts(rel)}'''
def shop():
    tabs = '<button class="tab" data-f="artist" data-v="all" aria-selected="true">All artists</button>' + "".join(f'<button class="tab" data-f="artist" data-v="{a["slug"]}" aria-selected="false">{E(a["name"])}</button>' for a in D["artists"] if any(w["artist"] == a["slug"] for w in WORKS))
    tabs += '<span class="sep"></span><button class="tab" data-f="avail" data-v="all" aria-selected="true">All</button><button class="tab" data-f="avail" data-v="available" aria-selected="false">Available</button>'
    avail = [w for w in WORKS if not w["sold"]]
    return f'''{head("Shop · Vivance Art", "Acquire original works by Latin American artists: painting, sculpture, photography. Secure checkout.")}
{nav("shop.html")}
<main id="top">
<section class="page-hero"><div class="container stack"><p class="caption" data-reveal>Shop · {len(avail)} works available</p><h1 class="display-2" data-reveal="0.08">Original works, acquired in a few clicks.</h1><p class="muted measure-l" data-reveal="0.12">Buy now takes you straight to our secure checkout with the work. Unique pieces are delivered personally; framing and mounting on request. Questions before buying: <a class="ul" href="contact.html">write to us</a>.</p></div></section>
<section class="section" style="padding-top:0"><div class="container">
  <div class="shop-bar"><div class="filters">{tabs}</div></div>
  <div class="shop-grid" id="works">{"".join(product_card(w) for w in WORKS)}</div><p class="muted body-s" id="empty" hidden style="padding:var(--s-7) 0">No work matches this selection.</p>
</div></section>
</main>
{footer()}
{scripts()}'''
# ---------------------------------------------------------------- EXHIBITIONS / ABOUT / FRAMING / CONTACT / LEGAL / 404
def exhibitions():
    def fmt(d): return datetime.date.fromisoformat(d).strftime("%-d %b %Y")
    items = "".join(f'''<article class="event" data-reveal><div class="date"><b>{datetime.date.fromisoformat(e["start"]).strftime("%d")}</b><span class="caption">{datetime.date.fromisoformat(e["start"]).strftime("%b %Y")}</span></div>
      <div class="txt stack"><p class="caption">{E(e["kind"])}</p><h2 class="h1 serif">{E(e["title"])}</h2><p class="muted body-s">{fmt(e["start"])}{" to " + fmt(e["end"]) if e["end"] != e["start"] else ""} · {E(e["time"])}<br>{E(e["place"])}</p><p class="measure-l">{E(e["text"])}</p></div>
      <div class="img">{f'<img src="{e["image"]}" alt="{E(e["title"])}" loading="lazy">' if e["image"] else ""}</div></article>''' for e in D["events"])
    return f'''{head("Exhibitions · Vivance Art", "Exhibitions, vernissages and events at Vivance Art, Paris.")}
{nav("exhibitions.html")}
<main id="top">
<section class="page-hero"><div class="container stack"><p class="caption" data-reveal>Exhibitions · 2025</p><h1 class="display-2" data-reveal="0.08">Evenings in Paris where Latin American art comes to life.</h1></div></section>
<section class="section" style="padding-top:0"><div class="container events">{items}</div></section>
</main>
{footer()}
{scripts()}'''
def about():
    countries = sorted({a["born"].split(",")[-1].strip() for a in D["artists"] if a["born"]})
    strip = "".join(f'<a class="mini" href="artists/{a["slug"]}.html"><img src="{a["portrait"]}" alt="{E(a["name"])}" loading="lazy"><span>{E(a["name"])}</span></a>' for a in D["artists"])
    pillars = [("01", "Exhibitions", "A programme of exhibitions, vernissages and finissages in Paris that gives Latin American artists a stage in Europe, from the first season in 2025 to the Latin America and Caribbean Weeks."),
               ("02", "Advisory", "Personal, expert advice to collectors, institutions and art enthusiasts, and help with the acquisition of unique, significant works that resonate with their values."),
               ("03", "Representation", "Emerging and established artists from Colombia, Venezuela and Argentina, championed on international stages and connected with new audiences.")]
    pil = "".join(f'<div class="pillar" data-reveal="{i*0.06:.2f}"><span class="caption">{n}</span><h3 class="h2 serif">{E(t)}</h3><p>{E(d)}</p></div>' for i, (n, t, d) in enumerate(pillars))
    facts = [(str(len(D["artists"])), "artists"), (str(len(countries)), "countries of origin"), (str(len(WORKS)), "works in the catalogue"), (str(len(D["events"])), "evenings in 2025")]
    fx = "".join(f'<div data-reveal="{i*0.05:.2f}"><span class="num serif">{v}</span><span class="caption">{E(l)}</span></div>' for i, (v, l) in enumerate(facts))
    return f'''{head("About · Vivance Art", D["about"]["lead"])}
{nav("about.html")}
<main id="top">
<section class="page-hero"><div class="container stack"><p class="caption" data-reveal>The gallery · Paris 12e</p><h1 class="display-2" data-reveal="0.08">{E(D["about"]["lead"])}</h1></div></section>
<section class="section" style="padding-top:0"><div class="container">
  <figure class="wide-figure" data-reveal><img src="{D["about"]["image"]}" alt="Vivance Art" loading="lazy"><figcaption class="caption">Vivance Art, 10 avenue de Corbera, Paris</figcaption></figure>
</div></section>
<section class="section" style="padding-top:0"><div class="container grid">
  <div class="span-5" data-reveal><p class="caption">Mission</p><p class="lead serif" style="margin-top:var(--s-4)">{E(D["about"]["body"][0].split(". ")[0])}.</p></div>
  <div class="span-6 start-7 stack" data-reveal="0.1">{"".join(f"<p>{E(p)}</p>" for p in D["about"]["body"])}</div>
</div></section>
<section class="section" style="background:var(--paper-2)"><div class="container">
  <div class="sec-head"><h2 class="h2">What we do</h2></div>
  <div class="pillars">{pil}</div>
</div></section>
<section class="section"><div class="container">
  <div class="facts">{fx}</div>
</div></section>
<section class="section" style="padding-top:0"><div class="container">
  <div class="sec-head"><h2 class="h2">The artists</h2><a class="link body-s" href="artists.html">All artists</a></div>
  <div class="mini-strip">{strip}</div>
</div></section>
<section class="section-s" style="border-top:1px solid var(--ink)"><div class="container row between">
  <div><p class="caption">Visit</p><p class="h2 serif">{E(B["address"])}</p><p class="muted body-s">By appointment and during exhibitions · Metro Reuilly-Diderot</p></div>
  <div class="row"><a class="btn btn-ink" href="contact.html">Write to us</a><a class="btn" href="exhibitions.html">Exhibitions</a></div>
</div></section>
</main>
{footer()}
{scripts()}'''
def framing():
    fr = D["framing"]; specs = {"Wood frame": ("Light natural wood", "Paper, canvas, photography", "Warm and soft, lets the work breathe"), "UV-protective acrylic frame": ("Acrylic glazing with UV filter", "Photography, works on paper, prints", "Museum-grade protection against light"),
             "Full-bleed mounting": ("No mat, image to the edge", "Photography, bold graphic works", "Clean, contemporary, maximum image"), "Mat mounting": ("5 cm white mat, bevel cut", "Drawings, small formats, prints", "Classic depth and breathing room"), "Float mounting": ("Print raised on a hidden support", "Deckled edges, handmade paper, textiles", "Shows the edges, adds shadow and relief")}
    rows = "".join(f'''<article class="fr-row{" flip" if i % 2 else ""}" id="framing-{i+1}" data-reveal>
      <div class="img">{f'<img src="{c["img"]}" alt="{E(c["t"])}" loading="lazy">' if c["img"] else ""}</div>
      <div class="txt"><span class="caption">{i+1:02d} / {len(fr):02d}</span><h2 class="h1 serif">{E(c["t"])}</h2><p>{E(c["d"])}</p>
        <dl><dt>Material</dt><dd>{E(specs.get(c["t"], ("", "", ""))[0])}</dd><dt>Best for</dt><dd>{E(specs.get(c["t"], ("", "", ""))[1])}</dd><dt>Effect</dt><dd>{E(specs.get(c["t"], ("", "", ""))[2])}</dd></dl></div>
    </article>''' for i, c in enumerate(fr))
    toc = "".join(f'<a class="link" href="#framing-{i+1}">{i+1:02d} {E(c["t"])}</a>' for i, c in enumerate(fr))
    steps = [("Choose the work", "In the shop or with us at the gallery. Every print and work on paper can be framed and mounted to measure."), ("We propose", "Two or three frame and mounting options adapted to the work, the room and your budget, with a quote."), ("Made locally", "Frames come from a family-run, local and sustainable workshop known for the durability of its work."), ("Delivered", "Unique pieces are delivered personally, framed and ready to hang.")]
    st = "".join(f'<div class="step" data-reveal="{i*0.06:.2f}"><span class="num serif">{i+1}</span><h3 class="h3">{E(t)}</h3><p>{E(d)}</p></div>' for i, (t, d) in enumerate(steps))
    return f'''{head("Framing and mounting · Vivance Art", "Framing and mounting options for the works acquired at Vivance Art: wood, UV acrylic, full-bleed, mat and float mounting.")}
{nav("framing.html")}
<main id="top">
<section class="page-hero"><div class="container stack"><p class="caption" data-reveal>Framing and mounting</p><h1 class="display-2" data-reveal="0.08">Every work can be framed and mounted to measure, by a local workshop.</h1><p class="muted measure-l" data-reveal="0.16">Five ways to frame a print or a work on paper. Ask for a quote when you acquire a piece, or write to us for a work you already own.</p><div class="toc" data-reveal="0.2">{toc}</div></div></section>
<section class="section" style="padding-top:0"><div class="container fr-rows">{rows}</div></section>
<section class="section" style="background:var(--paper-2)"><div class="container">
  <div class="sec-head"><h2 class="h2">How it works</h2></div>
  <div class="steps">{st}</div>
</div></section>
<section class="section-s" style="border-top:1px solid var(--ink)"><div class="container row between"><span class="h3 serif">Ask for a framing quote for a work you own or one from the shop.</span><a class="btn btn-accent" href="mailto:{B["email"]}?subject=Framing%20and%20mounting">Ask for a quote</a></div></section>
</main>
{footer()}
{scripts()}'''
def contact():
    return f'''{head("Contact · Vivance Art", "Contact Vivance Art, 10 avenue de Corbera, Paris 12e.")}
{nav("contact.html")}
<main id="top">
<section class="page-hero"><div class="container stack"><p class="caption" data-reveal>Contact</p><h1 class="display-2" data-reveal="0.08">A work, an artist, a visit or a project: write to us.</h1></div></section>
<section class="section" style="padding-top:0"><div class="container grid">
  <div class="span-5" data-reveal><div class="contact-card"><p class="caption">The gallery</p><p class="h2 serif">Vivance Art<br>{E(B["address"])}</p>
    <div class="rows"><div><span>Email</span><a class="ul" href="mailto:{B["email"]}">{B["email"]}</a></div><div><span>Instagram</span><a class="ul" href="{B["instagram"]}" target="_blank" rel="noopener">@vivancearts</a></div><div><span>Visits</span><span>By appointment and during exhibitions</span></div><div><span>Metro</span><span>Reuilly-Diderot, lines 1 and 8</span></div><div><span>Map</span><a class="ul" href="https://maps.google.com/?q={E(B["address"])}" target="_blank" rel="noopener">Open in Maps</a></div></div>
    <a class="btn btn-accent" href="shop.html" data-shop-open>Browse the works</a></div></div>
  <div class="span-6 start-7" data-reveal="0.1">{contact_form()}</div>
</div></section>
</main>
{footer()}
{scripts()}'''
def legal():
    L = D["legal"]
    return f'''{head("Legal · Vivance Art", "Terms of use and shipping policy of Vivance Art.")}
{nav("legal.html")}
<main id="top">
<section class="page-hero"><div class="container stack"><p class="caption">Legal</p><h1 class="display-2">Terms of use and shipping.</h1></div></section>
<section class="section legal-text" style="padding-top:0"><div class="container measure-l"><h3 class="h2">Terms of use</h3>{"".join(f"<p>{E(p)}</p>" for p in L["terms"])}<h3 class="h2">Shipping policy</h3>{"".join(f"<p>{E(p)}</p>" for p in L["shipping"])}</div></section>
</main>
{footer()}
{scripts()}'''
def notfound():
    return f'''{head("Page not found · Vivance Art", "Page not found")}
{nav()}
<main id="top"><section class="page-hero"><div class="container stack"><p class="caption">404</p><h1 class="display-2">This page is not on view.</h1><div class="row"><a class="btn btn-ink" href="index.html">Home</a><a class="btn" href="works.html">Works</a></div></div></section></main>
{footer()}
{scripts()}'''
os.makedirs(os.path.join(ROOT, "artists"), exist_ok=True); os.makedirs(os.path.join(ROOT, "works"), exist_ok=True)
PAGES = {"index.html": home(), "artists.html": artists(), "works.html": works(), "shop.html": shop(), "exhibitions.html": exhibitions(), "about.html": about(), "framing.html": framing(), "contact.html": contact(), "legal.html": legal(), "404.html": notfound()}
for a in D["artists"]: PAGES[f"artists/{a['slug']}.html"] = artist(a)
for w in WORKS: PAGES[f"works/{w['slug']}.html"] = work(w)
for fn, out in PAGES.items(): open(os.path.join(ROOT, fn), "w", encoding="utf-8").write(out)
print(f"{len(PAGES)} pages written")
