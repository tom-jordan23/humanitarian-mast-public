#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# classification:
#   visibility: public-safe          # THIS TOOL is public-safe (no coordinates)
#   geospatial_sensitivity: none     # ...but its OUTPUT is private/high — see below
#   contains_real_coordinates: false
#   contains_real_parcel_geometry: false
#   contains_identifiable_imagery: false
#   safe_for_public_repo: true
#
#   NOTE: The KMZ this script PRODUCES from a real parcel is
#   visibility: private, geospatial_sensitivity: high, safe_for_public_repo: false.
#   Write outputs only under private/ (git-ignored). Never publish them.
# ---------------------------------------------------------------------------
"""
Guy-anchor clearance heat-map overlay generator.

Given a property boundary (KML/KMZ parcel) and a guy-anchor radius, this renders a
translucent "clearance-margin" heat map as a KMZ ground overlay you can open in
Google Earth on top of the satellite layer.

The field it renders, per candidate mast-base point (x, y) inside the property:

    margin(x, y) = distance(base -> nearest property line) - guy_anchor_radius

  * margin >= 0  : a full guy circle of the given radius fits INSIDE your line
                   (guys can point any direction and stay on-property)
  * margin  < 0  : at least one guy anchor would cross OFF your property
  * a dark contour marks margin == 0 (the must-not-cross line for the base)

This is a PLANNING tool, not survey data. GIS/aerial parcel geometry is not
construction-grade. Field-verify every guy-anchor position before you dig.

Dependencies: numpy, Pillow (only). Pure-numpy geometry — no shapely/GDAL, so it
rebuilds from commonly available parts in the field.

Usage:
    # Real run (keep input + output under private/, which is git-ignored):
    python3 generate_overlay.py \
        --parcel   private/geospatial/parcel.kmz \
        --guy-radius-ft 40 \
        --out      private/site-planning/guy-clearance-overlay.kmz \
        --marker "willow" --marker "birch"      # optional labels for point placemarks in the KMZ

    # Self-test with a SYNTHETIC parcel (no real data needed):
    python3 generate_overlay.py --demo --out /tmp/demo-overlay.kmz
"""

import argparse
import json
import math
import os
import sys
import zipfile
import xml.etree.ElementTree as ET

import numpy as np
from PIL import Image, ImageDraw, ImageFont

FT_PER_M = 3.280839895


# --------------------------------------------------------------------------- #
# KML / KMZ parsing
# --------------------------------------------------------------------------- #
def _strip_ns(tag):
    return tag.split("}", 1)[-1] if "}" in tag else tag


def _parse_coord_string(text):
    """KML coordinate string -> list of (lon, lat)."""
    pts = []
    for tok in text.replace("\n", " ").split():
        parts = tok.split(",")
        if len(parts) >= 2:
            pts.append((float(parts[0]), float(parts[1])))
    return pts


def read_kml_bytes(path):
    """Return raw KML text from a .kml or .kmz file."""
    if path.lower().endswith(".kmz"):
        with zipfile.ZipFile(path) as zf:
            # KMZ convention: the root doc is doc.kml, else first *.kml
            names = zf.namelist()
            kml_name = next((n for n in names if n.lower() == "doc.kml"),
                            next((n for n in names if n.lower().endswith(".kml")), None))
            if kml_name is None:
                raise ValueError(f"No .kml found inside {path}")
            return zf.read(kml_name).decode("utf-8")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extract_polygon_and_points(kml_text):
    """
    Return (polygon, points) where:
      polygon = list of (lon, lat) for the LARGEST polygon outer boundary found
      points  = list of (lon, lat, name) for Point placemarks
    """
    root = ET.fromstring(kml_text)
    polygons = []
    points = []

    # Walk placemarks so we can capture names for point markers.
    for pm in root.iter():
        if _strip_ns(pm.tag) != "Placemark":
            continue
        name = None
        for ch in pm:
            if _strip_ns(ch.tag) == "name":
                name = (ch.text or "").strip()
        for node in pm.iter():
            t = _strip_ns(node.tag)
            if t == "Point":
                for c in node.iter():
                    if _strip_ns(c.tag) == "coordinates" and c.text:
                        cc = _parse_coord_string(c.text)
                        if cc:
                            points.append((cc[0][0], cc[0][1], name or "point"))

    # Polygons: grab every outerBoundaryIs/LinearRing coordinates block.
    for poly in root.iter():
        if _strip_ns(poly.tag) != "Polygon":
            continue
        for ob in poly.iter():
            if _strip_ns(ob.tag) != "outerBoundaryIs":
                continue
            for c in ob.iter():
                if _strip_ns(c.tag) == "coordinates" and c.text:
                    ring = _parse_coord_string(c.text)
                    if len(ring) >= 3:
                        polygons.append(ring)

    if not polygons:
        raise ValueError("No <Polygon> outer boundary found in KML/KMZ. "
                         "Draw the parcel as a polygon and re-export.")

    # If several polygons, keep the one with the largest lon/lat bbox area.
    def bbox_area(ring):
        lons = [p[0] for p in ring]
        lats = [p[1] for p in ring]
        return (max(lons) - min(lons)) * (max(lats) - min(lats))

    polygon = max(polygons, key=bbox_area)
    return polygon, points


