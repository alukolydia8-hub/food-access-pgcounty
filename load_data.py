"""
load_data.py
------------
Loads and cleans the USDA Food Access Research Atlas (FARA) census-tract
data, filtered down to Prince George's County, MD.

WHERE TO GET THE FILE (2 minutes, do this once):
  1. Go to: https://www.ers.usda.gov/data-products/food-access-research-atlas
  2. Click "Download the Data" -> download the current "Food Access
     Research Atlas Data" spreadsheet (it's one workbook, ~15-20MB,
     national coverage, sheet name usually "Food Access Research Atlas").
  3. Save it as data/food_access_atlas.xlsx (or .csv if you export the
     sheet to CSV) in this project's /data folder.

The national file is fine to keep whole -- this script filters it down
to just Prince George's County (State='MD', County='Prince George's')
so everything downstream stays small and fast.
"""

import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Column names as they appear in the official FARA data dictionary.
# (If USDA tweaks column names in a future release, adjust this list.)
KEEP_COLS = [
    "CensusTract", "State", "County", "Urban", "Pop2010",
    "OHU2010",                # occupied housing units
    "GroupQuartersFlag",
    "NUMGQTRS",
    "PCTGQTRS",
    "LILATracts_1And10",      # low income + low access (1mi urban/10mi rural)
    "LILATracts_halfAnd10",
    "LILATracts_1And20",
    "LILATracts_Vehicle",
    "LATracts1", "LATracts10", "LATracts20", "LATractsVehicle_20",
    "LowIncomeTracts",
    "PovertyRate",
    "MedianFamilyIncome",
    "LA1and10",
    "TractLOWI",               # count of low-income people in tract
    "TractKids",
    "TractSeniors",
    "TractWhite", "TractBlack", "TractAsian", "TractNHOPI",
    "TractAIAN", "TractOMultir", "TractHispanic",
    "TractHUNV",                # housing units, no vehicle
    "TractSNAP",
]


def load_fara(filename: str = "food_access_atlas.xlsx") -> pd.DataFrame:
    """Load the raw national FARA file (xlsx or csv)."""
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(
            f"Couldn't find {path}.\n"
            "Download the FARA workbook from "
            "https://www.ers.usda.gov/data-products/food-access-research-atlas "
            "and save it into the data/ folder (see docstring at top of this file)."
        )

    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    else:
        # The official workbook usually names the data sheet this way;
        # fall back to the first sheet if the name has changed.
        try:
            df = pd.read_excel(path, sheet_name="Food Access Research Atlas")
        except ValueError:
            df = pd.read_excel(path, sheet_name=0)
    return df


def filter_to_county(df: pd.DataFrame, state: str = "MD",
                      county: str = "Prince George's County") -> pd.DataFrame:
    """Filter the national dataset down to one county."""
    out = df[(df["State"] == state) & (df["County"] == county)].copy()
    available = [c for c in KEEP_COLS if c in out.columns]
    out = out[available]

    # Derived, easier-to-read fields
    if "TractLOWI" in out.columns and "Pop2010" in out.columns:
        out["pct_low_income"] = (out["TractLOWI"] / out["Pop2010"] * 100).round(1)
    if "TractHUNV" in out.columns and "OHU2010" in out.columns:
        out["pct_no_vehicle"] = (out["TractHUNV"] / out["OHU2010"] * 100).round(1)
    if "TractSNAP" in out.columns and "OHU2010" in out.columns:
        out["pct_snap"] = (out["TractSNAP"] / out["OHU2010"] * 100).round(1)

    return out.reset_index(drop=True)


def save_clean(df: pd.DataFrame, filename: str = "pgcounty_food_access_clean.csv"):
    out_path = DATA_DIR / filename
    df.to_csv(out_path, index=False)
    print(f"Saved cleaned data -> {out_path} ({len(df)} tracts)")
    return out_path


if __name__ == "__main__":
    raw = load_fara()
    clean = filter_to_county(raw)
    save_clean(clean)
    print(clean.head())
