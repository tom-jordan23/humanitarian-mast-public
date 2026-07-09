---
classification:
  visibility: public-safe
  geospatial_sensitivity: none
  contains_real_coordinates: false
  contains_real_parcel_geometry: false
  contains_identifiable_imagery: false
  safe_for_public_repo: true
---

# Safety Requirements — Two-Frame Outdoor Power Architecture (Bonding & Grounding)

> 🔒 This document sets **grounding, bonding, AC-safety, and surge-coordination requirements** for
> the two-frame outdoor power architecture. It is written by `grounding-safety-inspector` and does
> **not** edit or restate the power/load engineering owned elsewhere
> (`pi-field-station/power/README.md`, scope rulings in `docs/scope-ruling-dc-power-node.md`). Where
> this document and those disagree on load/architecture *content*, those documents are the source
> of truth for power engineering; this document is the source of truth for grounding/bonding/AC
> safety. Reconcile any conflict with `field-station-engineer` and `scope-warden`.

> ⚠️ Two permanently-energized, AC-powered outdoor enclosures hosting multiple experiments
> (including IP cameras and weather instruments) touch items CLAUDE.md lists as **deferred
> backlog** (camera sprawl, multiple experimental RF services, high-power AC loads). This document
> does not rule on that — it is a `scope-warden` question — but it is flagged here so the tension
> isn't silently absorbed into a "just grounding" doc.

Legend: 🔒 safety requirement · 🟢 settled pattern · 🔎 field-verify · ❓ open question ·
⚠️ pro-review required · ⏰ sequencing/timeline requirement

---

## 1. Architecture overview (as given)

| Frame | Power | Exposure | Load pattern | Likely siting |
|---|---|---|---|---|
| **Experimentation frame** | AC | Full outdoor weather exposure, permanent | Multiple concurrent experiments (Pis, IP cameras, weather instruments) | Flexible/relocatable |
| **Isolation frame** | 12V DC, solar + battery | Full outdoor weather exposure, permanent | One experiment at a time | Likely mast base (proximity to mast grounding electrode system) |

Both are **discrete, self-contained, weathertight enclosures**. All power and sensor connections
between a frame and the outside world (mains feed, PV leads, antenna/sensor cabling, bonding
conductor) pass through **weathertight bulkhead fittings** — not open cable entries.

This is a **permanent, grounded, structural mast site** (CLAUDE.md, `docs/safety-grounding-
bonding.md`). Nothing about "field flexibility" changes that — see §4, which is the core of this
document.

---

## 2. Outdoor AC safety — experimentation frame 🔒

| Requirement | Pattern | Status |
|---|---|---|
| **Ground-fault protection** | GFCI (NEC terminology) / RCD-class protection on the circuit(s) feeding this frame — at the breaker or at the first outdoor receptacle, per the electrician's design | 🔒 required pattern; exact device/placement = ⚠️ electrician |
| **Wet-location rating** | Receptacles rated for **wet location while in use** (in-use/"bubble" covers, not just "while closed"), enclosure body and AC entry fitting rated for continuous outdoor exposure | 🔒 required; specific NEMA/IP rating = ⚠️ electrician, verify against local code |
| **Local AC disconnect** | A readily accessible, clearly labeled AC disconnect **at or near the frame**, so the frame can be fully de-energized on site without a trip back to the house panel — important given storm-shutdown procedure and given the frame may be relocated (see §4) | 🔒 required; disconnect type/rating/lockout provision = ⚠️ electrician |
| **AC equipment-grounding conductor (EGC)** | The AC feed to the frame must carry its own EGC, bonded back to the **same premises grounding electrode system** the mast uses — not a separate/local ground rod substituting for the EGC | 🔒 required, ties directly to Prime Directive 1 (no isolated ground islands) |
| **Feeder/subpanel bonding nuance** | If the frame is fed as a **subpanel/detached-structure feeder** (vs. a simple branch circuit), neutral-and-ground bonding rules for detached structures differ from a main service panel — **do not assume the same bonding practice**. This must be determined by the electrician for the actual feed method chosen. | ⚠️ electrician — flag explicitly, common source of miswiring |
| **Conductor/conduit method for the feed run** | Buried, direct-burial-rated cable vs. conduit; burial depth; conduit fill; UV-rated jacket for any exposed run | ⚠️ electrician; 🔎 utility locate before any digging (`checklists/pre-dig.md`) |
| **Overcurrent protection sizing** | Branch/feeder ampacity, breaker size, wire gauge for the actual connected load | ⚠️ electrician — do not size from assumed load figures in this document |
| **Bonding within the enclosure** | If the enclosure body is metal, bond it to the AC EGC; keep AC wiring physically separated from low-voltage DC/sensor wiring inside the enclosure | 🔒 required pattern |

