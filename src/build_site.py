"""Build the GitHub Pages site in docs/ (D35). Run after a refresh or after changing a notebook:

    python -m src.build_site

What it does:
1. Redraws the summary charts (src/readme_charts.py) into docs/images/.
2. Fills the latest numbers into the front page template (src/site_template.html)
   and writes docs/index.html.
3. Exports every notebook, with its saved outputs, to docs/notebooks/<name>.html.
   Run and save each notebook in PyCharm first; this step doesn't run them.

GitHub Pages serves the docs/ folder of the master branch at
https://schirko.github.io/meat-prices/ (Settings -> Pages -> Deploy from a branch -> master, /docs).
"""
import re
from datetime import date
from string import Template

from . import checks, config, readme_charts

REPO = "https://github.com/schirko/meat-prices"
SITE_DIR = config.DOCS_DIR
NOTEBOOK_DIR = config.PROJECT_ROOT / "notebooks"
TEMPLATE = config.PROJECT_ROOT / "src" / "site_template.html"

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
}


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
    back = ('<div style="font:15px system-ui,sans-serif;padding:12px 20px;border-bottom:1px solid #ddd;'
            'background:#faf8f5"><a href="../index.html" style="color:#9A3B2E;text-decoration:none">'
            '&larr; Meat Price Explorer</a> &nbsp;·&nbsp; <a href="' + REPO + '/blob/master/notebooks/{name}" '
            'style="color:#555">view on GitHub</a></div>')
    listed = []
    for path in sorted(NOTEBOOK_DIR.glob("*.ipynb")):
        nb = nbformat.read(path, as_version=4)
        html, _ = exporter.from_notebook_node(nb, resources={"metadata": {"name": path.stem}})
        html = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + back.format(name=path.name), html, count=1)
        (out_dir / f"{path.stem}.html").write_text(html, encoding="utf-8")
        listed.append(path)
        print(f"  exported {path.name}")
    return listed


def notebook_list_html(paths):
    items = []
    for path in paths:
        number = path.stem[:2]
        title = notebook_title(path)
        title = re.sub(r"^\d+\s*·\s*", "", title)
        blurb = NOTEBOOK_BLURBS.get(number, "")
        items.append(f'<li><a href="notebooks/{path.stem}.html"><span class="num">{number}</span>'
                     f'<span class="nbtitle">{title}</span></a><span class="blurb">{blurb}</span></li>')
    return "\n".join(items)


def main():
    m = checks.load_master(config.PROCESSED_DIR / "master_monthly.csv")
    print("Charts:")
    readme_charts.OUT.mkdir(parents=True, exist_ok=True)
    readme_charts.headline(m)
    readme_charts.chain(m)
    n = readme_charts.summary_numbers(m)

    print("Notebooks:")
    paths = export_notebooks()

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
        "repo": REPO,
        "built": date.today().strftime("%B %d, %Y").replace(" 0", " "),  # no %-d: it fails on Windows
    }
    page = Template(TEMPLATE.read_text(encoding="utf-8")).substitute(values)
    (SITE_DIR / "index.html").write_text(page, encoding="utf-8")
    # Tell GitHub Pages to serve the files as they are (no Jekyll processing)
    (SITE_DIR / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Wrote {(SITE_DIR / 'index.html').relative_to(config.PROJECT_ROOT)} "
          f"(data through {values['latest_month']})")


if __name__ == "__main__":
    main()
