# Humanitarian Antenna Mast Field Station — Public

A disciplined field-systems lab: a humanitarian / off-grid **antenna mast and field station** at a
**private test site** (described here only as a *representative rural field-station test bed*). This
public repository holds **sanitized, generalized, and synthetic** engineering artifacts only.

> **Success standard:** could be understood, packed, rebuilt, powered, troubleshot, and adapted by
> a small field team under constrained conditions.

📌 **Current state & next steps: [`STATUS.md`](STATUS.md).**

## Core goal

By **November 15, 2026**, a safe, grounded, weather-ready mast station operating at the private
test site. Hard checkpoint: **mast standing and bonded by September 30, 2026.**

First build: 50-ft mast + guys/anchors, bonding & grounding, coax surge protection, shack
entry/bulkhead, top-mounted VHF/UHF vertical, one HF wire system, weatherproof field enclosure,
Raspberry Pi edge station, lighting controller, low-power DC architecture, fiber-ready data path,
and rebuild-grade documentation.

## Location privacy

This is a private home site. **No public artifact may reveal the location.** This repo contains no
real address, parcel number, coordinates, property geometry, map/aerial imagery, or real
KML/KMZ/GPX/GeoJSON. Authoritative real-site engineering lives in a **separate private repository**.
See `CLAUDE.md` for the full public/private discipline and the pre-publication review gate.

## Layout

```
docs/                Public (sanitized) engineering docs
diagrams/public/     Sanitized conceptual diagrams  ·  diagrams/templates/
bom/                 Bills of materials (items marked required / nice-to-have / deferred / do-not-buy-yet)
pi-field-station/    Raspberry Pi edge services (services/ scripts/ config/ systemd/)
lighting-controller/ Lighting control wiring/config/test-plan
checklists/          pre-dig · mast-raise · grounding-inspection · rf-test · field-box-test · publication-review · storm-shutdown
archive/             Prior concepts
.claude/             CLAUDE.md guidance, sub-agents, and slash commands
```

## First-time setup (enable the leak guard)

```sh
git config core.hooksPath .githooks   # activates the pre-commit location-leak scanner
```

Leak prevention runs in three layers: strict `.gitignore`, a pre-commit content scanner
(`scripts/check-leaks.sh`), and a CI job (`.github/workflows/leak-scan.yml`) that re-checks every
push. Audit manually anytime with `scripts/check-leaks.sh all`.

## Working with Claude

Read `CLAUDE.md` first. Specialist sub-agents live in `.claude/agents/`; privacy and classification
helpers are `/publication-review` and `/classify`. Nothing moves from the private repo into this one
until it passes the pre-publication review gate.
