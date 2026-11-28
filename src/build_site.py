"""Build the project site for schirko.com/scott/meat-prices (D36). Run after a refresh or
after changing a notebook:

    python -m src.build_site

What it does:
1. Redraws the summary charts (src/readme_charts.py) into docs/images/ and copies them.
2. Fills the latest numbers into the front page template (src/site_template.html).
3. Exports every notebook, with its saved outputs, to notebooks/<name>.html.
   Run and save each notebook in PyCharm first; this step doesn't run them.
4. Turns the project docs (decisions, data sources, column dictionary, milestones)
   into pages, so the site doesn't depend on the (private) GitHub repo.
5. Copies the exported presentation (presentation/ folder, D43) and builds its
   download buttons. Missing files are skipped; with none, the section is left out.

Where it goes: the folder named by SITE_DIR in .env. On Scott's PC that is the
portfolio folder of the Schirko project, B:\\Development\\Python\\Schirko\\scott\\meat-prices,
which schirko.com serves at /scott/meat-prices/ after a push (Coolify redeploys).
Without SITE_DIR the site is built into site/ here (ignored by git), for a local look.

Every page carries a noindex tag; schirko.com also sends a noindex header.
"""
import os
import re
import shutil
from datetime import date
from string import Template

from . import checks, config, readme_charts

SITE_DIR = config.Path(os.getenv("SITE_DIR", "").strip() or config.PROJECT_ROOT / "site")
NOTEBOOK_DIR = config.PROJECT_ROOT / "notebooks"
TEMPLATE = config.PROJECT_ROOT / "src" / "site_template.html"
NOINDEX = '<meta name="robots" content="noindex, nofollow">'

# One line per notebook for the front page; titles come from each notebook's first heading
NOTEBOOK_BLURBS = {
    "01": "Retail prices for ground beef, pork chops and chicken breast, and the Consumer Price Index.",
    "02": "How each retail dollar splits between farm, packer and store (USDA price spreads).",
    "03": "The beef cow herd every January 1, and how many cows go to slaughter each month.",
    "04": "Drought across cattle country, weighted by where the beef cows are.",
    "05": "Other grocery categories, for context: is meat special?",
    "06": "Cleaning every source and combining them into one monthly table.",
    "07": "First look at the combined data: inflation, the supply chain, who gets the dollar.",
    "08": "The 16 dated events on the price charts.",
    "11": "Testing whether prices really shifted at each event.",
    "12": "Measuring the chain: drought, then the cow sell-off, then the herd, then the price.",
    "13": "The verdict: inflation, who gets each beef dollar, and whether supply explains today's price.",
}

# The story presentation (D43). Scott exports these from the Slides artifact's Share > Export
# menu into presentation/ here; the builder copies whichever exist. file -> (label, note)
PRESENTATION_DIR = config.PROJECT_ROOT / "presentation"
PRESENTATION_FILES = {
    "meat-prices-story.pdf": ("PDF", "For reading or printing"),
    "meat-prices-story.pptx": ("PowerPoint", "Editable, with speaker notes"),
    "meat-prices-story.html": ("Web page", "One file, works offline"),
    "meat-prices-story-slides.zip": ("Slide images", "Every slide as a PNG, zipped"),
}
SLIDE_WIDTH = 1920  # pixels, for the PNGs made from the PDF

# Project docs published as pages: file -> page title
DOC_PAGES = {
    "FINDINGS.md": "Findings and methods explained",
    "DECISIONS.md": "Every decision and why",
    "DATA_SOURCES.md": "Data sources",
    "DATA_DICTIONARY.md": "Column dictionary",
    "MILESTONES.md": "Plan and progress",
}

