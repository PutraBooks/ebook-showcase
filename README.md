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
