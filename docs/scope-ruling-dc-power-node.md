# Scope Ruling — DC Power Architecture: Two-Frame Model + Graduation Gate

```yaml
classification:
  visibility: public-safe
  geospatial_sensitivity: none
  contains_real_coordinates: false
  contains_real_parcel_geometry: false
  contains_identifiable_imagery: false
  safe_for_public_repo: true
```

**Ruled by:** scope-warden · **Date:** 2026-07-08 (amended)
**Amends:** the original single-frame "DC solar power node" ruling of the same date, superseded
below per owner decision.
**Question:** Does the owner's two-discrete-frame lab architecture (AC experimentation frame +
solar/battery isolation frame) hold first-build scope discipline, and how does the previous
deferred-item tripwire list map onto it?

---

## 0. What changed

The owner has settled the DC/power architecture as **two discrete, self-contained, weathertight
frames**, not one power node:

1. **Experimentation frame** — AC-powered, no power-budget limit, multiple concurrent
   experiments allowed, full weather exposure. A **lab bench in a box**, not a field-deployment
   claim. Legitimate home for 24/7 Pis, IP cameras, weather instruments, and other experimental
   loads *while they are still experiments*.
2. **Isolation frame** — the solar/battery/12V frame, **one experiment at a time**. This is the
   off-grid **certification** frame: nothing is field-validated as "the build" until it has run,
   alone, in the isolation frame under real solar/battery/weather constraints.
3. **Graduation gate** — the only path from frame 1 to frame 2. An experiment matures in the
   experimentation frame, then is ported as a **single 12V load** into the isolation frame and
   certified there before it counts as "released" / field-ready.
4. Both frames are discrete, weathertight enclosures; all power/sensor couplings cross frame
   boundaries only through **weathertight bulkheads**; both are designed for **relocatable, modular,
   field-flexible** siting — not fixed, bespoke installs.

This does not change the charter's Prime Directive 3 (first-build scope discipline). It changes
**where** the previously-deferred experimental loads are allowed to live while they mature, and it
gives them an explicit, honest path to eventual field status instead of quietly creeping into the
one power node the prior ruling described.

## 1. Verdict: IN-SCOPE, as a two-frame architecture with a graduation gate

The two-frame model is **first-build scope for the isolation frame** (in its minimal form) and a
**sanctioned parallel bench track for the experimentation frame**. Neither frame, on its own,
authorizes deferred RF/mast hardware (rotator, beam/Yagi, remote transmit radio) — those remain
fully out of the first build regardless of which frame's power they'd nominally use, because they
are RF/mast-scope decisions, not power-architecture decisions. See §3.

| Frame | Scope status | Reasoning |
|---|---|---|
| **Isolation frame** (minimal: Pi field station, env sensors, lighting-controller logic, shunt telemetry, duty-cycled BirdNET — the original lean load list) | **IN — first-build spine** | This is the literal charter line item "low-power DC architecture, replicable off-grid." A minimal isolation frame is required to satisfy the Nov 15 acceptance criterion "the system can run in a low-power DC mode." |
| **Experimentation frame** (AC-powered lab bench) | **IN — sanctioned parallel track, not a field-deployment claim** | Matches charter language that the *first build* is what gets field-validated; a bench-only, AC-powered, non-field-replicable rig for maturing experiments does not itself claim to be "the field station." It is infrastructure for **disciplined experimentation**, which the charter has always implicitly needed somewhere — this makes that somewhere explicit and honest instead of ad hoc. |
| **Graduation gate** (process) | **IN — required discipline, not overhead** | This is what keeps the isolation frame's off-grid certification honest. Without a gate, "one and done" isolation-frame sizing (per the original ruling's §2 tripwires) would erode the first time someone wants to try a camera or an extra SDR "just to see." The gate is the mechanism that makes deferral real instead of aspirational. |

## 2. The re-mapping: deferred tripwires now apply to the isolation frame

The original ruling's §2 "deferred tripwires" were written against a single power node, so they
implicitly deferred these items from **the whole build**. That was too blunt for two frames. The
tripwires now apply specifically to **what may enter the isolation frame before graduation** — the
experimentation frame is the sanctioned container for the same items while they mature.

