---
classification:
  visibility: public-safe
  geospatial_sensitivity: none
  contains_real_coordinates: false
  contains_real_parcel_geometry: false
  contains_identifiable_imagery: false
  safe_for_public_repo: true
---

# HF Antenna: Sloping Wire (Sloper / Inverted-L Hybrid) — Design Note

> First-build HF scope: **one** simple wire system on the mast (EFHW / inverted-L / sloper or
> similar). This note evaluates the settled sloping-wire geometry and gives a design pattern —
> not final dimensions. Geometry described here is **generalized** (compass bearings, relative
> heights, qualitative slope) and contains no coordinates, parcel geometry, or site-identifying
> detail.

Legend: 🟢 settled · 🔧 working assumption · ❓ open question · 🔎 verify/tune (field task) · ⏸ deferred · 🔒 safety

> **Revision note:** this update incorporates a geometry refinement — the wire's low (NE) end is
> **co-located with the shack entry** (house sits NE of the mast; the shack is on the side of the
> house facing the mast). That changes the feed-point grounding picture (§2, §5) and introduces a
> new high-end coupling consideration with the top-mounted VHF/UHF vertical (§2b). Directionality
> (§3) is re-checked against this. All bearings/heights remain generalized — no coordinates or
> parcel geometry added.

---

## 1. Geometry summary (generalized, as given)

| Parameter | Value | Status |
|---|---|---|
| High end | ~50 ft AGL, at mast top, SW | 🟢 settled |
| Low end | ~20 ft AGL, NE, co-located with the shack entry (house sited NE of the mast; shack on the mast-facing side of the house) | 🟢 settled |
| Clearance | ≥20 ft AGL for full wire run | 🟢 settled |
| Terrain along run | Falls <10 ft SW→NE; effective slope somewhat gentler than a flat 50→20 ft (30 ft) drop implies | 🟢 settled (qualitative) |
| Horizontal run length | Not yet specified (now effectively "mast to shack") | ❓ open |
| Total wire length | Not yet specified | ❓ open |
| Target HF band(s) | Not yet specified | ❓ open |
| Low-end attachment hardware (wall bracket/standoff at the shack) | Not yet specified | ❓ open |

The ❓ items (run length, wire length, band, low-end attachment hardware) are the primary blockers
to a final band plan and matching component selection. Nothing below invents them.

---

## 2. Classification: what this geometry naturally becomes

As described — a single wire strung between a **high, fixed point at the mast top** and a
**lower end at the shack**, to the NE — this is fundamentally a **sloper** (single-wire diagonal
radiator between a high and a low anchor), not a level flat-top or a symmetric doublet. The
open question is *where it is fed*, which determines whether it reads as a classic end-fed sloper
or an inverted-L variant.

| Option | Feed location | Fit to this geometry | Read |
|---|---|---|---|
| **A — Low-end feed at the shack entry (recommended default)** | At/immediately adjacent to the shack's bonded bulkhead entry (~20 ft AGL end, NE) | Matches the wire's natural low, accessible end; classic end-fed sloper practice; feed hardware sits right where the bonded entry already is | 🔧 **working default** |
| B — High-end feed | At the mast top (~50 ft) | Requires transformer/arrestor 50 ft up — poor field access, conflicts with "keep tuning/maintenance simple" and "keep the mast top uncluttered" (VHF/UHF directive) | Not recommended |
| C — Mast-base feed with a vertical riser | At mast base (SW), wire runs up the mast on standoffs to the top, then slopes to the NE low end (inverted-L-like, sloping top leg) | Satisfies the charter's literal "feed at mast base" default, but adds a vertical HF wire running past the top-mounted VHF/UHF vertical — a coupling/detuning risk (see §2b) | 🔧 secondary alternative, now less motivated (see below) |