def extract_from_geojson(text):
    """
    Parse GeoJSON *or* Esri JSON (what an ArcGIS REST .../query?f=geojson|json returns).
    Returns (polygon, points): the largest Polygon outer ring as [(lon,lat), ...] plus
    any Point features as (lon, lat, name). Coordinates must be lon/lat (request the
    ArcGIS query with outSR=4326).
    """
    data = json.loads(text)
    polygons = []
    points = []

    def name_of(props):
        if isinstance(props, dict):
            for k in ("name", "NAME", "Name", "label", "LABEL"):
                if props.get(k):
                    return str(props[k])
        return None

    def handle(geom, nm=None):
        if not isinstance(geom, dict):
            return
        if "rings" in geom:                       # Esri JSON polygon
            for ring in geom["rings"]:
                if len(ring) >= 3:
                    polygons.append([(p[0], p[1]) for p in ring])
        elif "x" in geom and "y" in geom:         # Esri JSON point
            points.append((geom["x"], geom["y"], nm or "point"))
        else:                                      # GeoJSON geometry
            gt, co = geom.get("type"), geom.get("coordinates")
            if gt == "Polygon" and co:
                polygons.append([(p[0], p[1]) for p in co[0]])
            elif gt == "MultiPolygon" and co:
                for poly in co:
                    if poly:
                        polygons.append([(p[0], p[1]) for p in poly[0]])
            elif gt == "Point" and co:
                points.append((co[0], co[1], nm or "point"))

    if data.get("type") == "FeatureCollection":
        for f in data.get("features", []):
            handle(f.get("geometry"), name_of(f.get("properties")))
    elif data.get("type") == "Feature":
        handle(data.get("geometry"), name_of(data.get("properties")))
    elif "features" in data:                       # Esri JSON FeatureSet
        for f in data["features"]:
            handle(f.get("geometry"), name_of(f.get("attributes")))
    else:                                          # bare geometry
        handle(data)

    if not polygons:
        raise ValueError("No polygon geometry found in GeoJSON/JSON. If this came from an "
                         "ArcGIS query, confirm returnGeometry=true and the parcel matched.")

    def bbox_area(ring):
        lons = [p[0] for p in ring]
        lats = [p[1] for p in ring]
        return (max(lons) - min(lons)) * (max(lats) - min(lats))

    return max(polygons, key=bbox_area), points


def load_geometry(path):
    """Dispatch on file extension -> (polygon, points)."""
    lower = path.lower()
    if lower.endswith((".kml", ".kmz")):
        return extract_polygon_and_points(read_kml_bytes(path))
    if lower.endswith((".geojson", ".json")):
        with open(path, "r", encoding="utf-8") as f:
            return extract_from_geojson(f.read())
    raise ValueError(f"Unsupported input '{path}'. Use .kml/.kmz/.geojson/.json")


