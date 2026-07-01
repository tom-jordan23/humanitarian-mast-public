# Milestones & Schedule

**Classification:** `public-safe` — no site-identifying information.

**Core goal:** by **November 15, 2026**, a safe, grounded, weather-ready mast station operating at
the private test site.
**Hard checkpoint:** mast **standing and bonded by September 30, 2026**.

Legend: 🟢 settled · 🟡 working assumption · ❓ open question · 🔒 safety requirement · 🔎 field-verify

---

## July 2026 — Scope freeze & site plan

*Complete (planning artifacts):*

- [ ] 🟢 Mast siting concept
- [ ] 🟢 Guy/anchor geometry
- [ ] 🟢 Field enclosure placement
- [ ] 🟢 Conduit / fiber route
- [ ] 🔒 Grounding and bonding plan
- [ ] 🟢 Initial antenna stack (HF wire + top VHF/UHF vertical)
- [ ] 🟢 First-build bill of materials
- [ ] ❓ Permit / utility / inspection questions list

> Siting, parcel geometry, and route details are **private** (kept in the private repo). Public
> versions are generalized/synthetic only.

## August 2026 — Civil & utility work

*Complete or prepare:*

- [ ] 🔎 Mast base
- [ ] 🔎 Guy anchors
- [ ] 🔒 Grounding electrode and bonding materials
- [ ] 🔎 Conduit sleeves or trenching — **utility locate first** (see `checklists/pre-dig.md`)
- [ ] 🟡 Fiber / data path
- [ ] 🔒 Shack entry panel / bulkhead concept
- [ ] 🔎 Field enclosure mounting point

## September 2026 — Mast & RF build  ⏰ critical checkpoint

> **By September 30, 2026 the mast must be standing and bonded.**

*Complete:*

- [ ] 🔎 Mast assembly
- [ ] 🔎 Guy installation and tensioning
- [ ] 🔒 Bonding and grounding
- [ ] 🟢 VHF/UHF vertical (top-mounted, dual-band)
- [ ] 🟢 HF wire support (one wire system)
- [ ] 🔒 Coax path to shack (through bonded surge protection)
- [ ] 🔒 Surge protection
- [ ] 🔎 Basic continuity and RF checks

> After September 30, **avoid heavy construction scope.** Shift to tuning, cleanup, software,
> monitoring, documentation, and commissioning.

## October – mid-November 2026 — Commissioning

*Complete:*

- [ ] 🟢 Raspberry Pi field station
- [ ] 🟢 Lighting controller
- [ ] 🟡 BirdNET-ready field service capability
- [ ] 🟡 Basic telemetry
- [ ] 🟡 Remote health monitoring
- [ ] 🔒 Winter inspection checklist
- [ ] 🔎 As-built drawings (real → private; sanitized → public)
- [ ] 🟢 Operating notes
- [ ] 🔒 Shutdown / storm procedure

---

## Acceptance criteria for the first build

The first build is successful when:

- [ ] 🔒 Mast is standing, guyed, and bonded
- [ ] VHF/UHF vertical is installed and tested
- [ ] HF wire is installed, protected, and tested
- [ ] 🔒 Coax runs are protected and enter the shack through a bonded path
- [ ] Field enclosure is mounted, weather-protected, and serviceable
- [ ] Pi boots reliably and restarts services after power loss
- [ ] Lighting controller works locally and remotely
- [ ] The system can run in a low-power DC mode
- [ ] Documentation includes as-built notes, diagrams, BOM, and inspection checklists
- [ ] Private geospatial data products are versioned and backed up
- [ ] Public-facing artifacts are sanitized
- [ ] Deferred items remain deferred

## Scheduling notes

- 🔎 items are **field-verified only** — no staking/trenching/concrete/anchor/tower work off
  conceptual or GIS data.
- 🔒 items are on the critical path and must not be treated as deferrable polish.
- ❓ Permit/code/structural review timing depends on the local authority — resolve the "permit /
  utility / inspection questions list" early (July), as it can gate August/September work.