**⚠️ STOP — this entire section is licensed-electrician and local-AHJ territory.** Circuit sizing,
device selection, feeder method, permit requirements, and inspection sign-off are not settled by
this document and must not be treated as such.

---

## 3. DC + enclosure bonding — single-point, no ground loops 🔒

**Rule:** both frames, the PV panel frame/rack, and the DC-negative reference all bond into the
**same single site/mast grounding electrode system** described in `docs/safety-grounding-
bonding.md`. There is **one** coordinated ground for the whole site — mast, coax entry, AC service,
and both power frames. No frame gets its own independent ground rod that isn't bonded back into
that one system (that is precisely the "isolated ground island" Prime Directive 1 prohibits, and it
creates ground-potential-difference risk during a strike/fault, not just a code violation).

| Item | Requirement | Owner |
|---|---|---|
| Isolation frame DC-negative / system-ground reference | Bonds to the single-point site ground — same system as mast, not a separate electrode | ⚠️ electrician / `grounding-safety-inspector` |
| PV panel frame/rack (isolation frame) | Equipment-grounding conductor bonded to the same system | ⚠️ electrician |
| Experimentation frame enclosure body + AC EGC | Bonds to the same system (this is normally automatic if fed correctly per §2, but verify — don't assume) | ⚠️ electrician |
| Both frames' bonding conductors | Terminate at a common, inspectable bonding point/bus tied to the mast/premises grounding electrode system — not two unrelated paths to "ground" | 🔒 verify at commissioning, single-point continuity test |

### Bonding through a weathertight bulkhead — practice pattern

To carry a bonding conductor through an enclosure wall **without breaching the IP rating**:

- Use a **dedicated bonding stud/lug feedthrough** (a fitting purpose-built to pass a conductor
  through a sealed wall while maintaining a gasketed/compressed seal) — not an improvised hole, not
  sharing a cable gland meant for signal or power wiring.
- Keep the bonding penetration **separate** from AC and DC/data cable-gland penetrations so a
  ground fault or bonding-conductor movement can't disturb an unrelated seal.
- Provide an accessible **test/inspection point** at or near the bulkhead stud so continuity can be
  verified without opening the enclosure.
- Specific stud size, torque value, gland/fitting model, and gasket material are **not specified
  here** — 🔎 select and verify per the fitting manufacturer's spec and the electrician's sign-off.

**❌ Do not invent** bonding-conductor gauge, lug torque, or fitting part numbers. These are
field-/pro-verified items, recorded once determined.

---

## 4. Relocatability vs. permanent grounding — the key tension 🔒

**The conflict, stated plainly:** "totally field-flexible / relocatable" is in direct tension with
"permanent single-point grounding electrode system." A frame that moves cannot literally keep the
same physical grounding-electrode connection it had at its last site. Left unresolved, this
tension is exactly how a well-intentioned relocatable design ends up either (a) run temporarily
ungrounded "just for now," or (b) bonded to a hastily-driven local rod that is never tied back to
the main system — both are the isolated-ground-island failure mode Prime Directive 1 exists to
prevent.

**Resolution scheme — what's permanent vs. what's a documented procedure:**

| Element | Status | Rationale |
|---|---|---|
| **The mast-base bonding point itself** (the physical connection into the single-point site grounding electrode system, near/at the mast base) | 🟢 **Permanent.** Designed and installed once, jointly with the mast/shack grounding work (§6). This does not move even if what's plugged into it changes. | Prime Directive 1 requires one coordinated system; the mast base is where the electrode work already happens. |
| **Isolation frame**, sited at the mast base | 🟢 **Treated as effectively fixed for bonding purposes.** Even if the enclosure hardware is technically movable, its bonding conductor to the mast-base point is installed as a permanent run, not a per-move procedure. | It's *likely* sited at the mast base specifically for this reason — don't undermine that by treating its bond as ad hoc. |
| **Experimentation frame**, genuinely relocatable around the site | ❓ **Requires a documented per-location bonding procedure**, executed every time it is moved (see below) — not a permanent hardwired bond. | This is the frame the architecture explicitly wants to move; its grounding must move with it, safely, every time. |

**Per-location bonding procedure (required content, to be developed as a checklist — see
"Related"):**

1. Before energizing at a new location, identify the bonding path back to the **single site ground
   system** — either (a) a pre-existing fixed bonding point/bus already tied into that system, or
   (b) if genuinely far from any existing bonding point, an electrician-specified supplementary
   grounding electrode that is itself **bonded back to the main system** (never left as a standalone
   rod).
2. **Never treat a freshly-driven ground rod as sufficient on its own.** A local rod that is not
   bonded to the single-point system is, by definition, the isolated-ground-island pattern this
   project prohibits — it can create a dangerous potential difference relative to the mast/premises
   system during a fault or nearby strike.
3. Verify AC EGC continuity and DC bonding continuity with a test instrument before energizing.
4. Verify all bulkhead entries (AC, DC, sensor, bonding) are correctly sealed post-move — a
   relocated frame is exactly when a gland gets reused incorrectly or left loose.
5. Sign-off step before energizing at the new location (who signs off = operational decision, not
   set here).

This procedure is a **field-replicable-safety pattern**, the same category of artifact as
`checklists/pre-dig.md` or `checklists/mast-raise.md` — it has its own checklist rather than
living only as prose here: `checklists/frame-relocation-bonding.md` (produced by
`field-docs-writer`, operationalizing the five steps above). The bonding-point-inventory question
below remains open and is carried in that checklist as a field-verification task, not invented.

**❓ Open design question, not settled by this document:** how many fixed bonding points does the
site need for the experimentation frame's likely relocation range (one at the mast base only, or
additional pre-installed bonding buses at other likely locations)? This is a joint decision for
the electrician and site design, informed by where the frame is actually expected to move.

