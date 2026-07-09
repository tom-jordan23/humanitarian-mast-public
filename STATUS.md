# Project Status

**As of:** 2026-07-09
**Goal:** safe, grounded, weather-ready mast station operating by **Nov 15, 2026** ·
**Hard checkpoint:** mast standing & bonded by **Sep 30, 2026**.
**Classification:** `public-safe` — no site-identifying information.

---

## Where things stand

Foundation and governance are complete and **design work is well underway**; no physical build has
started yet. This cycle advanced the **DC power architecture, HF antenna plan, and mast siting**
substantially. Still in the **planning / scope-freeze** phase (July 2026 milestone).

### ✅ Done — infrastructure & governance

- **Two repositories (split public/private model):**
  - `humanitarian-mast-public` — https://github.com/tom-jordan23/humanitarian-mast-public (PUBLIC)
  - `humanitarian-mast-private` — https://github.com/tom-jordan23/humanitarian-mast-private (PRIVATE)
- **CLAUDE.md governance** in both repos (charter, three prime directives, scope, discipline).
- **Six specialist sub-agents** + slash commands (`/publication-review`, `/classify`).
- **Automated leak prevention (verified):** strict `.gitignore` + pre-commit content scanner
  (`scripts/check-leaks.sh`) + CI (`.github/workflows/leak-scan.yml`, passing).
- **Private repo:** Git LFS configured, manifest + checksum template, backup baseline settled.

### ✅ Done — first documents

- `docs/milestones.md` · `docs/safety-grounding-bonding.md` · `checklists/pre-dig.md`.

### ✅ Done — design (this cycle)

- **Mast siting selected** (SW edge, between two trees); guy-clearance **placement-overlay
  generator** built (`tools/placement-overlay/`, public-safe, reads KML/KMZ/GeoJSON → KMZ heat
  overlay). Real parcel overlay generated and kept **private**.
- `docs/antenna-hf-sloper.md` — **HF sloper**: high end at the 50-ft mast top, fed at the shack
  low end, with a mast-top VHF/UHF decoupling standoff. (Generalized geometry; public-safe.)
- **Two-frame DC power architecture:**
  - `docs/scope-ruling-dc-power-node.md` — scope ruling + **graduation gate**.
  - `pi-field-station/power/README.md` — **isolation frame** (12V solar/battery, **1× Pi 5**,
    50Ah / ~2-day, 200W MPPT, Gore-vent IP66 + battery/electronics thermal zoning).
  - `pi-field-station/experimentation-frame/README.md` — **experimentation frame** (AC bench,
    **3–4 pluggable bays**: 1 Jetson-class + 2–3 Pi 5, **passive keyed-connector backplane**,
    shared cross-frame **Experiment Module** interface).
  - `docs/safety-power-frames-bonding.md` + `checklists/frame-relocation-bonding.md` — AC/DC
    bonding into the single site ground; per-location bonding for the relocatable frame.
  - `bom/deferred-items.md` — fully-deferred list + experimentation-frame catalog.

### 🟢 Settled decisions

- Repo names + split public/private model; backup baseline; first-build scope frozen.
- **Operator is QRP (≤20W)** — low RF component ratings + a small DC budget.
- **Two-frame lab model:** an AC **experimentation bench** (unconstrained, bench-only, no field
  claim) + a solar **isolation frame** (12V, one experiment at a time, field-certification), joined
  by a graduation gate. Deferred tripwires apply to the isolation frame; rotator/beam/remote-TX/
  tuner stay fully deferred in **both** frames.
- **Enclosure law:** discrete, weathertight enclosures; every power/sensor coupling through a
  weathertight bulkhead; total field flexibility. Gore-vent/IP66 (owner field-proven) as the
  isolation-frame baseline.
- **HF:** single sloper, ~20 ft low end rising to the 50-ft mast top, clear ≥20 ft its full length.

---

## Next steps (prioritized)

### 1. Finish the July scope-freeze deliverables
- [ ] Permit / utility / inspection **questions list** (gates Aug/Sep work) — `docs/`.
- [ ] `bom/first-build-bom.md` — required / nice-to-have / deferred / do-not-buy-yet.
      → `field-docs-writer` + `scope-warden`.  *(`deferred-items.md` ✅ done.)*
- [ ] Antenna plan completion: the **top VHF/UHF vertical** + consolidated `docs/antenna-plan.md`.
      → `rf-antenna-engineer`.  *(HF sloper ✅ done.)*

### 2. Grounding-first sequencing (Aug/Sep)
- [ ] **Joint single-point-ground design** covering the mast, shack entry, and **both power
      frames' bonding points** — must be designed together and installed **once**, not retrofitted.
      → `grounding-safety-inspector` + licensed electrician / AHJ.

### 3. Blocking verifications before any power-frame build
- [ ] Real in-line **Pi 5 / Jetson current draw**; aggregate **thermal calc** (experimentation
      frame) before thermal BOM; **PP vs SB connector non-mating** confirmation; **sun-path/shade
      study** at the panel site; enclosure **dry-fit** mockups; wire-gauge/voltage-drop calc.

### 4. Remaining core docs & checklists
- [ ] `docs/field-enclosure.md`, `docs/commissioning.md`, `docs/winterization.md`,
      `docs/public-architecture.md`, `docs/goals.md`; checklists: `mast-raise.md`,
      `grounding-inspection.md`, `rf-test.md`, `field-box-test.md`, `storm-shutdown.md`.

### 5. Private engineering capture (real-site, field-verified)
- [ ] `site-engineering/` + `geospatial/` real artifacts (mast siting done as overlay; add
      guy/anchor geometry, conduit route, grounding plan). **Field-verified only**, each with a
      manifest + classification. → `grounding-safety-inspector`, `geospatial-privacy-steward`.

---

## Open questions (do NOT invent — field/pro-verify)

- Permit / code / **structural review** requirements → local authority (AHJ).
- **Outdoor AC** (experimentation frame): GFCI/disconnect/wet-location/detached-structure bonding →
  **licensed electrician** + AHJ (see `docs/safety-power-frames-bonding.md`).
- 811 (utility locate) lead time; foundation & guy-anchor specs; ground-electrode depth/count;
  bonding-conductor sizing → structural engineer / electrician.
- Local strike / soil-resistivity environment.
- **Which specific Pi 5 / Jetson SKUs** — pins the real power/thermal numbers.

## Operating reminders

- On any fresh clone of the public repo: `git config core.hooksPath .githooks` to enable the leak
  guard (CI is the backstop regardless).
- Nothing moves private → public without passing `/publication-review`.
- After Sep 30, avoid heavy construction scope — shift to tuning, software, monitoring, docs,
  commissioning.
</content>
