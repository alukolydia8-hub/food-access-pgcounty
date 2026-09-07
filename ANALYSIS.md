# Mapping Food Access in Prince George's County, MD

*Lydia Aluko*

## 1. Why Prince George's County

Food insecurity is not evenly distributed across Maryland. About 17%
of the state's entire food-insecure population is concentrated in
Prince George's County, and roughly one in seven county residents is
affected. The most food-insecure zip code in Maryland, 20743
(Capitol Heights, Fairmount Heights, Walker Mill, Seat Pleasant,
Coral Hills, and Pepper Mill Village), sits within the county. These
disparities carry health consequences: county-wide child obesity
runs above 16%, one of several downstream effects linked to limited
access to affordable, healthy food.[^1]

Existing county reporting also points to something more specific
than "no grocery stores nearby": in the areas inside the Capital
Beltway, the challenge is often the mix of available food (cheap,
processed options are abundant; healthy options are pricier and
farther away) rather than a total absence of retailers.[^2] This
project uses census-tract-level USDA data to see where, specifically,
low income and low food access overlap in the county, and where kids,
seniors, and no-vehicle households are most exposed.

## 2. Data and method

- **USDA Food Access Research Atlas (FARA)**, census-tract level,
  filtered to Prince George's County, MD
- **Census tract boundaries**, U.S. Census Bureau TIGER/Line
- Analysis in Python (pandas for cleaning/aggregation, matplotlib for
  charts, folium for the interactive map)
- Low-access tracts identified using USDA's standard flag: low-income
  tract AND a meaningful share of residents living beyond 1 mile
  (urban) / 10 miles (rural) from the nearest supermarket

*(Full pipeline: `src/load_data.py` -> `src/analyze.py` -> `src/make_map.py`)*

## 3. Findings

> Fill in after running `src/analyze.py` — the numbers below are the
> exact fields `outputs/summary_stats.txt` will give you. Suggested
> structure:

- **Scale:** [X] of the county's [Y] census tracts are flagged
  low-income and low food access — [Z]% of tracts.
- **Who's affected:** an estimated [X] children and [Y] seniors live
  in these flagged tracts.
- **Vehicle access:** flagged tracts have a [higher/similar] share of
  households without a vehicle compared to non-flagged tracts,
  meaning distance to a store compounds with the ability to get there.
- **Geographic pattern:** [describe what the choropleth map shows —
  e.g., clustering inside the Beltway, near/around zip 20743, etc.]
- **SNAP participation:** the tracts with the highest SNAP
  participation are [list top few] — cross-reference against the
  low-access flag to see how much overlap exists.

## 4. Recommendations

> Ground these in what your own map/charts actually show. Starting
> points based on county reporting:

1. **Target mobile markets / pop-up produce stands** at the highest
   low-access + no-vehicle tracts identified in the map, prioritizing
   locations near existing food pantries (see `README.md` links) to
   share transportation and outreach infrastructure.
2. **Coordinate with the county's Food Equity Council** and existing
   Food Desert Relief Plan work rather than duplicating it — point to
   the specific tracts this analysis flags as under-served by current
   pantry/market locations.
3. **Prioritize the 20743 corridor** given its documented status as
   the most food-insecure zip code in the state, unless the tract data
   shows an even higher-need area within the county.

## 5. Limitations

- FARA measures *distance* to supermarkets, not food *affordability*
  or *quality* — county reporting suggests the more specific problem
  inside the Beltway is the mix of what's available, not just distance.
- Census tract data is from the most recent FARA release, not
  real-time; store openings/closures since then won't be reflected.
- This is a first pass for a summer project, not a peer-reviewed
  study — frame recommendations as starting points for a community
  partner conversation, not final policy proposals.

---

[^1]: Maryland Matters, "Opinion: It's Time for Md. Leaders to Address
Food Insecurity," July 2022.
[^2]: Prince George's County Planning Department, "Healthy Food for
All Prince Georgians" (2015), as summarized by the Healthy Food
Policy Project.