| Item | Experimentation frame | Isolation frame | Note |
|---|---|---|---|
| Camera load (any) | **OK to bench-test** | **BLOCKED until graduated** | "Camera sprawl" stays fully deferred as a *field-site* commitment; a single camera experiment maturing on AC power is fine to run in the box. |
| APRS, airband, LoRa services | **OK to bench-test** | **BLOCKED until graduated** | Same pattern — mature on AC, port as one 12V load only after it's proven worth the isolation frame's power budget. |
| Additional/multiple SDR services | **OK to bench-test (multiple concurrently, that's the point of frame 1)** | **BLOCKED — one experiment at a time, and only after graduation** | The isolation frame's "one experiment at a time" rule is the mechanism that prevents SDR sprawl from ever reaching the field-certified side. |
| LTE modem / LTE failover | **OK to bench-test** | **BLOCKED until graduated** | A permanent LTE dependency is still charter-deferred as a *design commitment*; bench experimentation to characterize it is fine. |
| Weather-station expansion (beyond the minimal env-sensor set) | **OK to bench-test** | **BLOCKED until graduated** | |
| Continuous/24-7 BirdNET on a heavier SBC | **OK to bench-test** | **BLOCKED — isolation frame keeps BirdNET optional/duty-cycled per the original load list, unless/until that specific service graduates** | |
| Permanent automation dashboard built on telemetry | **OK to bench-prototype** | **BLOCKED until graduated** | A hosted/always-on dashboard product is still deferred as a *release commitment*, independent of frame. |
| High-power AC loads / inverter | **This is what the experimentation frame is for** — no additional ruling needed | **Still fully BLOCKED, permanently** | The isolation frame stays DC-native by design; "graduating" an AC load into it is a contradiction in terms. AC loads never cross this boundary. |
| Rotator / beam-Yagi motor loads | **NOT authorized by this ruling in either frame** | **NOT authorized by this ruling in either frame** | These are RF/mast-hardware scope decisions (antenna erected on the mast), not power-architecture decisions. The two-frame amendment does not touch RF/antenna scope. Still fully deferred backlog — see §3. |
| Remote transmit radio | **NOT authorized by this ruling in either frame** | **NOT authorized by this ruling in either frame** | Same reasoning — this is a radio-service scope decision (transmit authority, RF exposure, licensing), not something the power architecture can graduate on its own. Still fully deferred backlog. |
| Remote tuner (unless later justified) | **NOT authorized by this ruling in either frame** | **NOT authorized by this ruling in either frame** | Same category as remote TX — RF-scope, not power-scope. Needs its own documented justification, independent of which frame would power it. |
| Battery autonomy pushed past ~2 days "for margin" | n/a (experimentation frame is AC, autonomy doesn't apply) | **BLOCKED — isolation frame ceiling is ~2 days (1-day fallback), unchanged from the original ruling** | Frame architecture doesn't change isolation-frame sizing discipline. |
| A 3rd/4th solar panel beyond 200W (2×100W) | n/a | **BLOCKED — unchanged ceiling** | |
| Pre-wired/reserved distribution branches for any not-yet-graduated load | n/a | **BLOCKED — same "no provisioning for deferred scope" discipline as the original ruling, now phrased as "no provisioning ahead of graduation"** | |

**Reading this table:** the left two data columns are new; the reasoning column preserves the
original ruling's logic. Nothing that was fully deferred before (rotator, beam, remote TX, remote
tuner) has been promoted anywhere — those three/four items are **RF/mast-scope**, and this is a
**power-architecture** ruling. The two are independent axes. Everything else on the original
tripwire list is a power/data *load*, which is exactly what the two-frame model exists to manage.

## 3. Confirming the RF/mast-scope items stay fully deferred

Rotator, beam/Yagi, remote transmit radio, and remote tuner (unless justified) are **not** power
questions — they require installing additional RF hardware on or near the mast, which is a
first-build antenna-stack decision (`rf-antenna-engineer` territory, one HF wire + one VHF/UHF
vertical per the charter). The owner's two-frame amendment addresses **how experimental loads get
powered and certified**, not **what gets erected on the mast**. Confirmed: these four items remain
on the fully-deferred / out-of-the-whole-first-build list in `bom/deferred-items.md`, unaffected by
this ruling, in **both** frames.

## 4. Timeline check

**The mast-standing-and-bonded checkpoint (Sep 30, 2026) is not threatened by either frame.**

- **Mast + a minimal isolation frame remain the first-build spine.** The isolation frame's load
  list (Pi field station, env sensors, lighting-controller logic, shunt telemetry, duty-cycled
  BirdNET) is unchanged from the original ruling and is required to satisfy the Nov 15 "low-power
  DC mode" acceptance criterion. It can be bench-built/bench-tested independent of mast
  construction, same as before.
- **The experimentation frame grows in parallel or after**, and explicitly does **not** gate Sep 30
  or Nov 15. It is a lab-bench convenience for maturing future capability, not a milestone
  deliverable. Don't let its "no power limits, multiple concurrent experiments" freedom pull
  planning/build bandwidth away from the July scope-freeze deliverables or the Aug/Sep civil and
  grounding work — see `STATUS.md` open items.
- **Real dependency unchanged:** the isolation frame's DC bonding point still needs to coordinate
  with the single-point-ground scheme (mast, coax surge protection, shack entry). Route this
  through `grounding-safety-inspector` before the isolation-frame wiring is finalized, same as the
  original ruling required.
- **New dependency to flag:** the **experimentation frame is AC-powered**, which is a real
  electrical-safety scope (AC wiring, GFCI/bonding, weatherproofing an AC-fed enclosure sitting
  outdoors) that the original DC-only ruling never had to consider. This needs its own review —
  **flagged to `grounding-safety-inspector`**, who is concurrently authoring the safety treatment
  for both frames. This scope-ruling does not itself set AC-safety requirements.
- **Soft caution, unchanged:** don't pour concrete or fix conduit stubs for either frame's siting
  before the field-enclosure mounting-point decision (Aug 2026 milestone item) is settled. Both
  frames are designed to be relocatable/modular, which helps here, but the *first* physical siting
  still needs the same August sequencing discipline as before.

## 5. Conditions attached to this ruling

1. **The isolation frame stays minimal and lean** — same load list, same ~2-day autonomy, same
   200W/2×100W array ceiling as the original ruling. Nothing here re-opens isolation-frame sizing.
2. **"One experiment at a time" in the isolation frame is load-bearing**, not a suggestion — it is
   the mechanism that keeps the certification claim honest. Do not treat it as "one experiment plus
   whatever's already proven," which would silently re-inflate the isolation-frame load over time.
   Each graduation should be a deliberate swap, documented as such.
3. **Graduation is a documented event**, not an implicit one: when an experiment moves from frame 1
   to frame 2, record what it replaced or added, updated power budget, and updated field-enclosure
   contents in the BOM/docs. (Exact form of that record is `field-station-engineer` /
   `field-docs-writer` territory — this ruling only requires that it happens, not its format.)
4. **No pre-wiring or capacity reservation in the isolation frame** for anything not yet graduated
   — unchanged from the original ruling, now read as "not yet graduated" rather than "deferred."
5. **AC safety review required** before the experimentation frame is energized outdoors — routed to
   `grounding-safety-inspector`.
6. **DC bonding/grounding review required** before the isolation frame's DC bonding is finalized —
   routed to `grounding-safety-inspector`, coordinated with the mast/shack single-point-ground plan.
7. **RF/mast-scope items (rotator, beam/Yagi, remote transmit radio, remote tuner) are untouched by
   this ruling** and remain fully deferred regardless of frame, per §3.
8. This ruling **does not specify** frame construction, bulkhead hardware, enclosure siting, or
   service architecture — that is `field-station-engineer`'s concurrent work (frame specs) and
   `grounding-safety-inspector`'s concurrent work (safety doc). This document is scope/discipline
   only; it does not edit `pi-field-station/**` or any new safety/checklist document.

---

**Settled:** two discrete frames — AC experimentation frame (unlimited, multi-experiment, bench
only) and DC/solar isolation frame (12V, one-experiment-at-a-time, off-grid certification) — with a
documented graduation gate between them, is accepted as the project's power architecture. A minimal
isolation frame remains first-build spine; the experimentation frame is a parallel, non-gating bench
track.
**Deferred, mapped by frame:** experimentation-frame-eligible items now cataloged in
`bom/deferred-items.md` §"Experimentation-frame catalog"; RF/mast-scope items (rotator, beam/Yagi,
remote transmit radio, remote tuner) remain fully deferred in both frames.
**Condition:** grounding coordination (isolation frame) and AC-safety review (experimentation
frame) both routed to `grounding-safety-inspector`; graduation events documented; isolation frame
stays lean and one-at-a-time.
