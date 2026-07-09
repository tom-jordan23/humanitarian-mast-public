# bom/ — Bills of Materials

```yaml
classification:
  visibility: public-safe
  geospatial_sensitivity: none
  contains_real_coordinates: false
  contains_real_parcel_geometry: false
  contains_identifiable_imagery: false
  safe_for_public_repo: true
```

Every BOM item, in every file in this repo, is marked with one of:

- **Required for first build**
- **Nice to have**
- **Deferred**
- **Do not buy yet**

## Files

| File | Status | Contents |
|---|---|---|
| `first-build-bom.md` | Planned, not yet written | Consolidated required/nice-to-have items for the mast + minimal isolation frame first build. |
| `deferred-items.md` | **Written — authority for all deferred scope** | Full deferred backlog, split by the two-frame power model (see below). |
| `vendor-notes.md` | Planned, not yet written | Vendor/quote notes, once purchasing starts. |

Frame-specific power/electrical BOMs are **not duplicated here** — they live with the frame specs
that own them:

- `pi-field-station/power/README.md` §11 — isolation-frame BOM (solar/battery, 12V, first-build spine).
- `pi-field-station/experimentation-frame/README.md` §9 — experimentation-frame BOM (AC-powered lab
  bench).

## Deferred backlog — authority is `bom/deferred-items.md`

Since the owner's 2026-07-08 two-frame power-architecture decision
(`docs/scope-ruling-dc-power-node.md`), the deferred backlog is **not a single flat list**. It
splits into two parts — do not treat this README as the catalog; it only indexes it:

| Category | Meaning | Where |
|---|---|---|
| **§A — Fully deferred (both frames)** | RF/mast-hardware and release-commitment items no frame authorizes: rotator, beam/Yagi, remote transmit radio, remote tuner (unless justified), a *shipped/hosted* automation-dashboard commitment. | `bom/deferred-items.md` §A |
| **§B — Experimentation-frame catalog** | Loads sanctioned to **bench-test now** in the AC-powered experimentation frame (cameras, APRS, airband, LoRa, LTE modem, multiple SDR services, weather-station expansion, 24/7 BirdNET, dashboard prototyping) but **blocked from the solar/battery isolation frame** until each clears the documented **graduation gate** (mature in frame 1 → port as a single 12V load → certify in frame 2). | `bom/deferred-items.md` §B |
| **Isolation-frame sizing ceilings** | Not graduation candidates — stay blocked regardless of frame: >2-day battery autonomy, a 3rd/4th solar panel beyond 200W, any AC inverter in the isolation frame, pre-wired/reserved branches for ungraduated loads. | `bom/deferred-items.md` "Power / electrical backlog" |

See `docs/scope-ruling-dc-power-node.md` for the full reasoning and the graduation-gate mechanism.
Nothing moves off the deferred list, or between §A/§B, without an explicit scope decision — see
`.claude/agents/scope-warden.md`.

Use the `field-docs-writer` and `scope-warden` sub-agents.
