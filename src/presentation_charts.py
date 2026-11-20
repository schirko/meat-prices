"""Regenerate the story presentation's charts (D43). Run after a data refresh:

    python -m src.presentation_charts

Writes nine charts to docs/presentation_charts/, drawn from master_monthly.csv and
event_tests.csv in the presentation's palette. The deck ("Why Does Meat Cost So Much
Now?", a Claude slide deck built from docs/PRESENTATION_PLAN.md) uses these images;
after a refresh, update the deck with the new charts and numbers, then re-export the
PDF to the portfolio folder as presentation.pdf.

Charts (sized for a 1920x1080 slide at 2x): hero (rebased lines), bars (real change
since 2015), mini_beef / mini_pork / mini_chicken (price per meat with its events),
events_dots (event tests vs. ordinary months, dark), chain_big (drought -> sell-off ->
herd -> price), dollar_stack (who gets each beef dollar), cover_bg (title backdrop).
"""
import json
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from . import config  # noqa: E402

OUT = config.DOCS_DIR / "presentation_charts"
INK, PAPER, ALT, MUTED = "#1F1B18", "#FAF8F5", "#F1ECE6", "#5F5852"
BEEF, PORK, CHICK = "#9A3B2E", "#2F6690", "#A87613"
RANCH, PACK, STORE = "#5B3A1E", "#7A4E9C", "#2F7A4B"
GRID_L, GRID_D, LIGHT = "#E3DAD1", "#3D3631", "#D9D1C9"


def style(ax, bg, dark=False, ts=17):
    ax.set_facecolor(bg)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    for s in ["left", "bottom"]:
        ax.spines[s].set_color(GRID_D if dark else GRID_L)
        ax.spines[s].set_linewidth(1.5)
    ax.tick_params(colors=LIGHT if dark else MUTED, labelsize=ts, length=0, pad=10)
    ax.grid(color=GRID_D if dark else GRID_L, linewidth=1.2)
    ax.set_axisbelow(True)


def save(fig, name, bg):
    fig.savefig(OUT / name, dpi=200, facecolor=bg)
    plt.close(fig)
    print(f"  wrote {name}")


def year_ticks(ax, start=2016, end=2026, step=2):
    ax.set_xticks([pd.Timestamp(f"{y}-01-01") for y in range(start, end + 1, step)])
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))


def hero(p):
    rebase = lambda s: s / s.loc["2015"].mean() * 100
    fig, ax = plt.subplots(figsize=(16.64, 5.0))
    fig.patch.set_facecolor(PAPER)
    for col, name, c, lw in [("beef_price", "Ground beef", BEEF, 5),
                             ("chicken_price", "Chicken breast", CHICK, 3.2),
                             ("pork_price", "Pork chops", PORK, 3.2)]:
        s = rebase(p[col])
        ax.plot(s.index, s, color=c, lw=lw, solid_capstyle="round")
        ax.annotate(f"{name}  {s.iloc[-1]:.0f}", (s.index[-1], s.iloc[-1]), xytext=(14, 0),
                    textcoords="offset points", va="center", color=c, fontsize=21, fontweight="bold")
    cpi = rebase(p["cpi_all_items"])
    ax.plot(cpi.index, cpi, color=MUTED, ls=(0, (6, 4)), lw=2.6)
    ax.annotate(f"All prices  {cpi.iloc[-1]:.0f}", (cpi.index[-1], cpi.iloc[-1]), xytext=(14, 0),
                textcoords="offset points", va="center", color=MUTED, fontsize=21)
    ax.axhline(100, color=MUTED, lw=1.4)
    ax.annotate("2015 average = 100", (p.index[4], 103), fontsize=16, color=MUTED, va="bottom")
    ax.set_xlim(p.index.min(), p.index.max() + pd.DateOffset(months=44))
    year_ticks(ax)
    style(ax, PAPER)
    fig.tight_layout(pad=0.6)
    save(fig, "hero.png", PAPER)


