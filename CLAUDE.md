# CLAUDE.md — Humanitarian Antenna Mast Field Station

> This file is the source of truth for how Claude works in this repo. Start here every time.
> Source charter: `Humanitarian Antenna Mast Field Station.pdf` (this directory).

## What this project is

A humanitarian / off-grid **antenna mast and field station** at a private home test site. It is
run by an international humanitarian information-management practitioner (Digital Surge Officer /
IT-ITT Officer / IM Officer roles) as a **disciplined field-systems lab**, not a hobby antenna
install.

The standard for success is not "works at home." It is:

> **Could be understood, packed, rebuilt, powered, troubleshot, and adapted by a small field
> team under constrained conditions.**

Every design, doc, script, and BOM should be judged against that sentence.

## Core goal

By **November 15, 2026**: a safe, grounded, weather-ready mast station operating at the private
test site, whose first build includes:

- 50-foot H50 / 25G-style mast concept
- Top-mounted VHF/UHF vertical + one HF wire system
- Bonded coax and surge protection back to the shack
- Weatherproof field enclosure at the mast base
- Raspberry Pi field station (edge services)
- Lighting control for mast/tree/site lighting
- Low-power DC architecture replicable off-grid
- Documentation sufficient to rebuild, inspect, and troubleshoot

**Hard checkpoint:** by **September 30, 2026** the mast must be **standing and bonded**. After
that date, avoid heavy construction scope — shift to tuning, cleanup, software, monitoring,
documentation, and commissioning.

---

## ⚠️ The three prime directives (never trade these away)

These override convenience, performance, and feature ideas. When any of them is in tension with a
request, honor the directive and say so.

### 1. Safety & bonding are first-class

This is a permanent, grounded, structural mast — not a casual temporary pole. Assume proper mast
grounding, coax surge protection, a bonded entry panel, coordination with the premises grounding
electrode system, utility locate before digging, and conservative weather assumptions. Call out
anything that needs a **tower professional, electrician, or local authority (permit/code/
structural)**. Never generate instructions that imply this is a throwaway install.

### 2. Location privacy (public vs private separation)

This is a private home site. **Public artifacts must never leak the location.** Maintain two
classes of artifact:

- **Private, source-of-truth** — real coordinates, parcel geometry, real mast/guy/conduit/
  grounding layouts, real KML/KMZ/GPX/GeoJSON/QGIS, survey data, site photos, as-builts.
- **Public, sanitized derivatives** — local-relative or synthetic coordinates, abstract
  rectangular site outlines, generalized geometry, placeholder names like `private-test-site`.

Public docs must describe this only as a **"private test site" / "representative rural
field-station test bed."** They must **never** contain: street address, parcel number, real
coordinates, real property geometry, map/GIS/aerial screenshots, real KML/KMZ/GPX/GeoJSON, or
identifiable imagery. **If unclear whether an artifact is public or private, default to
`review-required` and treat it as private.** See `docs/` and the `geospatial-privacy-steward`
sub-agent.

### 3. First-build scope discipline

The system starts as a **passive mast-and-utility platform with solar-capable edge services**,
not a complex remote radio site. Preserve the settled scope. Warn loudly when a request adds
complexity before the baseline is stable.

**In the first build:** 50-ft mast, base, guy anchors, bonding/grounding, coax surge protection,
shack entry/bulkhead, top VHF/UHF vertical, one HF wire, field enclosure, Raspberry Pi, lighting
controller, low-power DC, fiber (or fiber-ready) data path, basic docs.

**NOT in the first build (deferred backlog):** rotator, beam/Yagi, multiple experimental RF
services, remote transmit radio, remote tuner (unless later justified), camera sprawl, APRS,
airband, LoRa, LTE failover / permanent LTE dependency, multiple SDR services, weather-station
expansion, permanent automation dashboard, high-power AC loads, solar/battery expansion beyond
what's needed to validate the DC architecture, any non-field-replicable convenience feature.

Do **not** let deferred items derail the first build.

---

## Field-deployment design discipline

