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

Where it goes: the folder named by SITE_DIR in .env. On Scott's PC that is the
portfolio folder of the Schirko project, B:\\_Dev\\Python\\Schirko\\scott\\meat-prices,
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
}

# Project docs published as pages: file -> page title
DOC_PAGES = {
    "FINDINGS.md": "Findings and methods explained",
    "DECISIONS.md": "Every decision and why",
    "DATA_SOURCES.md": "Data sources",
    "DATA_DICTIONARY.md": "Column dictionary",
    "MILESTONES.md": "Plan and progress",
}

BACK_BAR = ('<div style="font:15px system-ui,sans-serif;padding:12px 20px;border-bottom:1px solid #ddd;'
            'background:#faf8f5"><a href="../index.html" style="color:#9A3B2E;text-decoration:none">'
            '&larr; Meat Price Explorer</a> &nbsp;·&nbsp; <a href="../../" style="color:#555;text-decoration:none">'
            'Scott Schirkofsky · Portfolio</a></div>')

DOC_PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{noindex}
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
        html = html.replace("<head>", "<head>\n" + NOINDEX, 1)
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
        page = DOC_PAGE.format(noindex=NOINDEX, title=title, back=BACK_BAR, body=body)
        (out_dir / f"{name[:-3]}.html").write_text(page, encoding="utf-8")
        print(f"  wrote docs/{name[:-3]}.html")


def notebook_list_html(paths):
    items = []
    for path in paths:
        number = path.stem[:2]
        title = re.sub(r"^\d+\s*·\s*", "", notebook_title(path))
        blurb = NOTEBOOK_BLURBS.get(number, "")
        items.append(f'<li><a href="notebooks/{path.stem}.html"><span class="num">{number}</span>'
                     f'<span class="nbtitle">{title}</span></a><span class="blurb">{blurb}</span></li>')
    return "\n".join(items)


def main():
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
    }
    page = Template(TEMPLATE.read_text(encoding="utf-8")).substitute(values)
    (SITE_DIR / "index.html").write_text(page, encoding="utf-8")
    print(f"Wrote index.html (data through {values['latest_month']})")


if __name__ == "__main__":
    main()