def bars(m, p):
    real = lambda col: (p[col].iloc[-1] / p[col].loc["2015"].mean() - 1) * 100
    g_real = (m["cpi_food_at_home_2015eq100"].dropna().iloc[-1]
              / (p["cpi_all_items"].iloc[-1] / p["cpi_all_items"].loc["2015"].mean() * 100) - 1) * 100
    rows = [("Ground beef", real("beef_price_real"), BEEF),
            ("Groceries overall", g_real, MUTED),
            ("Chicken breast", real("chicken_price_real"), CHICK),
            ("Pork chops", real("pork_price_real"), PORK)]
    fig, ax = plt.subplots(figsize=(16.64, 5.0))
    fig.patch.set_facecolor(ALT)
    ys = np.arange(len(rows))[::-1]
    for y, (name, v, c) in zip(ys, rows):
        ax.barh(y, v, height=0.62, color=c, zorder=3)
        ax.annotate(f"{v:+.0f}%", (v, y), xytext=(14 if v > 0 else -14, 0), textcoords="offset points",
                    va="center", ha="left" if v > 0 else "right", fontsize=24, fontweight="bold", color=c)
        ax.annotate(name, (0, y), xytext=(-14 if v > 0 else 14, 0), textcoords="offset points",
                    va="center", ha="right" if v > 0 else "left", fontsize=21, color=INK)
    ax.axvline(0, color=INK, lw=2.4, zorder=4)
    ax.annotate("Same price as 2015, after inflation", (0, len(rows) - 0.28), fontsize=16, color=MUTED, ha="center")
    ax.set_xlim(-32, 26)
    ax.set_ylim(-0.6, len(rows) - 0.15)
    ax.set_yticks([])
    ax.xaxis.set_major_formatter(lambda x, _: f"{x:+.0f}%")
    style(ax, ALT)
    ax.grid(axis="y", alpha=0)
    fig.tight_layout(pad=0.6)
    save(fig, "bars.png", ALT)


def minis(p):
    def base(col, c, bg, yticks):
        fig, ax = plt.subplots(figsize=(9.0, 5.4))
        fig.patch.set_facecolor(bg)
        s = p[col]
        ax.set_yticks(yticks)
        ax.yaxis.set_major_formatter(lambda x, _: f"${x:.0f}")
        year_ticks(ax)
        style(ax, bg)
        return fig, ax, s

    fig, ax, s = base("beef_price", BEEF, PAPER, [4, 5, 6, 7])
    ax.axvspan(pd.Timestamp("2020-04-01"), pd.Timestamp("2020-07-01"), color=BEEF, alpha=0.12)
    ax.plot(s.index, s, color=BEEF, lw=4, solid_capstyle="round")
    ax.annotate("COVID\nclosures", (pd.Timestamp("2020-05-15"), s.max()), fontsize=15, color=MUTED,
                ha="center", va="top", linespacing=1.3)
    ax.axvline(pd.Timestamp("2025-05-11"), color=MUTED, lw=1.8, ls=(0, (4, 3)))
    ax.annotate("Mexico\nimport halt", (pd.Timestamp("2025-05-11"), s.min() * 1.02), fontsize=15, color=MUTED,
                ha="right", va="bottom", xytext=(-10, 0), textcoords="offset points", linespacing=1.3)
    fig.tight_layout(pad=0.6)
    save(fig, "mini_beef.png", PAPER)

    fig, ax, s = base("pork_price", PORK, ALT, [3, 4, 5])
    ax.axvspan(pd.Timestamp("2020-04-01"), pd.Timestamp("2020-07-01"), color=PORK, alpha=0.12)
    ax.plot(s.index, s, color=PORK, lw=4, solid_capstyle="round")
    ax.annotate("COVID\nclosures", (pd.Timestamp("2020-05-15"), s.max()), fontsize=15, color=MUTED,
                ha="center", va="top", linespacing=1.3)
    fig.tight_layout(pad=0.6)
    save(fig, "mini_pork.png", ALT)

    fig, ax, s = base("chicken_price", CHICK, PAPER, [3, 4])
    ax.axvspan(pd.Timestamp("2020-04-01"), pd.Timestamp("2020-07-01"), color=CHICK, alpha=0.10)
    ax.axvspan(pd.Timestamp("2022-02-01"), pd.Timestamp("2023-01-01"), color=CHICK, alpha=0.14)
    ax.plot(s.index, s, color=CHICK, lw=4, solid_capstyle="round")
    ax.annotate("Feed costs\n+ bird flu", (pd.Timestamp("2023-02-15"), s.max() * 0.995), fontsize=15, color=MUTED,
                ha="left", va="top", linespacing=1.3)
    ax.annotate("COVID", (pd.Timestamp("2020-05-15"), s.max() * 0.995), fontsize=15, color=MUTED,
                ha="center", va="top")
    fig.tight_layout(pad=0.6)
    save(fig, "mini_chicken.png", PAPER)