**Reconciliation with the charter's "feedpoint at/near mast base" default:** that default exists
because the mast base is normally where the arrestor, bonded entry, and counterpoise/ground plan
naturally co-locate. With the low end now confirmed at the shack, the *same logic that motivates
"feed near the mast base" is satisfied at the other end of the wire instead* — the feed point is
still right next to the single bonded entry/arrestor location, just at the shack rather than the
mast footing. This is a stronger, simpler reconciliation than before.

**Recommendation: feed at the low (NE) end, at/adjacent to the shack entry (Option A).** This is
now clearly favored, not just a workaround:

- The unun/feedpoint hardware can mount directly on (or immediately next to) the exterior wall
  bracket at the bonded bulkhead entry — minimal outdoor coax run, minimal exposed hardware.
- **The earlier "second, isolated outdoor ground point" concern is resolved.** Because the feed
  is co-located with the shack entry, the feed-point ground and the bulkhead/entry ground are the
  **same point**, not two points needing separate bonding. See §5.
- What still needs `grounding-safety-inspector` review: confirming the unun/feedpoint arrestor
  and the bulkhead entry arrestor reference a single common ground buss (not two separate paths
  into the structure), and any code/practice considerations for mounting antenna hardware and a
  loaded wire directly on the dwelling (clearance from combustibles, mounting hardware rating,
  local code). This is a narrower, more tractable question than the original "bond a remote
  ground rod into the system" task.
- Option C (mast-base riser) is now **less motivated** — it no longer offers a grounding
  simplification the shack-entry feed doesn't already provide, and it still carries the VHF/UHF
  coupling risk. Keep it only as a fallback if the shack-wall attachment proves structurally or
  aesthetically unworkable.

---

## 2b. New consideration: HF high-end coupling with the top-mounted VHF/UHF vertical

The wire's high end terminates **at the mast top — the same location as the top-mounted VHF/UHF
vertical.** The charter's VHF/UHF section calls for keeping the mast top uncluttered; a second
antenna's end insulator and wire landing right at that point is a real proximity/coupling risk,
even though HF and VHF/UHF are far apart in frequency (gross detuning of the VHF/UHF vertical is
unlikely, but near-field interaction, mechanical clutter, and pattern distortion of either antenna
are still worth avoiding by design rather than discovering after install).

**Practical mitigation (design pattern, not final dimensions):**

- Mount the VHF/UHF vertical at the true physical top of the mast, per its own design (unchanged).
- Terminate the HF wire's high-end insulator on a **short standoff arm/bracket offset below and/or
  horizontally away** from the VHF/UHF vertical's active element and coax connection — "near the
  mast top" (satisfying "mast as the high support") without sharing the same attachment point.
- Use a non-conductive end insulator and a dielectric standoff; keep the initial run of HF wire
  away from the VHF/UHF antenna's element and feedline before it slopes off toward the shack.
- Treat exact clearance as a **field/bench verification task**, not a fixed spec: after
  installation, check the VHF/UHF vertical's performance (e.g., SWR) with the HF wire in place vs.
  disconnected/detuned, to confirm no meaningful interaction. No separation distance is asserted
  here as a verified number.
- If interaction is found, options in order of preference: increase the standoff arm's offset,
  reposition the HF wire's attachment slightly lower on the mast (still "near the top"), or add
  decoupling on the VHF/UHF coax — evaluate in the field, not by assumption.

This stays inside first-build scope: it's a mounting/mechanical detail of the same two antennas
already planned, not a new antenna or service.

---

## 3. Directionality & takeoff (qualitative)

- **Favored azimuth:** for a sloping wire, the dominant lobe typically forms in the direction the
  wire slopes *down and away from* the high support — i.e., generally toward the **low (NE) end**
  of this run, with reduced response back toward the high (SW) end. Expect a broad, moderately
  directive pattern rather than a sharp beam.
- **Role of the high (SW) end:** mechanically it is the top anchor (and, if Option C were used,
  the electrical top); electrically, for a low/end-fed sloper (Option A), it contributes less to
  the far-field pattern than the low end does.