**Prefer** designs that are: low-power, solar-capable, DC-native where practical, rugged, modular,
easily documented, easy to inspect, easy to repair, understandable by non-specialists, rebuildable
from commonly available parts, able to recover after power loss, not dependent on cloud services
for core operation, not dependent on home-only conveniences.

**Avoid** designs that: work only because they sit at a comfortable home site; require fragile
configuration knowledge; depend on undocumented manual steps; assume unlimited AC power or stable
internet; need specialized tools without justification; add complexity before the baseline is
stable; would be embarrassing or impractical to recommend for field replication.

## Off-grid / solar / DC discipline

All first-build decisions must be compatible with eventual off-grid operation. Grid power may be
used for testing/fallback, but the **architecture must not depend on it**. Prefer hardware/software
that: runs on 12V/24V DC or efficient DC conversion, recovers automatically after power loss, can
be monitored remotely, has low idle draw, needs no cloud for core operation, and is documentable
and reproducible.

## Data & network architecture

- Prefer **fiber** between house/shack and the field enclosure where practical.
- **Avoid copper Ethernet as the primary long outdoor data path** — it adds a conductive lightning
  pathway.
- Keep the field-box network simple and robust; assume outages and power cycling will happen.
- The Pi must support: local control, local logging, remote access over the site network, recovery
  after reboot, and clear service documentation.

## Antenna priorities

First RF priority is **HF + VHF/UHF** (nothing else yet).

- **VHF/UHF:** one clean, serious, top-mounted dual-band vertical. Mount at/near the top, keep the
  top uncluttered, coax returns to the shack through bonded surge protection, no early side whips
  or unrelated services.
- **HF:** mast as high support for **one** wire system — EFHW, inverted-L, sloper, or similar
  simple wire. Feedpoint/transformer/arrestor/drip-loop/counterpoise plan at/near the mast base
  unless a better reason is documented. Keep tuning and maintenance simple. Favor field-replicable
  patterns over max-performance complexity. Public docs show **generalized** geometry, not real
  site geometry.

Solve the mast/grounding path **before** over-optimizing antennas.

## Field enclosure (base of mast)

Purpose is **edge services, not full remote radio operation.** Initial services: Raspberry Pi
field station, lighting controller, BirdNET-ready microphone support, environmental sensors, DC
power distribution, fiber/data termination, basic telemetry, possibly receive-only SDR later.
**Do not place primary transmit-radio functions in the field enclosure during the first build.**

---

## Repository model (split public / private)

Use a **split repository** model. This repo (`humanitarian-mast-*`) is treated as the **public**
side unless a file/dir is explicitly private.

```
public/   → CLAUDE.md, README, docs/, diagrams/public/, bom/, pi-field-station/,
            lighting-controller/, checklists/, archive/   (sanitized, generalized, synthetic only)
private/  → geospatial/ (source, processed, qgis, kml, geojson, rasters, exports),
            site-engineering/ (mast-location, guy-anchors, conduit-routes, grounding, shack-entry),
            photos/, permits/, manifests/, sanitized-exports/   (authoritative real engineering record)
```

- The **private** repo is the authoritative engineering record and **must be versioned, backed
  up, and reproducible** (≥1 local copy, ≥1 private remote git, ≥1 additional backup; use Git LFS
  / DVC / git-annex / restic for large artifacts — never leave them outside version control).
- The **public** repo contains only sanitized/generalized/synthetic products.
- `private/sanitized-exports/` stages public-safe artifacts; **nothing moves to public until it
  passes privacy review.**
- **Never** suggest that important private geospatial artifacts live only on a single local
  machine, NAS, or workstation.

### Git-ignore posture

- **Public `.gitignore` is strict:** ignore `/private/`, `/geospatial/`, `/site-engineering/`,
  `*.kml *.kmz *.gpx *.geojson *.shp *.shx *.dbf *.prj *.qgz *.qgs`, and location-leak globs
  (`*parcel* *survey* *site-map* *property-boundary* *aerial* *satellite* *plat* *csm* *address*`).
