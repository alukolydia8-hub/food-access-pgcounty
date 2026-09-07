"""
make_map.py
-----------
Builds an interactive choropleth map of low-access census tracts in
Prince George's County using folium.

Needs a census tract boundary file (GeoJSON) in addition to the FARA
data, since FARA itself has no geometry.

WHERE TO GET TRACT BOUNDARIES (2 minutes):
  Option A (easiest): Census Bureau TIGER/Line Shapefiles
    https://www.census.gov/cgi-bin/geo/shapefiles/index.php
    -> Year: 2020ish -> Layer type: "Census Tracts" -> State: Maryland
    Download, then convert to GeoJSON at https://mapshaper.org (drag
    the .shp+.dbf+.shx files in, export as GeoJSON), filtered to
    Prince George's County (COUNTYFP = "033").
  Option B: Maryland's open data portal (data.maryland.gov) often has
    a ready-made Census Tract GeoJSON layer you can filter/export directly.

Save the result as data/pgcounty_tracts.geojson

Run after analyze.py has produced data/pgcounty_food_access_clean.csv:
    python src/make_map.py
"""

import json
import pandas as pd
import folium
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA_CSV = BASE / "data" / "pgcounty_food_access_clean.csv"
GEOJSON = BASE / "data" / "pgcounty_tracts.geojson"
OUT_HTML = BASE / "outputs" / "pgcounty_food_access_map.html"

PG_COUNTY_CENTER = [38.8, -76.8]  # rough centroid, good enough for map init


def build_map():
    if not DATA_CSV.exists():
        raise FileNotFoundError("Run src/load_data.py first.")
    if not GEOJSON.exists():
        raise FileNotFoundError(
            f"{GEOJSON} not found. See the docstring in this file for how "
            "to get census tract boundaries and save them there."
        )

    df = pd.read_csv(DATA_CSV, dtype={"CensusTract": str})
    with open(GEOJSON) as f:
        geo = json.load(f)

    m = folium.Map(location=PG_COUNTY_CENTER, zoom_start=11, tiles="cartodbpositron")

    value_col = "pct_low_income" if "pct_low_income" in df.columns else "PovertyRate"

    folium.Choropleth(
        geo_data=geo,
        data=df,
        columns=["CensusTract", value_col],
        key_on="feature.properties.GEOID",  # adjust if your GeoJSON uses a different key
        fill_color="YlOrRd",
        fill_opacity=0.75,
        line_opacity=0.3,
        legend_name=f"{value_col.replace('_', ' ').title()} by Census Tract",
    ).add_to(m)

    # tooltip layer with tract-level detail
    lookup = df.set_index("CensusTract").to_dict("index")
    for feature in geo["features"]:
        geoid = feature["properties"].get("GEOID")
        row = lookup.get(geoid)
        if row:
            tip = (f"Tract {geoid}<br>"
                   f"Poverty rate: {row.get('PovertyRate', 'n/a')}%<br>"
                   f"No vehicle: {row.get('pct_no_vehicle', 'n/a')}%<br>"
                   f"SNAP: {row.get('pct_snap', 'n/a')}%")
            folium.GeoJson(
                feature,
                style_function=lambda x: {"fillOpacity": 0, "weight": 0},
                tooltip=tip,
            ).add_to(m)

    m.save(str(OUT_HTML))
    print(f"Map saved -> {OUT_HTML}")


if __name__ == "__main__":
    build_map()
