#!/usr/bin/env python3
"""Build a standalone buyer-facing preview page for one ebook.

Usage:
    python3 tools/build_page.py <book-slug>          # e.g. python3 tools/build_page.py ajbit-063

Reads <book-slug>/spec.json and writes <book-slug>/index.html.
The output page is fully self-contained for that one book: it links to no
other book and exposes no index of the catalogue, so a QR code pointing at
/book-slug/ shows the buyer exactly one product.

spec.json fields:
  slug, title, subtitle, author, series, volume, description,
  excerpt_heading, excerpt (list of paragraphs),
  facts (ordered dict of label -> value),
  buy_links (dict of store name -> URL; empty values render nothing)

cover.png must sit in the same directory as spec.json.
"""
import json
import html
import pathlib
import sys

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title} - {author}</title>
<style>
:root {{
  --navy:#0a1628; --navy2:#0f2038; --cyan:#22d3ee; --cyan-dim:#0e7490;
  --text:#e6edf5; --muted:#8fa3bd; --gold:#d8b45a; --line:#1c3050;
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ background:var(--navy); color:var(--text);
  font-family:Georgia,'Times New Roman',serif; line-height:1.65; }}
.wrap {{ max-width:860px; margin:0 auto; padding:32px 20px 64px; }}
.cover {{ display:block; width:280px; max-width:78%; margin:12px auto 20px;
  border-radius:6px; box-shadow:0 18px 50px rgba(0,0,0,.55); }}
.kicker {{ text-align:center; color:var(--cyan); letter-spacing:.28em;
  text-transform:uppercase; font-size:12px; font-family:Verdana,Arial,sans-serif; }}
h1 {{ text-align:center; font-size:30px; line-height:1.25; margin:10px 0 6px;
  font-weight:normal; }}
.sub {{ text-align:center; color:var(--muted); font-style:italic; margin-bottom:4px; }}
.byline {{ text-align:center; color:var(--gold); letter-spacing:.22em;
  text-transform:uppercase; font-size:13px; font-family:Verdana,Arial,sans-serif; }}
hr {{ border:0; border-top:1px solid var(--line); margin:28px auto; width:120px; }}
h2 {{ color:var(--cyan); font-size:13px; letter-spacing:.2em; text-transform:uppercase;
  font-family:Verdana,Arial,sans-serif; margin:26px 0 12px; font-weight:normal; }}
p.lead {{ font-size:17px; }}
.reader {{ background:var(--navy2); border:1px solid var(--line); border-radius:8px;
  padding:26px 28px; }}
.reader p {{ margin-bottom:14px; }}
.reader p:last-child {{ margin-bottom:0; }}
.reader .src {{ color:var(--muted); font-style:italic; font-size:14px; margin-top:16px; }}
.facts {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:12px; }}
.fact {{ background:var(--navy2); border:1px solid var(--line); border-radius:8px; padding:12px 16px; }}
.fact .k {{ color:var(--muted); font-size:11px; letter-spacing:.14em; text-transform:uppercase;
  font-family:Verdana,Arial,sans-serif; }}
.fact .v {{ font-size:15px; margin-top:3px; }}
.buy {{ text-align:center; }}
.buy .note {{ color:var(--muted); font-size:14px; margin-bottom:14px; }}
.buy a {{ display:inline-block; margin:6px 8px; padding:12px 26px; border-radius:6px;
  background:var(--cyan-dim); color:#fff; text-decoration:none; font-size:15px;
  font-family:Verdana,Arial,sans-serif; border:1px solid var(--cyan); }}
.foot {{ text-align:center; color:var(--muted); font-size:12px; margin-top:44px;
  font-family:Verdana,Arial,sans-serif; }}
</style>
</head>
<body>
<div class="wrap">
  <p class="kicker">{series} &middot; Volume {volume}</p>
  <img class="cover" src="cover.png" alt="Cover of {title_attr}">
  <h1>{title}</h1>
  <p class="sub">{subtitle}</p>
  <p class="byline">{author}</p>
  <hr>
  <h2>About this book</h2>
  <p class="lead">{description}</p>
  <h2>Peek inside</h2>
  <div class="reader">
    {excerpt_ps}
    <p class="src">&mdash; {excerpt_heading}</p>
  </div>
  <h2>Details</h2>
  <div class="facts">{fact_divs}</div>
  {buy_section}
  <p class="foot">Published by {author} &middot; {series}</p>
</div>
</body>
</html>
"""

BUY_BLOCK = """  <h2>Get your copy</h2>
  <div class="buy">
    <p class="note">Available at your favourite ebook store.</p>
    {buy_links}
  </div>"""


def e(v: str) -> str:
    return html.escape(v, quote=True)


def build(slug: str) -> None:
    d = pathlib.Path(slug)
    spec = json.loads((d / "spec.json").read_text())
    excerpt_ps = "\n    ".join(
        "<p>" + e(p) + "</p>" for p in spec["excerpt"])
    fact_divs = "\n    ".join(
        f'<div class="fact"><div class="k">{e(k)}</div>'
        f'<div class="v">{e(v)}</div></div>'
        for k, v in spec["facts"].items())
    buy_section = ""
    links = {k: u for k, u in spec.get("buy_links", {}).items() if u}
    if links:
        buy_links = "\n    ".join(
            f'<a href="{e(u)}">{e(k)}</a>' for k, u in links.items())
        buy_section = BUY_BLOCK.format(buy_links=buy_links)
    page = TEMPLATE.format(
        title=e(spec["title"]),
        title_attr=e(spec["title"]),
        subtitle=e(spec["subtitle"]),
        author=e(spec["author"]),
        series=e(spec["series"]),
        volume=spec["volume"],
        description=e(spec["description"]),
        excerpt_ps=excerpt_ps,
        excerpt_heading=e(spec["excerpt_heading"]),
        fact_divs=fact_divs,
        buy_section=buy_section,
    )
    (d / "index.html").write_text(page)
    print(f"wrote {d / 'index.html'}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    build(sys.argv[1].strip("/"))