- **Private `.gitignore` ignores only scratch/temp** (`*.tmp *.bak *.aux.xml .qgis2/ __pycache__/
  scratch/ tmp/ working/`). Do **not** globally ignore geospatial data in the private repo — it is
  versioned intentionally.

## Data-product classification

Every generated artifact gets a classification header:

```yaml
classification:
  visibility: private | public-safe | review-required
  geospatial_sensitivity: none | low | medium | high
  contains_real_coordinates: true | false
  contains_real_parcel_geometry: true | false
  contains_identifiable_imagery: true | false
  safe_for_public_repo: true | false
```

If an artifact contains real coordinates, real parcel geometry, identifiable imagery, or
address-derived info → it is **private by default**.

## Pre-publication review gate

Before any artifact moves private → public, run the gate (see `/publication-review`). If **any**
answer is yes, do **not** publish — create a sanitized derivative instead:

Real address? parcel number? real coordinates? real parcel geometry? real KML/KMZ/GPX/GeoJSON?
county GIS / Google Maps / aerial imagery? road names or nearby landmarks? EXIF GPS metadata? Does
the filename reveal the location? Could a motivated reader identify the home site from this
artifact?

**Photos:** strip EXIF/GPS, check background landmarks (road frontage, mailbox, house number,
driveway, unique buildings), avoid map-UI/parcel/aerial screenshots, prefer close-up construction
shots, and use sanitized filenames (no address/parcel/road/county-GIS clues).

---

## Sub-agents (delegate to the right expert)

Specialists live in `.claude/agents/`. Delegate proactively:

| Sub-agent | Use it for |
|-----------|-----------|
| `geospatial-privacy-steward` | Any public-facing artifact, sanitization, classification, publication review, geospatial versioning/backup. **Consult before anything is published.** |
| `grounding-safety-inspector` | Grounding, bonding, lightning/surge, structural, permit/code, utility-locate concerns; flagging pro-required work. |
| `rf-antenna-engineer` | HF wire + VHF/UHF vertical design, coax/feedpoint/arrestor/counterpoise, RF checks. |
| `field-station-engineer` | Raspberry Pi services, DC power distribution, lighting controller, BirdNET/sensors, telemetry, recovery-after-reboot, fiber/network. |
| `scope-warden` | Checking whether a request stays inside first-build scope; managing the deferred backlog. |
| `field-docs-writer` | BOMs, checklists, as-builts, commissioning notes, operating/storm procedures, diagrams (public). |

Slash commands: `/publication-review` (run the privacy gate), `/classify` (tag an artifact).

## Engineering guardrails (how Claude should behave)

- **Start from this file.** Confirm whether a request affects first-build scope and the Nov 15 /
  Sept 30 milestones.
- Preserve settled scope unless explicitly changed; separate "first build" vs "later enhancement"
  vs "bad idea for now."
- Prefer durable civil/electrical infrastructure over buying radios early. Prefer simple,
  inspectable, field-replicable systems.
- **Do not invent** dimensions, code requirements, parcel facts, equipment specs, or geospatial
  details. When uncertain, label the assumption clearly and **create a verification task**.
- Any staking, trenching, concrete, guy-anchor install, or permanent tower work is
  **field-verified only** — never treat public GIS, conceptual drawings, or sanitized diagrams as
  construction-grade survey data.
- Produce practical artifacts saved directly into the repo. Use concise engineering language;
  prefer tables and checklists.
- Distinguish in docs: settled decisions · working assumptions · open questions · deferred
  features · safety requirements. Mark BOM items (required / nice-to-have / deferred / do-not-buy-yet)
  and data products (public-safe / private / review-required).
- Treat private geospatial artifacts as **durable engineering records, not disposable scratch**.
  Treat public artifacts as **sanitized derivatives, not copies** of private site products.

## The core pattern this first build must prove

**HF + VHF, safe mast, bonded entry, solar-capable field enclosure, Pi edge services, lighting
control, and field-replicable documentation.**