# --------------------------------------------------------------------------- #
# Local ENU projection (equirectangular around parcel centroid)
# --------------------------------------------------------------------------- #
def make_projector(lon0, lat0):
    m_per_deg_lat = 110540.0
    m_per_deg_lon = 111320.0 * math.cos(math.radians(lat0))

    def to_m(lon, lat):
        x = (np.asarray(lon) - lon0) * m_per_deg_lon
        y = (np.asarray(lat) - lat0) * m_per_deg_lat
        return x, y

    return to_m


# --------------------------------------------------------------------------- #
# Vectorized geometry (pure numpy)
# --------------------------------------------------------------------------- #
def point_in_polygon(px, py, poly_x, poly_y):
    """Ray-casting PIP for arrays px, py against a closed polygon. Returns bool array."""
    inside = np.zeros(px.shape, dtype=bool)
    n = len(poly_x)
    j = n - 1
    for i in range(n):
        xi, yi = poly_x[i], poly_y[i]
        xj, yj = poly_x[j], poly_y[j]
        cond = ((yi > py) != (yj > py))
        # avoid divide-by-zero on horizontal edges
        denom = np.where((yj - yi) == 0, 1e-12, (yj - yi))
        xints = (xj - xi) * (py - yi) / denom + xi
        inside ^= cond & (px < xints)
        j = i
    return inside


def dist_to_boundary(px, py, poly_x, poly_y):
    """Min distance (meters) from each (px,py) to the polygon boundary segments."""
    best = np.full(px.shape, np.inf)
    n = len(poly_x)
    for i in range(n):
        ax, ay = poly_x[i], poly_y[i]
        bx, by = poly_x[(i + 1) % n], poly_y[(i + 1) % n]
        abx, aby = bx - ax, by - ay
        ab2 = abx * abx + aby * aby
        if ab2 == 0:
            continue
        t = ((px - ax) * abx + (py - ay) * aby) / ab2
        t = np.clip(t, 0.0, 1.0)
        cx, cy = ax + t * abx, ay + t * aby
        d = np.hypot(px - cx, py - cy)
        best = np.minimum(best, d)
    return best


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #
def render_overlay(polygon, guy_radius_ft, long_px=1200, pad_frac=0.06):
    lons = np.array([p[0] for p in polygon])
    lats = np.array([p[1] for p in polygon])
    lon0, lat0 = float(lons.mean()), float(lats.mean())
    to_m = make_projector(lon0, lat0)

    # Bounding box in lon/lat with padding
    west, east = lons.min(), lons.max()
    south, north = lats.min(), lats.max()
    dlon = (east - west) * pad_frac
    dlat = (north - south) * pad_frac
    west, east = west - dlon, east + dlon
    south, north = south - dlat, north + dlat

    # Pixel grid; long side = long_px
    span_lon = east - west
    span_lat = north - south
    if span_lon >= span_lat:
        W = long_px
        H = max(2, int(round(long_px * span_lat / span_lon)))
    else:
        H = long_px
        W = max(2, int(round(long_px * span_lon / span_lat)))

    grid_lon = np.linspace(west, east, W)
    grid_lat = np.linspace(north, south, H)   # row 0 = north (KML image convention)
    GX_lon, GY_lat = np.meshgrid(grid_lon, grid_lat)

    gx_m, gy_m = to_m(GX_lon, GY_lat)
    px_m, py_m = to_m(lons, lats)

    inside = point_in_polygon(gx_m, gy_m, px_m, py_m)
    dbound_m = dist_to_boundary(gx_m, gy_m, px_m, py_m)
    dbound_ft = dbound_m * FT_PER_M

    margin_ft = dbound_ft - guy_radius_ft   # only meaningful where inside

    rgba = np.zeros((H, W, 4), dtype=np.uint8)

    feasible = inside & (margin_ft >= 0)
    infeasible = inside & (margin_ft < 0)

    # Feasible: yellow (tight) -> green (roomy)
    if feasible.any():
        mmax = max(float(margin_ft[feasible].max()), 1.0)
        t = np.clip(margin_ft / mmax, 0.0, 1.0)
        R = (255 * (1 - t)).astype(np.uint8)
        G = (220 - 60 * t).astype(np.uint8)
        B = (60 * t).astype(np.uint8)
        rgba[..., 0] = np.where(feasible, R, rgba[..., 0])
        rgba[..., 1] = np.where(feasible, G, rgba[..., 1])
        rgba[..., 2] = np.where(feasible, B, rgba[..., 2])
        rgba[..., 3] = np.where(feasible, 150, rgba[..., 3])

    # Infeasible: red (deeper red the further off-property the guys reach)
    if infeasible.any():
        over = np.clip((-margin_ft) / max(guy_radius_ft, 1.0), 0.0, 1.0)
        rgba[..., 0] = np.where(infeasible, (210 - 40 * over).astype(np.uint8), rgba[..., 0])
        rgba[..., 1] = np.where(infeasible, (40 * (1 - over)).astype(np.uint8), rgba[..., 1])
        rgba[..., 2] = np.where(infeasible, (30 * (1 - over)).astype(np.uint8), rgba[..., 2])
        rgba[..., 3] = np.where(infeasible, 165, rgba[..., 3])

    # margin == 0 contour (must-not-cross line for the base): ~0.4 ft band, dark
    contour = inside & (np.abs(margin_ft) <= 0.4)
    rgba[contour] = (20, 20, 20, 220)

    img = Image.fromarray(rgba)

    # Draw the property boundary as a crisp line for reference.
    draw = ImageDraw.Draw(img)

    def to_px(lon, lat):
        x = (lon - west) / (east - west) * (W - 1)
        y = (north - lat) / (north - south) * (H - 1)
        return (x, y)

    ring_px = [to_px(lon, lat) for lon, lat in polygon]
    ring_px.append(ring_px[0])
    draw.line(ring_px, fill=(255, 255, 255, 255), width=3)
    draw.line(ring_px, fill=(0, 0, 0, 255), width=1)

    latlonbox = dict(north=north, south=south, east=east, west=west)
    stats = dict(
        feasible_px=int(feasible.sum()),
        infeasible_px=int(infeasible.sum()),
        max_margin_ft=float(margin_ft[feasible].max()) if feasible.any() else 0.0,
    )
    return img, latlonbox, stats


