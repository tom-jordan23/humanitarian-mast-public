# Project Status

**As of:** 2026-06-30
**Goal:** safe, grounded, weather-ready mast station operating by **Nov 15, 2026** ·
**Hard checkpoint:** mast standing & bonded by **Sep 30, 2026**.
**Classification:** `public-safe` — no site-identifying information.

---

## Where things stand

Foundation and governance are complete; no physical build work has started yet. The project is in
the **planning / scope-freeze** phase (July 2026 milestone).

### ✅ Done — infrastructure & governance

- **Two repositories (split public/private model):**
  - `humanitarian-mast-public` — https://github.com/tom-jordan23/humanitarian-mast-public (PUBLIC)
  - `humanitarian-mast-private` — https://github.com/tom-jordan23/humanitarian-mast-private (PRIVATE)
- **CLAUDE.md governance** in both repos (charter, three prime directives, scope, discipline).
- **Six specialist sub-agents** (`.claude/agents/`): `geospatial-privacy-steward`,
  `grounding-safety-inspector`, `rf-antenna-engineer`, `field-station-engineer`, `scope-warden`,
  `field-docs-writer`.
- **Slash commands:** `/publication-review`, `/classify`.
- **Public repo tree scaffolded:** `docs/ diagrams/ bom/ pi-field-station/ lighting-controller/
  checklists/ archive/` with README stubs.
- **Automated leak prevention (verified):** strict `.gitignore` + pre-commit content scanner
  (`scripts/check-leaks.sh`) + CI (`.github/workflows/leak-scan.yml`, passing). Blocks geo file
  types, location-token filenames, GPS EXIF, and decimal `lat,lon` patterns.
- **Private repo:** Git LFS configured (`.gitattributes`), manifest + checksum template, backup
  strategy settled.

### ✅ Done — first documents

- `docs/milestones.md` — full schedule + acceptance criteria.
- `docs/safety-grounding-bonding.md` — single-point-ground / bonded-entry discipline.
- `checklists/pre-dig.md` — utility-locate-first excavation gate.

### 🟢 Settled decisions

- Repo names and split public/private model.
- Charter PDF is public (`docs-source-charter.pdf`).
- **Backup baseline:** local working copy + private GitHub remote is sufficient; third/offline copy
  optional. Priority is leak prevention, not redundancy.
- First-build scope frozen per the charter; deferred backlog stands (rotator, beam, remote TX,
  APRS, LoRa, LTE, extra SDRs, etc.).

---

## Next steps (prioritized)

### 1. Finish the July scope-freeze deliverables
- [ ] Permit / utility / inspection **questions list** (gates Aug/Sep work) — `docs/`.
- [ ] `bom/first-build-bom.md` (+ `deferred-items.md`) — items marked required / nice-to-have /
      deferred / do-not-buy-yet. → `field-docs-writer` + `scope-warden`.
- [ ] Antenna stack decisions: `docs/antenna-plan.md` (HF wire type + top VHF/UHF vertical,
      generalized geometry). → `rf-antenna-engineer`.

### 2. Remaining core docs & checklists
- [ ] `docs/field-enclosure.md`, `docs/solar-dc-power.md`, `docs/commissioning.md`,
      `docs/winterization.md`, `docs/public-architecture.md`, `docs/goals.md`.
- [ ] Checklists: `mast-raise.md`, `grounding-inspection.md`, `rf-test.md`, `field-box-test.md`,
      `publication-review.md`, `storm-shutdown.md`.

### 3. Private engineering capture (real-site, field-verified)
- [ ] Begin `site-engineering/` and `geospatial/` real artifacts: mast siting, guy/anchor geometry,
      conduit route, grounding plan. **Field-verified only**, each with a manifest + classification.
      → `grounding-safety-inspector` for the grounding plan; `geospatial-privacy-steward` for
      classification/versioning.

### 4. Field station software (after baseline docs)
- [ ] Scaffold `pi-field-station/` services (systemd units, recover-after-reboot) and
      `lighting-controller/` config/test-plan. → `field-station-engineer`.

---

## Open questions (do NOT invent — field/pro-verify)

- Permit / code / **structural review** requirements → local authority (AHJ).
- 811 (utility locate) lead time → local one-call center.
- Foundation & guy-anchor specs, ground-electrode depth/count, bonding conductor sizing →
  licensed structural engineer / electrician.
- Local strike / soil-resistivity environment.

## Operating reminders

- On any fresh clone of the public repo: `git config core.hooksPath .githooks` to enable the leak
  guard (CI is the backstop regardless).
- Nothing moves private → public without passing `/publication-review`.
- After Sep 30, avoid heavy construction scope — shift to tuning, software, monitoring, docs,
  commissioning.
