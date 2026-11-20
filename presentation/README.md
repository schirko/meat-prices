# Presentation exports

The story presentation (D43) is a Claude Slides deck. Export it from the deck's
**Share → Export** menu and save the files here with these exact names:

| Export | Save as |
|---|---|
| PDF | `meat-prices-story.pdf` |
| PowerPoint | `meat-prices-story.pptx` |
| HTML | `meat-prices-story.html` |

The export menu has no image option, so `build_site` makes the slide images itself:
it draws each PDF page as a 1920-pixel PNG, zips them as
`meat-prices-story-slides.zip`, and saves the first as `cover.png`, the front page
thumbnail. It redoes this whenever the PDF is newer than the zip. It needs PyMuPDF:
`pip install pymupdf` (now in `requirements.txt`).

Then run `python -m src.build_site`. It copies whichever files exist to
`scott/meat-prices/presentation/` and builds the download buttons. After a data
refresh, run `python -m src.presentation_charts`, update the deck's images, re-export
and rebuild.