---

## 5. Surge / lightning coordination 🔒

| Item | Requirement | Owner |
|---|---|---|
| PV-input surge protection | DC-rated SPD on the isolation frame's PV leads at the point of enclosure entry | ⚠️ electrician / vendor spec |
| AC surge protection | SPD on the AC circuit feeding the experimentation frame (and/or at the panel/disconnect) | ⚠️ electrician |
| Coordination with existing mast/coax surge protection | All protective devices — coax entry arrestors, HF feedpoint arrestor, AC SPD, PV SPD — must reference the **same bonded ground system**, per `docs/safety-grounding-bonding.md`'s "bond, then protect" principle. Do not design these in isolation from each other. | 🔒 design coordination; ⚠️ electrician for device selection |
| Routing cautions | Keep AC/DC power runs and sensor/camera cabling **away from and not parallel to** mast guy wires, the grounding/bonding conductors, and HF counterpoise/radial conductors — minimize induced-coupling and strike-pathway risk. Cross conductors near-perpendicular where unavoidable; keep clear of the mast's likely strike zone. | 🔒 layout requirement; coordinate with `rf-antenna-engineer` on counterpoise/radial geometry |
| Camera/sensor cabling on the experimentation frame | Avoid routing near the HF feedpoint/arrestor or mast-base counterpoise field | 🔎 verify against actual cable routing once frame siting is fixed |

---

## 6. Timeline dependency — hard sequencing requirement ⏰

- The bonding point(s) described in §3–§4 **must be designed jointly with the mast/shack
  single-point ground during the August–September 2026 grounding work** (`docs/milestones.md`:
  August "Grounding electrode and bonding materials," September "Bonding and grounding" — the
  hard **Sept 30, 2026 mast-standing-and-bonded checkpoint**).
- **Install once, not retrofit.** The physical bonding bus/point both frames tie into should be
  planned during the July scope-freeze work, built alongside the mast-base electrode work in
  August, and verified together with mast bonding in September — not added later as a separate
  trip.
- **Sequencing risk to flag now:** if either frame's construction or siting gets ahead of the
  grounding design (e.g., the isolation frame enclosure is built/sited before the mast-base
  bonding point is finalized), the site risks exactly the retrofit/isolated-ground scenario this
  document exists to prevent. **Do not finalize frame siting or pour any foundation/mounting
  point for the isolation frame before the mast-base grounding design is settled.**
- The experimentation frame's AC feed routing (§2) also has a **utility-locate dependency** —
  coordinate with `checklists/pre-dig.md` before any trenching for the AC feed or bonding
  conductor run.

---

## 7. STOP — professional review required