def events_dots():
    """The curated event tests against each meat's ordinary range (notebook 11)."""
    tests = pd.read_csv(config.PROCESSED_DIR / "event_tests.csv")
    nb = json.loads((config.PROJECT_ROOT / "notebooks" / "11_event_tests.ipynb").read_text(encoding="utf-8"))
    band_line = ""
    for cell in nb["cells"]:
        for o in cell.get("outputs", []):
            t = "".join(o.get("text", []))
            if "95% of ordinary months" in t:
                band_line = t
    bands = {k: float(v) for k, v in re.findall(r"'(\w+)': '±([\d.]+)%'", band_line)}
    mc = {"beef": BEEF, "pork": PORK, "chicken": CHICK}
    want = [("E03", "pork", "COVID plant closures — pork"),
            ("E03", "chicken", "COVID plant closures — chicken"),
            ("E03", "beef", "COVID plant closures — beef"),
            ("E06", "chicken", "2022 feed costs + bird flu — chicken"),
            ("E12", "beef", "Mexico import halt, May 2025 — beef"),
            ("E05", "beef", "JBS cyberattack — beef"),
            ("E02", "beef", "Tyson plant fire 2019 — beef"),
            ("E09", "chicken", "Colorado bird-flu culls — chicken"),
            ("E11", "chicken", "Cage-free egg law — chicken")]
    fig, ax = plt.subplots(figsize=(16.64, 5.2))
    fig.patch.set_facecolor(INK)
    ys = np.arange(len(want))[::-1]
    for y, (eid, meat, label) in zip(ys, want):
        r = tests[(tests.event_id == eid) & (tests.meat == meat)].iloc[0]
        b = bands.get(meat, 5)
        ax.barh(y, 2 * b, left=-b, height=0.6, color="#332D28", zorder=2)
        ax.scatter([r.gap_pct], [y], s=260, color=mc[meat], edgecolor=PAPER, linewidth=2.2, zorder=4)
        far_right = r.gap_pct > 14
        ax.annotate(f"{r.gap_pct:+.0f}%", (r.gap_pct, y), xytext=(16, 0) if far_right else (0, 16),
                    textcoords="offset points", ha="left" if far_right else "center",
                    va="center" if far_right else "baseline", fontsize=17, fontweight="bold",
                    color=mc[meat] if abs(r.gap_pct) > b else LIGHT)
        ax.annotate(label, (-19.6, y), va="center", ha="left", fontsize=17, color=LIGHT)
    ax.axvline(0, color=LIGHT, lw=1.6, zorder=3)
    ax.annotate("Gray band: the normal range of ordinary months. A dot outside it is a real shift.",
                (19.6, -1.08), fontsize=16, color=LIGHT, ha="right", va="bottom")
    ax.set_xlim(-20, 20)
    ax.set_ylim(-1.25, len(want) - 0.3)
    ax.set_yticks([])
    ax.xaxis.set_major_formatter(lambda x, _: f"{x:+.0f}%")
    style(ax, INK, dark=True)
    ax.grid(axis="y", alpha=0)
    fig.tight_layout(pad=0.6)
    save(fig, "events_dots.png", INK)


