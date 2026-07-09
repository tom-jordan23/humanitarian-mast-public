# Deferred Items Backlog & Experimentation-Frame Catalog

```yaml
classification:
  visibility: public-safe
  geospatial_sensitivity: none
  contains_real_coordinates: false
  contains_real_parcel_geometry: false
  contains_identifiable_imagery: false
  safe_for_public_repo: true
```

Items here are **not in the field-certified first build**. They are not cancelled — they're parked
until either (a) the baseline is stable and there's a specific, justified reason to promote a
still-fully-deferred item, or (b) an experimentation-frame item clears the **graduation gate**
described in `docs/scope-ruling-dc-power-node.md`. Nothing moves off this list without an explicit
scope decision (see `.claude/agents/scope-warden.md`).

Per the owner's two-frame power architecture (2026-07-08 amendment), this backlog now splits into
two categories:

- **§A — Still fully deferred, out of the whole first build (both frames).** RF/mast-hardware and
  release-commitment items that the two-frame power amendment does not touch. No frame authorizes
  these; they need their own scope decision.
- **§B — Experimentation-frame catalog.** Loads/services that are **sanctioned to run in the
  AC-powered experimentation frame now**, as bench experiments, but are **blocked from the
  solar/battery isolation frame** until they clear the graduation gate (mature in frame 1 → port as
  a single 12V load → certify in frame 2). Running something in the experimentation frame is **not**
  a field-deployment claim — nothing there counts as "the build" until graduated.

All items are marked **do-not-buy-yet** unless the entry says otherwise.

---

## §A — Still fully deferred (out of the whole first build, both frames)

These are RF/mast-hardware scope decisions or release commitments. The two-frame power amendment
is a power-architecture decision and does not authorize any of these in either frame. See
`docs/scope-ruling-dc-power-node.md` §3.

### RF / antenna
- Rotator
- Beam / Yagi
- Remote transmit radio
- Remote tuner (unless later justified with a documented reason)

### Release commitments (frame-independent)
- Permanent automation dashboard as a **shipped/hosted product** commitment (bench-prototyping the
  dashboard itself is §B-eligible — see below; *committing* to it as a permanent service is not)

---

## §B — Experimentation-frame catalog (OK in frame 1, blocked from frame 2 until graduated)

| Item | Experimentation frame (AC, unlimited, multi-experiment) | Isolation frame (12V, solar/battery, one-at-a-time) |
|---|---|---|
| Camera(s), any load beyond none | **OK to bench-test** — "camera sprawl" is fine as an experiment, not as a field commitment | **Blocked until graduated** as a single ported 12V camera load |
| APRS | **OK to bench-test** | **Blocked until graduated** |
| Airband | **OK to bench-test** | **Blocked until graduated** |
| LoRa | **OK to bench-test** | **Blocked until graduated** |
| LTE modem / LTE failover | **OK to bench-test** | **Blocked until graduated** — a permanent LTE dependency stays out of the isolation frame's design commitment even after graduation is *considered*; graduating here means "characterized as a deliberate single load," not "adopted as core architecture" |
| Multiple/additional SDR services | **OK to run several concurrently** — that concurrency is exactly what frame 1 is for | **Blocked — isolation frame enforces one experiment at a time**; at most one SDR service may ever be the *current* isolation-frame experiment, and only after graduation |
| Weather-station expansion (beyond the minimal env-sensor set already in the isolation-frame load list) | **OK to bench-test** | **Blocked until graduated** |
| Continuous/24-7 BirdNET on a heavier SBC | **OK to bench-test** | **Blocked** — isolation frame keeps BirdNET optional/duty-cycled per its settled lean load list, unless/until this specific service clears graduation |
| Permanent automation dashboard (prototype/bench version) | **OK to bench-prototype** | **Blocked** — see §A; even after graduation this would need its own separate scope decision before being treated as a permanent isolation-frame service |

**Graduation gate (how an item moves from this table's left column to the right):** mature the
experiment in the experimentation frame → port it as a **single** 12V load into the isolation frame
→ certify it there under real solar/battery/weather constraints, with the isolation frame still
running only that one experiment at a time → document the graduation event (what it replaced/added,
updated power budget, updated enclosure contents). Full process detail: `field-station-engineer`
(frame specs) and `docs/scope-ruling-dc-power-node.md` (scope conditions).

---

## Power / electrical backlog (isolation-frame sizing ceilings — unaffected by frame split)

These are isolation-frame-specific sizing tripwires, not graduation candidates — they stay blocked
regardless of the two-frame model:

- Battery autonomy pushed past ~2 days (1-day fallback) "for margin" — later-enhancement, decide
  from real operational data, not speculative padding
- A 3rd/4th solar panel beyond the ratified 200W (2×100W) array
- Any AC inverter added to the isolation frame — **the isolation frame stays DC-native by design;
  AC loads live in the experimentation frame and never cross into the isolation frame, graduation
  gate or not**
- Pre-wired/reserved Powerpole distribution branches in the isolation frame for any not-yet-graduated
  load — do not provision isolation-frame capacity ahead of an actual graduation event
- Powering deferred RF hardware (§A: rotator, beam, remote TX, remote tuner) off either frame's
  power bank — these are RF-scope blocks, not power-sizing questions; no amount of isolation-frame
  or experimentation-frame headroom authorizes them

## General

- Any non-field-replicable convenience feature (applies to the isolation frame; the experimentation
  frame is explicitly *not* held to field-replicability, since it makes no field-deployment claim)

---

## Provenance

- General backlog per `CLAUDE.md` Prime Directive 3 and `bom/README.md`.
- Two-frame split (§A vs §B) and graduation-gate mechanism per
  `docs/scope-ruling-dc-power-node.md` (2026-07-08 scope ruling, amended same day for the owner's
  two-discrete-frame power architecture decision).

See also: `docs/scope-ruling-dc-power-node.md` for the full reasoning behind this split.