| Area | Professional | Why |
|---|---|---|
| AC circuit design, GFCI placement, feeder/subpanel bonding, wet-location device selection, permit filing | **Licensed electrician** | §2 — outdoor permanent AC power is code-governed; do not self-design |
| Neutral-ground bonding method if the experimentation frame is fed as a detached-structure subpanel | **Licensed electrician** | §2 — a common and consequential miswiring point |
| Grounding electrode design, bonding-conductor sizing, single-point-ground verification for both frames | **Licensed electrician / `grounding-safety-inspector`** | §3, §4 — must tie into the same system as the mast |
| Supplementary grounding electrode for a relocated experimentation frame, if a fixed bonding point isn't available at a new location | **Licensed electrician** | §4 — must be bonded to the main system, never left standalone |
| PV and AC surge-protective-device selection and installation | **Licensed electrician** | §5 |
| Mast/guy/foundation structural coordination if frame siting or trenching interacts with guy anchor geometry | **Structural engineer / tower professional** | Cross-reference `docs/safety-grounding-bonding.md` structural section |
| Local code edition, permit requirements, inspection sign-off for outdoor AC installation and any detached-structure feeder | **Local AHJ** | Not asserted anywhere in this document — verify locally |
| Utility locate before any trenching for AC feed, bonding conductor, or frame foundation work | **811 / utility locate service** | Standard pre-dig requirement, see `checklists/pre-dig.md` |

---

## 8. Verification tasks (collected)

| # | Task | Ties to |
|---|---|---|
| 1 | Confirm AC feed method (branch circuit vs. subpanel/feeder) and resulting neutral-ground bonding rules | §2 |
| 2 | Select GFCI device type/placement, wet-location receptacle/enclosure ratings, AC disconnect rating | §2 |
| 3 | Confirm conductor/conduit method and burial depth for the AC feed run | §2 |
| 4 | Select bonding stud/feedthrough fitting and conductor gauge for the weathertight bulkhead bonding path | §3 |
| 5 | Determine how many fixed bonding points the site needs to support the experimentation frame's real relocation range | §4 |
| 6 | ~~Develop `checklists/frame-relocation-bonding.md` from the 5-step procedure in §4~~ — **done**, see that checklist | §4 |
| 7 | Select PV-input DC SPD and AC SPD models, coordinated with existing coax/HF arrestor plan | §5 |
| 8 | Confirm actual cable routing (AC, DC, sensor/camera) clears the mast counterpoise/radial field and HF feedpoint | §5 |
| 9 | Confirm mast-base bonding point design and schedule against August/September grounding work before any frame foundation work | §6 |
| 10 | Utility locate before any trenching for AC feed or bonding conductor runs | §6, `checklists/pre-dig.md` |

---

## 9. Pre-energize / commissioning checklist (stub)

- [ ] 🔒 Single-point-ground continuity verified for **both** frames — no second/isolated path
- [ ] 🔒 AC EGC continuity verified on the experimentation frame's feed
- [ ] 🔒 GFCI/RCD protection tested (test button / trip test) on the experimentation frame circuit
- [ ] 🔒 AC disconnect located, labeled, and confirmed to fully de-energize the frame
- [ ] 🔒 All weathertight bulkhead entries (AC, DC, sensor, bonding) inspected and sealed
- [ ] 🔒 PV and AC SPDs installed and referencing the same bonded ground as the mast/coax entry
- [ ] 🔎 Cable routing checked against mast counterpoise/radial and HF feedpoint clearance
- [ ] ⚠️ Electrician / AHJ sign-off obtained where required
- [ ] 🔒 If experimentation frame has been relocated since last commissioning: full per-location
      bonding procedure (§4) re-executed and signed off

This is a **stub for expansion into a standalone checklist** (`field-docs-writer` ownership) once
device/product specifics are settled — do not treat it as complete.

---

## Related

- `docs/safety-grounding-bonding.md` — site-wide single-point-ground philosophy this document
  extends to the two power frames.
- `pi-field-station/power/README.md` — DC power/load engineering (isolation-frame-class 12V
  architecture); this document adds grounding/bonding/AC-safety requirements on top of, not in
  place of, that spec.
- `docs/scope-ruling-dc-power-node.md` — scope reasoning for the DC power node; note the
  camera/multiple-experiment flag in this document's header if reconciling scope.
- `checklists/pre-dig.md` — utility locate requirement, applies to any trenching for AC feed or
  bonding runs.
- `checklists/frame-relocation-bonding.md` — field checklist operationalizing the §4 per-location
  bonding procedure and the §7 STOP list; created by `field-docs-writer`, not by this document.
- Sub-agents: `grounding-safety-inspector` (this document's owner), `field-station-engineer`
  (power/load content), `rf-antenna-engineer` (counterpoise/radial routing coordination),
  `scope-warden` (camera/multiple-experiment scope flag), `field-docs-writer` (checklist
  production).