def render_legend(guy_radius_ft):
    W, H = 250, 150
    img = Image.new("RGBA", (W, H), (255, 255, 255, 210))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
    d.text((10, 8), f"Guy clearance (R = {guy_radius_ft:.0f} ft)", fill=(0, 0, 0, 255), font=font)
    rows = [
        ((0, 160, 60), "Roomy: guys well inside line"),
        ((255, 220, 0), "Tight: guys near the line"),
        ((210, 40, 30), "Off-property: guy crosses line"),
        ((20, 20, 20), "must-not-cross (base = R)"),
    ]
    y = 34
    for color, label in rows:
        d.rectangle([10, y, 30, y + 16], fill=color + (255,), outline=(0, 0, 0, 255))
        d.text((38, y + 3), label, fill=(0, 0, 0, 255), font=font)
        y += 26
    return img


# --------------------------------------------------------------------------- #
# KMZ writer
# --------------------------------------------------------------------------- #
def build_kml(latlonbox, points, guy_radius_ft):
    b = latlonbox
    placemarks = ""
    for lon, lat, name in points:
        placemarks += f"""
    <Placemark>
      <name>{_xml_escape(name)}</name>
      <Point><coordinates>{lon},{lat},0</coordinates></Point>
    </Placemark>"""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Guy-anchor clearance (R = {guy_radius_ft:.0f} ft)</name>
    <description><![CDATA[
      PRIVATE / geospatial_sensitivity: high. Do NOT publish.
      Green=guys well inside property line, yellow=tight, red=guy anchor off-property,
      dark contour=must-not-cross line for the mast base. Planning tool only —
      field-verify every guy-anchor position before digging.
    ]]></description>
    <GroundOverlay>
      <name>Clearance heat map</name>
      <color>ffffffff</color>
      <Icon><href>overlay.png</href></Icon>
      <LatLonBox>
        <north>{b['north']}</north>
        <south>{b['south']}</south>
        <east>{b['east']}</east>
        <west>{b['west']}</west>
        <rotation>0</rotation>
      </LatLonBox>
    </GroundOverlay>
    <ScreenOverlay>
      <name>Legend</name>
      <Icon><href>legend.png</href></Icon>
      <overlayXY x="0" y="0" xunits="fraction" yunits="fraction"/>
      <screenXY x="0.01" y="0.01" xunits="fraction" yunits="fraction"/>
      <size x="0" y="0" xunits="pixels" yunits="pixels"/>
    </ScreenOverlay>{placemarks}
  </Document>