def chain(m):
    c = m.loc["2010":]
    fig, axes = plt.subplots(4, 1, figsize=(8.2, 6.6), sharex=True)
    fig.patch.set_facecolor(PAPER)
    axes[0].fill_between(c.index, c["drought_cattle_d2_plus_pct"], color="#C9952F", alpha=0.75, lw=0)
    axes[0].set_title("Drought: % of cattle country in severe drought", loc="left", fontsize=20,
                      fontweight="bold", color=INK, pad=7)
    axes[1].plot(c.index, c["slaughter_beef_cows_slaughtered_12mo"] / 1e6, color=RANCH, lw=3.2)
    axes[1].set_title("Cows sold for slaughter (millions, past 12 months)", loc="left", fontsize=20,
                      fontweight="bold", color=INK, pad=7)
    axes[2].step(c.index, c["herd_beef_cows_jan1"] / 1e6, where="post", color=INK, lw=3.2)
    axes[2].set_title("The beef cow herd on January 1 (millions)", loc="left", fontsize=20,
                      fontweight="bold", color=INK, pad=7)
    axes[3].plot(c.index, c["beef_price_real"], color=BEEF, lw=3.2)
    axes[3].set_title("Ground beef, after inflation ($ per lb)", loc="left", fontsize=20,
                      fontweight="bold", color=INK, pad=7)
    for ax in axes:
        style(ax, PAPER, ts=16)
        ax.yaxis.set_major_locator(plt.MaxNLocator(3))
    axes[3].set_xticks([pd.Timestamp(f"{y}-01-01") for y in range(2012, 2027, 4)])
    axes[3].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    fig.tight_layout(pad=0.6, h_pad=1.0)
    save(fig, "chain_big.png", PAPER)


def dollar_stack(m):
    defl = m.loc[m["cpi_all_items"].last_valid_index(), "cpi_all_items"] / m["cpi_all_items"]
    parts = {"Rancher": "net_farm", "Packer": "spread_farm_to_wholesale", "Store": "spread_wholesale_to_retail"}
    yearly = pd.DataFrame({k: (m[f"ers_beef_{v}"] * defl / 100).groupby(m.index.year).mean()
                           for k, v in parts.items()}).loc[config.PRICE_START_YEAR:]
    fig, ax = plt.subplots(figsize=(9.8, 6.4))
    fig.patch.set_facecolor(ALT)
    bottom = np.zeros(len(yearly))
    for name, col in [("Rancher", RANCH), ("Packer", PACK), ("Store", STORE)]:
        v = yearly[name].clip(lower=0).values
        ax.bar(yearly.index, v, bottom=bottom, color=col, width=0.72, label=name, zorder=3)
        bottom += v
    for x, t in zip(yearly.index, bottom):
        ax.annotate(f"${t:.2f}", (x, t), xytext=(0, 8), textcoords="offset points", ha="center",
                    fontsize=14, color=MUTED)
    ax.set_xticks(list(yearly.index))
    ax.tick_params(axis="x", labelsize=14, rotation=45)
    ax.yaxis.set_major_formatter(lambda x, _: f"${x:.0f}")
    ax.legend(frameon=False, fontsize=17, loc="upper left", labelcolor=INK, ncols=3)
    style(ax, ALT)
    ax.grid(axis="x", alpha=0)
    fig.tight_layout(pad=0.6)
    save(fig, "dollar_stack.png", ALT)


def cover_bg(m):
    fig, ax = plt.subplots(figsize=(19.2, 10.8))
    fig.patch.set_facecolor(INK)
    ax.set_facecolor(INK)
    s = m["beef_price_real"].dropna().loc["2010":]
    for lw, a in [(22, 0.10), (12, 0.18), (5.5, 0.75)]:
        ax.plot(s.index, s, color=BEEF, lw=lw, alpha=a, solid_capstyle="round")
    ax.set_ylim(s.min() * 0.96, s.max() * 1.04)
    ax.axis("off")
    fig.subplots_adjust(left=-0.02, right=1.02, bottom=0.04, top=0.46)
    save(fig, "cover_bg.png", INK)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    m = pd.read_csv(config.PROCESSED_DIR / "master_monthly.csv", parse_dates=["date"]).set_index("date")
    p = m.loc[str(config.PRICE_START_YEAR):]
    print("Presentation charts:")
    hero(p)
    bars(m, p)
    minis(p)
    events_dots()
    chain(m)
    dollar_stack(m)
    cover_bg(m)
    print(f"Saved to {OUT.relative_to(config.PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
