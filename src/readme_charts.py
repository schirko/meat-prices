"""Make the charts shown in the README (D32). Run after a data refresh:

    python -m src.readme_charts

Writes docs/images/headline.png and docs/images/chain.png from master_monthly.csv,
and prints the numbers quoted in the README summary so they can be checked.
"""
import matplotlib
import matplotlib.dates

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from . import checks, config

OUT = config.DOCS_DIR / "images"
COLORS = {"beef": "#9A3B2E", "pork": "#2F6690", "chicken": "#C08A1E", "cpi": "#666666"}
LABELS = {"beef": "Ground beef", "pork": "Pork chops", "chicken": "Chicken breast"}


def _style(ax):
    ax.grid(alpha=0.3)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)


def headline(m):
    """All three meats and all prices, rebased so the 2015 average = 100."""
    p = m.loc[str(config.PRICE_START_YEAR):]
    rebase = lambda s: s / s.loc[str(config.PRICE_START_YEAR)].mean() * 100
    fig, ax = plt.subplots(figsize=(10, 5.2), dpi=150)
    for meat, label in LABELS.items():
        s = rebase(p[f"{meat}_price"])
        ax.plot(s.index, s, color=COLORS[meat], linewidth=2.6 if meat == "beef" else 1.8)
        ax.annotate(f"{label} {s.iloc[-1]:.0f}", (s.index[-1], s.iloc[-1]), xytext=(6, 0),
                    textcoords="offset points", va="center", color=COLORS[meat], fontsize=10,
                    fontweight="bold")
    cpi = rebase(p["cpi_all_items"])
    ax.plot(cpi.index, cpi, color=COLORS["cpi"], linestyle="--", linewidth=1.6)
    ax.annotate(f"All prices {cpi.iloc[-1]:.0f}", (cpi.index[-1], cpi.iloc[-1]), xytext=(6, 0),
                textcoords="offset points", va="center", color=COLORS["cpi"], fontsize=10)
    ax.axhline(100, color="#bbbbbb", linewidth=0.8)
    years = range(p.index.min().year + 1, p.index.max().year + 1, 2)
    ax.set_xticks([pd.Timestamp(f"{y}-01-01") for y in years])
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%Y"))
    ax.set_ylabel("Price, 2015 average = 100")
    ax.set_title("Beef pulled away from inflation; pork and chicken didn't",
                 loc="left", fontweight="bold", fontsize=13)
    ax.set_xlim(p.index.min(), p.index.max() + (p.index.max() - p.index.min()) * 0.17)
    _style(ax)
    fig.text(0.01, 0.01, f"U.S. average retail prices (BLS), {p.index.min():%b %Y} to {p.index.max():%b %Y}. "
             "Line above 'All prices' = rose faster than inflation.", fontsize=8, color="#555555")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(OUT / "headline.png")
    plt.close(fig)


def chain(m):
    """Drought -> cow sell-off -> smaller herd -> higher real beef price (D17)."""
    fig, axes = plt.subplots(4, 1, figsize=(10, 9), dpi=150, sharex=True)
    axes[0].fill_between(m.index, m["drought_cattle_d2_plus_pct"], color="#C08A1E", alpha=0.5)
    axes[0].set_ylabel("% of area")
    axes[0].set_title("1. Drought: cattle country in severe drought or worse", loc="left", fontweight="bold")
    axes[1].plot(m.index, m["slaughter_beef_cows_slaughtered_12mo"] / 1e6, color="#9A3B2E", linewidth=2)
    axes[1].set_ylabel("Millions, past 12 mo")
    axes[1].set_title("2. Sell-off: beef cows slaughtered", loc="left", fontweight="bold")
    axes[2].step(m.index, m["herd_beef_cows_jan1"] / 1e6, where="post", color="#5B3A1E", linewidth=2)
    axes[2].set_ylabel("Millions of head")
    axes[2].set_title("3. Herd: beef cows on January 1", loc="left", fontweight="bold")
    base = m["cpi_all_items"].last_valid_index()
    axes[3].plot(m.index, m["beef_price_real"], color="#9A3B2E", linewidth=2)
    axes[3].set_ylabel(f"Dollars per lb\n({base:%b %Y} dollars)")
    axes[3].set_title("4. Price: ground beef, adjusted for inflation", loc="left", fontweight="bold")
    for ax in axes:
        _style(ax)
    fig.tight_layout()
    fig.savefig(OUT / "chain.png")
    plt.close(fig)


def summary_numbers(m):
    """The figures quoted in the README, computed from the data."""
    base = m["cpi_all_items"].last_valid_index()
    y15 = m.loc[str(config.PRICE_START_YEAR)]
    out = {"latest month": f"{base:%B %Y}"}
    for meat in LABELS:
        out[f"{meat} nominal change since 2015 (%)"] = round((m.loc[base, f"{meat}_price"] / y15[f"{meat}_price"].mean() - 1) * 100)
        out[f"{meat} real change since 2015 (%)"] = round((m.loc[base, f"{meat}_price_real"] / y15[f"{meat}_price_real"].mean() - 1) * 100)
    out["all prices change since 2015 (%)"] = round((m.loc[base, "cpi_all_items"] / y15["cpi_all_items"].mean() - 1) * 100)
    herd = m["herd_beef_cows_jan1"]
    peak_year = herd.groupby(herd.index.year).first().loc[2015:].idxmax()
    out["beef cow herd peak year"] = int(peak_year)
    out["beef cow herd change peak to latest (%)"] = round((herd.iloc[-1] / herd.loc[str(peak_year)].iloc[0] - 1) * 100)
    sl = m["slaughter_beef_cows_slaughtered"].groupby(m.index.year).sum()
    herd_y = herd.groupby(herd.index.year).first()
    pct = (sl / herd_y * 100).loc[:base.year - 1]
    out["peak cow sell-off year"] = int(pct.idxmax())
    out["peak cow sell-off (% of herd)"] = round(pct.max(), 1)
    farmer = m["ers_beef_farmer_share_pct"].groupby(m.index.year).mean()
    out["rancher share of beef dollar, 2019 (%)"] = round(farmer.loc[2019])
    out[f"rancher share of beef dollar, {base.year - 1} (%)"] = round(farmer.loc[base.year - 1])
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    m = checks.load_master(config.PROCESSED_DIR / "master_monthly.csv")
    headline(m)
    chain(m)
    for k, v in summary_numbers(m).items():
        print(f"{k:45} {v}")
    print(f"Saved charts to {OUT.relative_to(config.PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
