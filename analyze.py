"""
analyze.py
----------
Generates the core visualizations and summary numbers for the write-up
and presentation, from the cleaned Prince George's County FARA data.

Run after load_data.py:
    python src/load_data.py
    python src/analyze.py
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data" / "pgcounty_food_access_clean.csv"
FIG_DIR = BASE / "figures"
OUT_DIR = BASE / "outputs"

plt.rcParams["figure.dpi"] = 140


def load():
    if not DATA.exists():
        raise FileNotFoundError(
            f"{DATA} not found -- run `python src/load_data.py` first."
        )
    return pd.read_csv(DATA)


def chart_low_access_share(df):
    """Bar chart: how many tracts are flagged low-income + low-access."""
    flag_cols = [c for c in
                 ["LILATracts_1And10", "LILATracts_halfAnd10",
                  "LILATracts_1And20", "LILATracts_Vehicle"]
                 if c in df.columns]
    counts = df[flag_cols].sum()
    labels = {
        "LILATracts_1And10": "1mi urban /\n10mi rural",
        "LILATracts_halfAnd10": "0.5mi urban /\n10mi rural",
        "LILATracts_1And20": "1mi urban /\n20mi rural",
        "LILATracts_Vehicle": "Vehicle access\nmeasure",
    }
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar([labels[c] for c in flag_cols], counts.values, color="#2f6f4f")
    ax.set_ylabel("Number of census tracts")
    ax.set_title("Prince George's County: Tracts Flagged Low-Income\n"
                  "& Low Food Access, by Distance Measure")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "01_low_access_tract_counts.png")
    plt.close(fig)


def chart_poverty_vs_access(df):
    """Scatter: poverty rate vs. no-vehicle % , colored by low-access flag."""
    if not {"PovertyRate", "pct_no_vehicle"}.issubset(df.columns):
        return
    flag_col = "LILATracts_1And10" if "LILATracts_1And10" in df.columns else None
    fig, ax = plt.subplots(figsize=(6, 5))
    if flag_col:
        colors = df[flag_col].map({1: "#c0392b", 0: "#7f8c8d"})
    else:
        colors = "#2f6f4f"
    ax.scatter(df["PovertyRate"], df["pct_no_vehicle"], c=colors, alpha=0.8, s=60)
    ax.set_xlabel("Poverty rate (%)")
    ax.set_ylabel("Households with no vehicle (%)")
    ax.set_title("Poverty Rate vs. Vehicle Access by Census Tract\n"
                  "(red = flagged low-income & low food access)")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "02_poverty_vs_vehicle_access.png")
    plt.close(fig)


def chart_snap_by_tract(df):
    """Horizontal bar: top 10 tracts by SNAP participation share."""
    if "pct_snap" not in df.columns:
        return
    top = df.sort_values("pct_snap", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.barh(top["CensusTract"].astype(str), top["pct_snap"], color="#2f6f4f")
    ax.invert_yaxis()
    ax.set_xlabel("Households receiving SNAP (%)")
    ax.set_title("Top 10 Census Tracts by SNAP Participation Rate")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "03_top10_snap_tracts.png")
    plt.close(fig)


def chart_kids_seniors_exposure(df):
    """Stacked bar: kids vs. seniors living in low-access tracts."""
    flag_col = "LILATracts_1And10" if "LILATracts_1And10" in df.columns else None
    if not flag_col or not {"TractKids", "TractSeniors"}.issubset(df.columns):
        return
    grouped = df.groupby(flag_col)[["TractKids", "TractSeniors"]].sum()
    grouped.index = ["Not flagged", "Low-access tract"] if len(grouped) == 2 else grouped.index
    fig, ax = plt.subplots(figsize=(6, 4))
    grouped.plot(kind="bar", stacked=True, ax=ax, color=["#3498db", "#e67e22"])
    ax.set_ylabel("Number of people")
    ax.set_title("Kids & Seniors Living in Low-Access\nvs. Non-Flagged Tracts")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    fig.tight_layout()
    fig.savefig(FIG_DIR / "04_kids_seniors_exposure.png")
    plt.close(fig)


def write_summary(df):
    """Write a plain-text summary of headline numbers for the report."""
    lines = []
    lines.append(f"Total census tracts analyzed: {len(df)}")
    if "LILATracts_1And10" in df.columns:
        n_flagged = int(df["LILATracts_1And10"].sum())
        pct = round(n_flagged / len(df) * 100, 1)
        lines.append(f"Tracts flagged low-income & low-access (1mi/10mi): "
                      f"{n_flagged} ({pct}% of tracts)")
    if "TractLOWI" in df.columns:
        lines.append(f"Total low-income residents across all tracts: "
                      f"{int(df['TractLOWI'].sum()):,}")
    if "TractHUNV" in df.columns:
        lines.append(f"Total housing units with no vehicle: "
                      f"{int(df['TractHUNV'].sum()):,}")
    if "PovertyRate" in df.columns:
        lines.append(f"Average tract poverty rate: "
                      f"{df['PovertyRate'].mean():.1f}%")
    if "TractKids" in df.columns and "LILATracts_1And10" in df.columns:
        kids_exposed = int(df.loc[df["LILATracts_1And10"] == 1, "TractKids"].sum())
        lines.append(f"Children living in flagged low-access tracts: {kids_exposed:,}")

    out_path = OUT_DIR / "summary_stats.txt"
    out_path.write_text("\n".join(lines))
    print("\n".join(lines))
    print(f"\nSaved -> {out_path}")


if __name__ == "__main__":
    df = load()
    chart_low_access_share(df)
    chart_poverty_vs_access(df)
    chart_snap_by_tract(df)
    chart_kids_seniors_exposure(df)
    write_summary(df)
    print(f"\nFigures saved to {FIG_DIR}")