- **Re-check now that the low end is at the shack:** the favored lobe direction (toward NE) now
  points back generally over/near the house, while the high (SW) end points out over the open
  property. Two separate questions here, kept distinct:
  - *Far-field pattern impact of the house* — at HF, wire heights of 20–50 ft are electrically
    close to the ground/structure on the lower bands, and slopers already produce broad, high-angle
    patterns on those bands; a nearby, electrically small wood-frame structure is typically a minor
    pattern perturbation rather than a major redirection, but this is **not verified** without
    modeling against real structure/material data (private-side, later, non-blocking).
  - *Near-field/RF-in-the-shack consideration* — because the feed and part of the low-end wire run
    are now close to the dwelling, treat routine RF-safety/RFI good practice (keep transmit power
    reasonable during initial testing, check for RFI into house electronics/networking, don't run
    the wire directly over roofing/gutters if avoidable) as a **first-build commissioning check**,
    not a redesign trigger.
  - Neither point changes the recommended feed location (§2) — they're flagged as minor,
    non-blocking items for the RF-test/commissioning checklist (§6).
- **Takeoff angle vs. band:** wire height in *wavelengths* (not feet) drives takeoff angle. At
  20–50 ft AGL:
  - **Lower HF bands** (longer wavelength → wire is a small fraction of a wavelength high):
    expect a **high takeoff angle** — more NVIS/regional-leaning behavior.
  - **Upper HF bands** (shorter wavelength → wire height is a larger fraction of, or exceeds, a
    wavelength): expect the takeoff angle to **lower**, trending toward more DX-capable angles.
  - This is a **qualitative trend**, not a modeled prediction. No gain, SWR, or takeoff-angle
    numbers should be treated as verified until the band(s) and true dimensions are set and
    (optionally) modeled.

---

## 4. Slope-angle effect (qualitative)

- The **actual slope angle** is set mainly by the ratio of vertical drop to **horizontal run
  length** — and horizontal run length is not yet specified (❓ open, §1). Without it, no slope
  angle or wire length can be responsibly stated.
- As given, terrain reduces the *net* elevation difference between the two wire ends versus a
  naive flat-ground 50→20 ft (30 ft) calculation — so treat the true slope as **somewhat gentler**
  than a flat-terrain estimate.
- General trend to keep in mind once the run length is known:
  - A **steep** slope (short horizontal run relative to the height difference) behaves more like
    a quarter/half-wave vertical sloper — more pronounced low-angle directivity toward the low
    end.
  - A **shallow** slope (long horizontal run relative to the height difference) behaves more like
    a horizontal wire — higher takeoff angle overall, with the same general directive lean toward
    the low (NE) end, but less pronounced.
- 🔎 Once horizontal run length and target band are known, this can be checked with basic
  modeling (see §6) — private-side only, since accurate modeling needs real site heights/terrain.

---

## 5. First-build recommendations

| Element | Pattern | Notes |
|---|---|---|
| Wire type | Single-wire **end-fed sloper**, fed at the low (NE) end | 🔧 working default (§2, Option A) |
| Matching | End-fed half-wave (EFHW) style step-up transformer ("unun") mounted at/immediately adjacent to the shack's exterior wall bracket, next to the bonded entry | 🔎 exact ratio and wire length depend on target band(s) — do not assume 49:1 or any specific figure until band is chosen and length is tuned/measured |
| Wire length | Sized to the chosen band(s) (e.g., half-wave or a multi-band EFHW length) | ❓ open — pick target band(s) first |
| Counterpoise / ground plan | A modest counterpoise (a small number of short wires) at the feed point, bonded to the **same** ground/arrestor system as the bulkhead entry | 🔎 count and lengths are a tuning task, not to be invented |
| Arrestor | One coax lightning arrestor at/near the feed point, referencing the **same single bonded ground buss** as the bulkhead entry (feed point and entry are now co-located, so this may be a single consolidated arrestor rather than two separate ones) | 🔒 confirm with `grounding-safety-inspector` — single-point-ground discipline still applies; verify one common return path, and any code considerations for mounting antenna hardware directly on the dwelling |
| Coax routing | Feed point (at the shack) → arrestor → short run into the bonded bulkhead entry | Outdoor coax run is now minimal — this is a simplification vs. the earlier remote-support assumption |
| Tuning method | Trim/adjust length at install using an antenna analyzer; no automatic/remote tuner | Remote tuner is explicitly deferred-unless-justified per charter; a simple manual tuner used only when a person is physically present is acceptable if the EFHW length alone doesn't cover all desired bands, but default plan is a resonant/near-resonant EFHW length with no tuner |
| Low-end attachment | Wall bracket/standoff on the shack exterior (fixed structure — no tree-sway tensioning needed) | 🔎 confirm bracket location, standoff distance from the wall, and hardware rating |
| High-end attachment (mast top) | Standoff arm/bracket offset from the VHF/UHF vertical's active element and coax, per §2b | 🔎 mechanical detail + post-install VHF/UHF interaction check |

