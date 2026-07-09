# Guy-anchor clearance overlay

A **planning** tool that renders a translucent heat map showing where the mast base can
stand so that **all guy anchors stay on your property**. Output is a KMZ ground overlay
you drop onto the satellite layer in Google Earth.

```yaml
# This TOOL (script + this README):
classification:
  visibility: public-safe
  geospatial_sensitivity: none
  contains_real_coordinates: false
  safe_for_public_repo: true

# The KMZ it PRODUCES from a real parcel:
classification:
  visibility: private
  geospatial_sensitivity: high
  contains_real_coordinates: true
  contains_real_parcel_geometry: true
  safe_for_public_repo: false        # never publish it — not even a thumbnail
```

## What the heat map means

For every candidate mast-base point inside your property:

```
margin = distance(base → nearest property line) − guy_anchor_radius
```

| Color | Meaning |
|-------|---------|
| **Green** | Guys land well inside your line — roomy. |
| **Yellow** | Tight — a guy anchor sits close to the boundary. |
| **Red** | Infeasible — at least one guy anchor crosses **off** your property. |
| **Dark contour** | `margin = 0`: the **must-not-cross line for the base**. Keep the base on the green side of it. |

The red band is a `guy_anchor_radius`-wide keep-out around the whole boundary. Aim the
mast for the greenest spot in your target zone (e.g. between the willow and birch).

## Assumptions & limits (read these)

- **Radius model:** feasibility assumes the guy circle can point any direction (base must
  be ≥ radius from *every* line). This is the conservative, direction-independent answer.
  If your guy bearings are fixed by obstacles, the real feasible area may be a bit larger.
- **`guy_anchor_radius` default = 40 ft** (80% of the 50-ft mast). Change with
  `--guy-radius-ft`. This number should come from the actual guy engineering — confirm it
  with the `grounding-safety-inspector` / `rf-antenna-engineer`.
- **Not survey data.** GIS/aerial parcel geometry is *not* construction-grade. This tool
  narrows down *where to look*; every guy-anchor position is **field-verified before you
  dig**. Utility locate still required (see `checklists/pre-dig.md`).
- The parcel input must contain a **polygon** boundary (not just a pin).

## Usage

Requires `python3`, `numpy`, `pillow`.

**Keep the real parcel input and the KMZ output under `private/`** (git-ignored — real
coordinates never enter the public repo):

```bash
python3 tools/placement-overlay/generate_overlay.py \
    --parcel private/geospatial/parcel.kmz \
    --guy-radius-ft 40 \
    --out    private/site-planning/guy-clearance-overlay.kmz \
    --marker willow --marker birch      # optional: relabel point pins carried from the parcel
```

Then in Google Earth: **File → Open →** the KMZ. It draws over the satellite imagery with
the legend pinned bottom-left. Toggle its opacity with the layer's transparency slider.

**Self-test with a synthetic parcel** (no real data — safe to run anywhere):

```bash
python3 tools/placement-overlay/generate_overlay.py --demo --out /tmp/demo-overlay.kmz
```

## Getting the parcel boundary

Accepted inputs: `.kml`, `.kmz`, `.geojson`, `.json` (GeoJSON **or** Esri JSON). Save into
`private/geospatial/` (git-ignored).

**If the county has an export button:** select your parcel → export to KML/KMZ → save.

**If it doesn't (common):** pull it from the county's ArcGIS REST API. The map viewers are
front-ends to an ArcGIS Server, and any parcel layer that supports *Query* will return one
parcel as GeoJSON. General shape:

```
<layer-url>/query
    ?where=<PARCEL_FIELD>='<YOUR_PARCEL_NUMBER>'
    &outFields=<PARCEL_FIELD>
    &returnGeometry=true
    &outSR=4326          # <- WGS84 lon/lat, required for Google Earth + this tool
    &f=geojson           # <- fall back to f=json (Esri rings); the tool reads both
```

Find `<layer-url>` by browsing `.../arcgis/rest/services` for a parcels layer, and get
`<YOUR_PARCEL_NUMBER>` by clicking your lot in the county's web map. Save the response as
`private/geospatial/parcel.geojson`.

**Last resort (always works):** read the boundary in the county viewer, trace it in Google
Earth (Add → Polygon), and save the KMZ.
