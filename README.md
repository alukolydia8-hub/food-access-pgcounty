# Mapping Food Access in Prince George's County, MD

A data-driven look at food insecurity and low-access census tracts in
Prince George's County, built with USDA and Census data, for the
Seeds of Tomorrow community project.

## Why this matters here
About 17% of Maryland's entire food-insecure population lives in
Prince George's County, and roughly one in seven county residents is
affected by food insecurity. The most food-insecure zip code in the
state, 20743 (Capitol Heights / Fairmount Heights / Seat Pleasant /
Coral Hills), is right here in the county. Child obesity in the
county runs over 16%, a downstream effect of limited access to
affordable, healthy food. *(Sources in ANALYSIS.md.)*

## One-day build plan
| Time | Task |
|---|---|
| Hour 1 | Download FARA data (state-filtered) + Census tract boundaries (links below) |
| Hour 2 | Run `src/load_data.py` to clean + filter to Prince George's County |
| Hour 3-4 | Run `src/analyze.py` for the 4 charts + summary stats |
| Hour 5 | Run `src/make_map.py` for the interactive choropleth |
| Hour 6-7 | Fill in `ANALYSIS.md` with your own numbers (template + real county context already written) |
| Hour 8 | Turn `presentation/OUTLINE.md` into slides |

## Setup
```bash
pip install -r requirements.txt
```

## Get the data (do this first, ~10 minutes total)

**1. USDA Food Access Research Atlas** (the core dataset)
- https://www.ers.usda.gov/data-products/food-access-research-atlas
- Click "Download the Data," get the current workbook
- Save as `data/food_access_atlas.xlsx`

**2. Census tract boundaries** (for the map only)
- https://www.census.gov/cgi-bin/geo/shapefiles/index.php -> Census Tracts -> Maryland
- Convert to GeoJSON at https://mapshaper.org, filter to `COUNTYFP == "033"`
  (Prince George's County's FIPS code)
- Save as `data/pgcounty_tracts.geojson`

**3. (Optional, for extra depth) PG County open data + ACS**
- https://data.princegeorgescountymd.gov
- https://data.census.gov -- American Community Survey, food stamp
  (SNAP) and poverty tables, Prince George's County, MD

## Run it
```bash
python src/load_data.py     # -> data/pgcounty_food_access_clean.csv
python src/analyze.py       # -> figures/*.png, outputs/summary_stats.txt
python src/make_map.py      # -> outputs/pgcounty_food_access_map.html
```

## What's in this repo
```
src/load_data.py     Cleans + filters the national FARA file to PG County
src/analyze.py       4 charts + headline summary stats
src/make_map.py      Interactive folium choropleth map
ANALYSIS.md           1-2 page write-up template, pre-loaded with county context
presentation/OUTLINE.md   Slide-by-slide outline for a community presentation
```


