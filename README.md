# ebook-showcase

One standalone buyer-facing preview page per ebook. Buyers arrive via a QR code
printed on the product listing; the QR points directly at the single book's page,
and no page links to any other book.

## Layout

- `<slug>/` - one directory per book: `spec.json`, `cover.png`, generated `index.html`
- `index.html` - neutral brand landing (no catalogue)
- `tools/build_page.py` - page generator

## Add a book

1. `mkdir <slug>` and copy the book's `cover.png` into it.
2. Write `<slug>/spec.json` (fields documented in `tools/build_page.py`).
3. `python3 tools/build_page.py <slug>`
4. Commit and push; the page appears at
   `https://putrabooks.github.io/ebook-showcase/<slug>/`

Fill `buy_links` with store URLs at release; empty links render no button.
QR code payload for a book is simply its page URL.

## Rules

- Never add cross-links between book pages.
- Keep the root landing catalogue-free.


## Family-sweep audit (2026-10-21): 1 fix

- ajbit-063 cover was the pre-2026-10-20 rejected "minimal-diagram" generation
  (page built 2026-10-17, before the cover regeneration campaign). Replaced with
  the shipped composed cover (byte-size 1667x2500, pixel-identical to the AJBIT
  shipped EPUB cover home); page regenerated with tools/build_page.py.
- ajbot-016 verified clean: cover pixel-identical to the shipped AJBOT cover.
- Reproducibility: both pages regenerate identically from spec.json + cover.png.
- Symlinks: 0. Secret-pattern scan: clean.
- Standing rule: build a showcase page only AFTER its book's cover clears the
  current generation, and re-copy cover.png when a book's cover is regenerated.