# Shared "back to portfolio" bar (D40). The portfolio owns /scott/backbar.css; don't copy or restyle it.
BACKBAR_HEAD = """<link rel="stylesheet" href="/scott/backbar.css">
<link rel="icon" href="/scott/favicon.ico" sizes="32x32">
<link rel="icon" type="image/png" sizes="16x16" href="/scott/favicon-16.png">
<link rel="icon" type="image/png" sizes="32x32" href="/scott/favicon-32.png">
<link rel="apple-touch-icon" href="/scott/apple-touch-icon.png">"""  # stylesheet and favicons owned by the portfolio
BACKBAR = """<div class="sx-backbar">
  <a class="sx-back" href="/scott/">
    <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5"/><path d="m12 19-7-7 7-7"/></svg>
    Portfolio
  </a>
  <span class="sx-crumb">Meat Price Explorer</span>
  <span class="sx-links"><a href="/scott/meat-prices/">Overview</a><a href="/scott/meat-prices/explore.html">Explore</a><a href="/scott/meat-prices/notebooks/">Notebooks</a><a href="/scott/meat-prices/docs/">Docs</a></span>
</div>"""
BACK_BAR = BACKBAR  # first element inside <body> on notebook and doc pages

DOC_PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{noindex}
{backbar_head}
<title>{title} · Meat Price Explorer</title>
<style>
body {{ margin: 0; background: #faf8f5; color: #1f1b18; font: 16px/1.6 system-ui, sans-serif; }}
main {{ max-width: 860px; margin: 0 auto; padding: 8px 20px 60px; }}
a {{ color: #9A3B2E; }}
h1, h2, h3 {{ line-height: 1.25; }}
table {{ border-collapse: collapse; width: 100%; display: block; overflow-x: auto; font-size: 14.5px; }}
th, td {{ border: 1px solid #e0d9d0; padding: 6px 9px; text-align: left; vertical-align: top; }}
th {{ background: #f1ece6; }}
code {{ background: #f1ece6; padding: 1px 5px; border-radius: 4px; font-size: 0.92em; }}
pre {{ background: #f1ece6; padding: 12px; border-radius: 8px; overflow-x: auto; }}
pre code {{ background: none; padding: 0; }}
@media (prefers-color-scheme: dark) {{
  body {{ background: #171412; color: #f1ece6; }} a {{ color: #e0796a; }}
  th, code, pre {{ background: #2a2420; }} th, td {{ border-color: #3a332e; }}
}}
</style></head>
<body>{back}<main>{body}</main></body></html>
"""


def notebook_title(path):
    import nbformat
    nb = nbformat.read(path, as_version=4)
    first = nb.cells[0].source.splitlines()[0] if nb.cells else path.stem
    return first.lstrip("# ").strip()


def export_notebooks():
    """Export each notebook to standalone HTML with a link back to the front page."""
    import nbformat
    from nbconvert import HTMLExporter

    out_dir = SITE_DIR / "notebooks"
    out_dir.mkdir(parents=True, exist_ok=True)
    exporter = HTMLExporter(template_name="lab")
    listed = []
    for path in sorted(NOTEBOOK_DIR.glob("*.ipynb")):
        nb = nbformat.read(path, as_version=4)
        html, _ = exporter.from_notebook_node(nb, resources={"metadata": {"name": path.stem}})
        html = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + BACK_BAR, html, count=1)
        # Let the shared bar run edge to edge: move the notebook template's page margin onto its content
        edge = "<style>body.jp-Notebook{margin:0;padding:0}body.jp-Notebook>main{padding:10px 18px}</style>"
        html = html.replace("<head>", "<head>\n" + NOINDEX + "\n" + BACKBAR_HEAD + "\n" + edge, 1)
        (out_dir / f"{path.stem}.html").write_text(html, encoding="utf-8")
        listed.append(path)
        print(f"  exported {path.name}")
    return listed


def export_docs():
    """Turn the project's Markdown docs into pages under docs/."""
    import mistune  # installed with nbconvert

    to_html = mistune.create_markdown(plugins=["table", "strikethrough"])
    out_dir = SITE_DIR / "docs"
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, title in DOC_PAGES.items():
        body = to_html((config.DOCS_DIR / name).read_text(encoding="utf-8"))
        # Links between the docs: DECISIONS.md -> DECISIONS.html
        for other in DOC_PAGES:
            body = body.replace(f'href="{other}', f'href="{other[:-3]}.html').replace(
                f'href="docs/{other}', f'href="{other[:-3]}.html')
        page = DOC_PAGE.format(noindex=NOINDEX, backbar_head=BACKBAR_HEAD, title=title, back=BACK_BAR, body=body)
        (out_dir / f"{name[:-3]}.html").write_text(page, encoding="utf-8")
        print(f"  wrote docs/{name[:-3]}.html")


# ---------------------------------------------------------------- explorer page (D39)
GROCERIES = {
    "all_items": "All prices",
    "food_at_home": "Groceries overall",
    "cereals_and_bakery": "Cereals and bakery",
    "dairy": "Dairy",
    "eggs": "Eggs",
    "fresh_fruits_and_vegetables": "Fresh fruits and vegetables",
    "nonalcoholic_beverages": "Non-alcoholic drinks",
    "food_away_from_home": "Restaurant meals",
}
DOLLAR_PARTS = {
    "beef": {"rancher / farmer": "net_farm", "packer / processor": "spread_farm_to_wholesale",
             "store": "spread_wholesale_to_retail"},
    "pork": {"rancher / farmer": "net_farm", "packer / processor": "spread_farm_to_wholesale",
             "store": "spread_wholesale_to_retail"},
    "chicken": {"farm + packer (wholesale)": "wholesale", "store": "spread_wholesale_to_retail"},
}
# Short notes shown when one year is picked. Written for the data through October 2026 (checked after the November 2026 refresh).
YEAR_NOTES = {
    "2015": "The beef herd was rebuilding after the 2011–2013 drought, so beef started high and then eased.",
    "2016": "A growing herd and mild drought: real beef prices kept falling.",
    "2017": "The herd kept growing; beef was close to its cheapest real price in this data.",
    "2018": "The herd was near its peak, and real beef prices stayed low.",
    "2019": "The beef herd peaked at 31.6 million cows, but ranchers had started selling more cows than they replaced.",
    "2020": "COVID-19 closed meatpacking plants in April and May: the clearest price shock in the data, for all three meats, and it faded within months.",
    "2021": "Drought returned to cattle country, and the JBS cyberattack hit in early June.",
    "2022": "The cow sell-off peaked (13.2% of the herd). Chicken spiked with feed costs and bird flu.",
    "2023": "The herd kept shrinking after three years of heavy selling.",
    "2024": "With the herd near its low, beef's price climb steepened. Mexican cattle imports were suspended in November.",
    "2025": "The herd was the smallest in this data. Imports were suspended again in May, and many heifers still went to slaughter.",
    "2026": "Drought is back, but ranchers are keeping their cows. Beef runs about 11% above what the herd explains, mostly in store margins.",
}


def _date_label(value, precision):
    import pandas as pd
    d = pd.Timestamp(value)
    if precision == "day":
        return f"{d:%b} {d.day}, {d.year}"
    if precision == "year":
        return f"{d.year}"
    return f"{d:%b %Y}"


def explorer_data(m):
    """Everything the explorer page needs, as plain lists and dicts."""
    import json
    import pandas as pd

    prices = m.loc[str(config.PRICE_START_YEAR):].dropna(subset=["beef_price"])
    latest = prices.index.max()
    clean = lambda s: [None if pd.isna(v) else round(float(v), 3) for v in s]
    data = {
        "months": [f"{d:%Y-%m}" for d in prices.index],
        "latest_label": f"{latest:%B %Y}",
        "years_partial": latest.year if latest.month < 12 else None,
        "built": date.today().strftime("%B %d, %Y").replace(" 0", " "),
        "nominal": {k: clean(prices[f"{k}_price"]) for k in ["beef", "pork", "chicken"]},
        "real": {k: clean(prices[f"{k}_price_real"]) for k in ["beef", "pork", "chicken"]},
        "groceries": {k: {"name": name, "values": clean(prices[f"cpi_{k}_2015eq100"])} for k, name in GROCERIES.items()},
        "estimated": [f"{d:%Y-%m}" for d in prices.index[prices["filled_columns"].fillna("").astype(str).str.contains("beef_price")]],
    }

    # Who gets each dollar: yearly averages in latest-month dollars (same method as notebook 13)
    to_today = m.loc[latest, "cpi_all_items"] / m["cpi_all_items"]
    data["dollar"] = {}
    for meat, parts in DOLLAR_PARTS.items():
        yearly = {stage: (m[f"ers_{meat}_{col}"] * to_today / 100).groupby(m.index.year).mean().loc[config.PRICE_START_YEAR:]
                  for stage, col in parts.items()}
        years = list(next(iter(yearly.values())).index)
        data["dollar"][meat] = {"years": [int(y) for y in years],
                                "parts": {stage: [round(float(v), 2) for v in s] for stage, s in yearly.items()}}

    # Events, with labels and (if notebook 11 has been run) its test results
    events = pd.read_csv(config.PROCESSED_DIR / "events.csv", parse_dates=["start_date", "end_date"])
    tests = {}
    tests_file = config.PROCESSED_DIR / "event_tests.csv"
    if tests_file.exists():
        for _, r in pd.read_csv(tests_file).iterrows():
            tests.setdefault(r["event_id"], []).append({
                "meat": r["meat"], "gap": round(float(r["gap_pct"]), 1), "verdict": r["verdict"],
                "simple_verdict": r["simple_verdict"], "agree": bool(r["agree"])})
    data["tests"] = tests
    data["events"] = []
    for _, e in events.iterrows():
        end = e["end_date"]
        if pd.isna(end) and e["category"] == "weather":
            end = latest  # a drought still going on runs to the latest month (as in notebook 08)
        data["events"].append({
            "id": e["event_id"], "name": e["event"], "category": e["category"], "meats": e["meats"].split(";"),
            "claim": e["popular_explanation"] == "yes", "expected": e["expected_effect"],
            "notes": "" if pd.isna(e["notes"]) else e["notes"],
            "source_name": "" if pd.isna(e["source_name"]) else e["source_name"],
            "source_url": "" if pd.isna(e["source_url"]) else e["source_url"],
            "start": f"{e['start_date']:%Y-%m-%d}", "end": None if pd.isna(end) else f"{end:%Y-%m-%d}",
            "start_label": _date_label(e["start_date"], e["date_precision"]),
            "end_label": None if pd.isna(end) else ("ongoing" if pd.isna(e["end_date"]) else _date_label(end, e["date_precision"])),
        })

    # "What it means" text per selection
    first = prices.loc[str(config.PRICE_START_YEAR)]
    real_change = {k: (prices[f"{k}_price_real"].iloc[-1] / first[f"{k}_price_real"].mean() - 1) * 100
                   for k in ["beef", "pork", "chicken"]}
    data["meaning"] = {
        "beef": (f"After inflation, ground beef costs {real_change['beef']:.0f}% more than in 2015, the only meat that "
                 "does. Its rise follows the cattle herd: drought pushed ranchers to sell cows, the herd shrank to its "
                 "smallest in this data, and a 1% smaller herd goes with about a 1.8% higher real price. Since 2019 most "
                 "of the extra money went to ranchers; packers were squeezed. In 2026 beef runs about 11% above what "
                 "the herd explains, and that extra went mainly into store margins."),
        "pork": (f"After inflation, pork chops cost {abs(real_change['pork']):.0f}% less than in 2015. The 2020 COVID "
                 "plant closures caused the biggest jump in the series, and it faded within months. How each dollar "
                 "is split has barely changed since 2019."),
        "chicken": (f"After inflation, chicken breast costs {abs(real_change['chicken']):.0f}% less than in 2015. Its "
                    "2022 spike was real and lines up with higher feed costs and bird flu at the same time. The "
                    "popular claims (plant fires, Colorado culls, the cage-free egg law) don't line up with any jump."),
        "all": ("Only beef costs more than in 2015 after inflation. Turn on <i>After inflation</i> to see it: beef sits "
                "above 100 while pork and chicken sit below. Use <i>Compare with</i> to set meat against the rest of "
                "the grocery cart."),
    }
    data["year_notes"] = YEAR_NOTES
    return json.dumps(data, separators=(",", ":"), allow_nan=False).replace("</", "<\\/")


def build_explorer(m):
    template = (config.PROJECT_ROOT / "src" / "explore_template.html").read_text(encoding="utf-8")
    marker = "const D = __DATA__;"
    assert marker in template, "explore_template.html must contain: " + marker
    page = template.replace(marker, "const D = " + explorer_data(m) + ";", 1)
    page = page.replace("<!--BACKBAR_HEAD-->", BACKBAR_HEAD, 1).replace("<!--BACKBAR-->", BACKBAR, 1)
    (SITE_DIR / "explore.html").write_text(page, encoding="utf-8")
    print("  wrote explore.html")


def folder_indexes(paths):
    """notebooks/index.html and docs/index.html, so the bar's Notebooks and Docs links open a list (D40)."""
    nb_items = []
    for p in paths:
        title = re.sub(r"^\d+\s*·\s*", "", notebook_title(p))
        nb_items.append(f'<li><a href="{p.stem}.html"><b>{p.stem[:2]}</b> · {title}</a>'
                        f'<br><span class="blurb">{NOTEBOOK_BLURBS.get(p.stem[:2], "")}</span></li>')
    nb_items = "\n".join(nb_items)
    doc_items = "\n".join(f'<li><a href="{name[:-3]}.html"><b>{title}</b></a></li>' for name, title in DOC_PAGES.items())
    style = ("<style>ul.list{list-style:none;padding:0}ul.list li{padding:10px 0;border-bottom:1px solid #e0d9d0}"
             "ul.list a{text-decoration:none}.blurb{color:#6b6560;font-size:15px}</style>")
    for folder, title, intro, items in [
        ("notebooks", "The notebooks",
         "Every step of the analysis, in order. Each notebook says what it's looking for, shows the code and its "
         "result, then how to read it and what it means.", nb_items),
        ("docs", "Project docs",
         "Start with <i>Findings and methods explained</i> for the whole project in plain language.", doc_items),
    ]:
        body = f"{style}<h1>{title}</h1><p>{intro}</p><ul class=\"list\">{items}</ul>"
        page = DOC_PAGE.format(noindex=NOINDEX, backbar_head=BACKBAR_HEAD, title=title, back=BACK_BAR, body=body)
        (SITE_DIR / folder / "index.html").write_text(page, encoding="utf-8")
        print(f"  wrote {folder}/index.html")


def notebook_list_html(paths):
    items = []
    for path in paths:
        number = path.stem[:2]
        title = re.sub(r"^\d+\s*·\s*", "", notebook_title(path))
        blurb = NOTEBOOK_BLURBS.get(number, "")
        items.append(f'<li><a href="notebooks/{path.stem}.html"><span class="num">{number}</span>'
                     f'<span class="nbtitle">{title}</span></a><span class="blurb">{blurb}</span></li>')
    return "\n".join(items)


def _size(path):
    b = path.stat().st_size
    return f"{b / 1e6:.1f}&nbsp;MB" if b >= 1e6 else f"{max(1, round(b / 1e3))}&nbsp;KB"


def _source(name):
    """The exported file for a published name (D43).

    The exact name if it's there; otherwise the newest file of the same type, so the
    export menu's own names ("Why Does Meat Cost So Much Now.pdf") work without renaming.
    Returns None when there is no such file."""
    exact = PRESENTATION_DIR / name
    if exact.exists():
        return exact
    suffix = exact.suffix.lower()
    if suffix in (".zip", ".png"):  # made by slides_from_pdf, always under the exact name
        return None
    matches = [f for f in PRESENTATION_DIR.glob("*") if f.is_file() and f.suffix.lower() == suffix]
    return max(matches, key=lambda f: f.stat().st_mtime) if matches else None


def slides_from_pdf():
    """Make the slide-images zip and cover thumbnail from the exported PDF (D43).

    The Slides export menu offers PDF, PowerPoint and HTML but no images, so each PDF page
    is drawn as a PNG here with PyMuPDF. Skipped when the PDF is missing or the zip is
    already newer than it."""
    pdf = _source("meat-prices-story.pdf")
    zip_path = PRESENTATION_DIR / "meat-prices-story-slides.zip"
    if pdf is None or (zip_path.exists() and zip_path.stat().st_mtime >= pdf.stat().st_mtime):
        return
    import zipfile
    import pymupdf
    with pymupdf.open(pdf) as doc, zipfile.ZipFile(zip_path, "w", zipfile.ZIP_STORED) as z:
        for i, page in enumerate(doc, start=1):
            zoom = SLIDE_WIDTH / page.rect.width
            png = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom)).tobytes("png")
            z.writestr(f"meat-prices-story-slide-{i:02d}.png", png)
            if i == 1:
                thumb = 800 / page.rect.width
                page.get_pixmap(matrix=pymupdf.Matrix(thumb, thumb)).save(PRESENTATION_DIR / "cover.png")
        n = len(doc)
    print(f"  made {zip_path.name} and cover.png from the PDF ({n} slides)")


def presentation_html():
    """Copy the exported presentation files to the site and return the front page section.

    The cover thumbnail is presentation/cover.png if it exists, otherwise the first PNG
    inside the slide-images zip. Returns "" when no files have been exported yet."""
    slides_from_pdf()
    sources = {f: _source(f) for f in PRESENTATION_FILES}
    found = {f: v for f, v in PRESENTATION_FILES.items() if sources[f] is not None}
    if not found:
        print("  no exported presentation files in presentation/; section left out")
        return ""
    out = SITE_DIR / "presentation"
    out.mkdir(exist_ok=True)
    for f in found:
        shutil.copy2(sources[f], out / f)
        print(f"  {sources[f].name} -> {f} ({_size(sources[f]).replace('&nbsp;', ' ')})")

    cover = ""
    if (PRESENTATION_DIR / "cover.png").exists():
        shutil.copy2(PRESENTATION_DIR / "cover.png", out / "cover.png")
        cover = "presentation/cover.png"
    elif "meat-prices-story-slides.zip" in found:
        import zipfile
        with zipfile.ZipFile(PRESENTATION_DIR / "meat-prices-story-slides.zip") as z:
            pngs = sorted(n for n in z.namelist() if n.lower().endswith(".png"))
            if pngs:
                (out / "cover.png").write_bytes(z.read(pngs[0]))
                cover = "presentation/cover.png"

    n_slides = 14
    if "meat-prices-story-slides.zip" in found:
        import zipfile
        with zipfile.ZipFile(PRESENTATION_DIR / "meat-prices-story-slides.zip") as z:
            n_slides = sum(n.lower().endswith(".png") for n in z.namelist()) or n_slides
    view = "presentation/meat-prices-story.html" if "meat-prices-story.html" in found else \
           "presentation/meat-prices-story.pdf" if "meat-prices-story.pdf" in found else ""
    thumb = (f'<a class="deck-thumb" href="{view or cover}"><img src="{cover}" '
             f'alt="Cover slide: Why does meat cost so much now?"><span>{n_slides} slides</span></a>') if cover else ""
    view_btn = f'<a class="btn primary" href="{view}" target="_blank" rel="noopener">View the presentation</a>' if view else ""
    tiles = "\n".join(
        f'<a class="dl" href="presentation/{f}" download><span class="ext">{f.rsplit(".", 1)[1].upper()}</span>'
        f'<span><b>{label}</b><small>{note} · {_size(sources[f])}</small></span></a>'
        for f, (label, note) in found.items())
    return f"""<h2 id="presentation">The story, as a presentation</h2>
<div class="deck">
  {thumb}
  <div>
    <p class="note" style="margin-top:0">The whole project told as a {n_slides}-slide business story: the question, what the
    data shows for each meat, the events people blame, the real cause, who got the money and the verdict.</p>
    {view_btn}
    <div class="dls">
{tiles}
    </div>
  </div>
</div>"""


def check_site_dir():
    """Refuse to build anywhere but this project's own folder (D41).

    The portfolio owns scott/index.html and scott/styles.css; this project owns only
    scott/meat-prices/ (and its card screenshot). A SITE_DIR pointing at the scott/
    folder would overwrite the portfolio's index.html, so the build stops instead.
    """
    allowed = SITE_DIR.name == "meat-prices" or SITE_DIR.resolve() == (config.PROJECT_ROOT / "site").resolve()
    if not allowed:
        raise SystemExit(f"SITE_DIR must be the meat-prices folder (or the local site/ preview), not {SITE_DIR}. "
                         "This project only writes inside scott/meat-prices/ (D41).")


def main():
    check_site_dir()
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Building the site in {SITE_DIR}")
    m = checks.load_master(config.PROCESSED_DIR / "master_monthly.csv")

    print("Charts:")
    readme_charts.OUT.mkdir(parents=True, exist_ok=True)
    readme_charts.headline(m)
    readme_charts.chain(m)
    (SITE_DIR / "images").mkdir(exist_ok=True)
    for png in ["headline.png", "chain.png"]:
        shutil.copy2(readme_charts.OUT / png, SITE_DIR / "images" / png)
    n = readme_charts.summary_numbers(m)

    print("Notebooks:")
    paths = export_notebooks()
    print("Docs:")
    export_docs()
    folder_indexes(paths)
    print("Explorer:")
    build_explorer(m)
    print("Presentation:")
    presentation = presentation_html()

    base = m["cpi_all_items"].last_valid_index()
    groceries = m["cpi_food_at_home_2015eq100"].dropna()
    values = {
        "latest_month": n["latest month"],
        "beef_nominal": n["beef nominal change since 2015 (%)"],
        "beef_real": n["beef real change since 2015 (%)"],
        "pork_nominal": n["pork nominal change since 2015 (%)"],
        "pork_real": -n["pork real change since 2015 (%)"],
        "chicken_nominal": n["chicken nominal change since 2015 (%)"],
        "chicken_real": -n["chicken real change since 2015 (%)"],
        "all_prices": n["all prices change since 2015 (%)"],
        "groceries": round(groceries.iloc[-1] - 100),
        "herd_peak_year": n["beef cow herd peak year"],
        "herd_change": -n["beef cow herd change peak to latest (%)"],
        "selloff_year": n["peak cow sell-off year"],
        "selloff_pct": n["peak cow sell-off (% of herd)"],
        "rancher_2019": n["rancher share of beef dollar, 2019 (%)"],
        "rancher_latest": n[f"rancher share of beef dollar, {base.year - 1} (%)"],
        "rancher_year": base.year - 1,
        "notebooks": notebook_list_html(paths),
        "built": date.today().strftime("%B %d, %Y").replace(" 0", " "),  # no %-d: it fails on Windows
        "backbar_head": BACKBAR_HEAD,
        "backbar": BACKBAR,
        "presentation": presentation,
        "presentation_link": '<a class="btn" href="#presentation">The presentation</a>' if presentation else "",
    }
    page = Template(TEMPLATE.read_text(encoding="utf-8")).substitute(values)
    (SITE_DIR / "index.html").write_text(page, encoding="utf-8")
    print(f"Wrote index.html (data through {values['latest_month']})")


if __name__ == "__main__":
    main()