</kml>
"""


def _xml_escape(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def write_kmz(out_path, kml_text, overlay_img, legend_img):
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    import io
    ov = io.BytesIO(); overlay_img.save(ov, format="PNG")
    lg = io.BytesIO(); legend_img.save(lg, format="PNG")
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("doc.kml", kml_text)
        zf.writestr("overlay.png", ov.getvalue())
        zf.writestr("legend.png", lg.getvalue())


# --------------------------------------------------------------------------- #
# Demo parcel (synthetic — NOT a real location)
# --------------------------------------------------------------------------- #
def demo_polygon():
    # Generic US-centroid area (approx.); an L-shaped ~120 x 90 m lot. Purely synthetic.
    lon0, lat0 = -98.5, 39.5
    m_lat = 110540.0
    m_lon = 111320.0 * math.cos(math.radians(lat0))
    # meters -> lon/lat
    def ll(xm, ym):
        return (lon0 + xm / m_lon, lat0 + ym / m_lat)
    pts_m = [(0, 0), (120, 0), (120, 55), (70, 55), (70, 90), (0, 90)]
    return [ll(x, y) for x, y in pts_m]


# --------------------------------------------------------------------------- #
def main(argv=None):
    ap = argparse.ArgumentParser(description="Guy-anchor clearance heat-map KMZ generator")
    ap.add_argument("--parcel", help="Path to parcel boundary: .kml/.kmz or .geojson/.json (private input)")
    ap.add_argument("--guy-radius-ft", type=float, default=40.0,
                    help="Horizontal guy-anchor radius in feet (default 40)")
    ap.add_argument("--out", required=True, help="Output .kmz path (write under private/)")
    ap.add_argument("--marker", action="append", default=[],
                    help="Rename carried-over point placemarks in order (e.g. --marker willow --marker birch)")
    ap.add_argument("--long-px", type=int, default=1200, help="Long-side resolution of the heat PNG")
    ap.add_argument("--demo", action="store_true", help="Use a synthetic parcel (no real data needed)")
    args = ap.parse_args(argv)

    if args.demo:
        polygon, points = demo_polygon(), []
    else:
        if not args.parcel:
            ap.error("--parcel is required unless --demo is given")
        polygon, points = load_geometry(args.parcel)

    # Apply user labels to carried-over point placemarks, in order.
    if args.marker and points:
        for i, label in enumerate(args.marker):
            if i < len(points):
                points[i] = (points[i][0], points[i][1], label)

    img, latlonbox, stats = render_overlay(polygon, args.guy_radius_ft, long_px=args.long_px)
    legend = render_legend(args.guy_radius_ft)
    kml_text = build_kml(latlonbox, points, args.guy_radius_ft)
    write_kmz(args.out, kml_text, img, legend)

    total = stats["feasible_px"] + stats["infeasible_px"]
    pct = (100.0 * stats["feasible_px"] / total) if total else 0.0
    print(f"Wrote {args.out}")
    print(f"  guy radius            : {args.guy_radius_ft:.0f} ft")
    print(f"  parcel vertices       : {len(polygon)}")
    print(f"  feasible area (of lot): {pct:.1f}%")
    print(f"  max base clearance    : {stats['max_margin_ft']:.1f} ft beyond the R={args.guy_radius_ft:.0f} ft minimum")
    if not args.demo:
        print("  classification        : PRIVATE / high — do not publish this KMZ")
    return 0


if __name__ == "__main__":
    sys.exit(main())