---

## 6. Open questions / verification & tuning tasks

| Item | What's needed | Owner |
|---|---|---|
| Target HF band(s) | Operating priorities decision | Owner / operator |
| Horizontal run length (mast to shack) | Field measurement | 🔎 field-verify (private geometry) |
| Total wire length | Derived from band + measured geometry, then trimmed/tuned | 🔎 field-verify + tune |
| Shack-wall attachment hardware (bracket, standoff, mounting) | Site walk — confirm location, clearance, hardware rating | 🔎 field-verify |
| Consolidated vs. separate arrestor at the feed/entry point | Confirm single common ground buss for feed-point + bulkhead entry; check code considerations for antenna hardware mounted on the dwelling | 🔒 `grounding-safety-inspector` |
| Mast-top standoff arm for the HF wire's high end (§2b) | Mechanical design — offset from VHF/UHF vertical, materials | 🔎 design + field-verify |
| VHF/UHF-to-HF-wire decoupling check | Bench/field SWR (or equivalent) check of the VHF/UHF vertical with the HF wire installed vs. disconnected | 🔎 post-install RF test |
| Unun ratio / matching component | Select once band(s) and measured feedpoint impedance are known | 🔎 verify at install |
| Counterpoise count/length | Tune at install with analyzer | 🔎 tune |
| Pattern/takeoff modeling incl. proximity to the house | Basic NEC-style model using **real** site heights/terrain/structure, once run length is fixed | ⏸ nice-to-have, **private-side only** (real geometry) — not required to proceed with first build |
| RF acceptance checks | Continuity, insulation resistance, SWR sweep across target band(s), arrestor ground-path continuity, connector weatherproofing, basic RFI check near the house | 🔎 to be captured in a future `checklists/rf-test.md` |

---

## 7. Scope check

- Stays within first-build HF scope: **one** wire system, feedpoint/arrestor/counterpoise plan
  near a single accessible point, coax returns to the shack through bonded surge protection, no
  tuner automation, no second/experimental wire.
- Nothing here proposes a rotator, beam, remote transmit radio, or remote/automatic tuner. If a
  remote tuner is later requested to cover more bands from one wire length, route that request
  through `scope-warden` for a documented justification before adding it.
- Modeling with real site geometry (§6) is a private-side, non-blocking nice-to-have — flagged so
  it isn't confused with a first-build requirement.

---

## Related

- `docs/safety-grounding-bonding.md` — single-point-ground / bonded-entry discipline (applies to
  the feed-point ground referenced in §2, §5–6, now co-located with the shack entry).
- `docs/milestones.md` — schedule context.
- Sub-agents: `grounding-safety-inspector` (feed/entry bonding, §2, §5), `scope-warden`
  (tuner/backlog calls), `geospatial-privacy-steward` (before any real-geometry modeling artifact,
  including anything referencing the house-to-mast relationship in more detail, is considered for
  publication).
