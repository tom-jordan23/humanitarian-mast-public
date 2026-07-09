# Frame Relocation — Bonding Checklist

```yaml
classification:
  visibility: public-safe
  geospatial_sensitivity: none
  contains_real_coordinates: false
  contains_real_parcel_geometry: false
  contains_identifiable_imagery: false
  safe_for_public_repo: true
```

**Use:** every time a relocatable power frame (primarily the **experimentation frame** — see
"Which frame does this apply to" below) is moved to a new location on site and before it is
re-energized there. **Source of truth for the underlying requirement:**
`docs/safety-power-frames-bonding.md` §4 ("Relocatability vs. permanent grounding — the key
tension"). This checklist operationalizes that document's 5-step procedure and STOP list into a
field-usable form; it does **not** add new safety requirements or code citations beyond what that
document states.

> 🔒 **STOP conditions.** Do **not** energize a relocated frame until every 🔒 item below is
> satisfied and signed off. A frame bonded only to a fresh, standalone ground rod is **not
> grounded** in the sense this project requires — it is the isolated-ground-island failure mode
> Prime Directive 1 exists to prevent, and it can create a dangerous potential difference relative
> to the mast/premises system during a fault or nearby lightning strike.

---

## Which frame does this apply to

| Frame | Relocation bonding status |
|---|---|
| **Experimentation frame** | 🔒 **This checklist applies in full, every time it is moved.** It is the frame the two-frame architecture explicitly designed to be relocatable — its bonding must move with it, safely, every time. |
| **Isolation frame** | Normally sited at the mast base and its bond is installed as a **permanent run** to the mast-base bonding point, not re-executed per move (`docs/safety-power-frames-bonding.md` §4). If the isolation frame is ever genuinely relocated away from that permanent bond, treat it the same as the experimentation frame and run this full checklist — do not assume its "fixed" status still applies. |

---

## 1. Identify the bonding path back to the single site ground system (Step 1)

- [ ] 🔒 Confirmed **which** bonding path this move will use — one of:
  - [ ] **(a) A pre-existing fixed bonding point/bus** already tied into the site's single-point
        grounding electrode system (e.g., the mast-base bonding point, or another pre-installed
        bonding bus), **or**
  - [ ] **(b) An electrician-specified supplementary grounding electrode**, installed **only**
        because the new location is genuinely far from any existing bonding point, and **bonded
        back to the main system** — never left as a standalone rod (see STOP list, item 1).
- [ ] Recorded which option (a or b) was used, and where, for the as-built/commissioning record.

## 2. Never rely on a standalone freshly-driven rod (Step 2)

- [ ] 🔒 Confirmed the bonding conductor from this location's ground reference (rod, bus, or
      structure) **physically ties back to the same single-point site grounding electrode system**
      the mast, coax entry, AC service, and both power frames use — not a separate, unbonded
      electrode.
- [ ] 🔒 If a new rod was driven at this location for any reason, confirmed it is **bonded to the
      main system** before being relied on for anything — a freshly-driven rod that is not bonded
      back is **not** an acceptable ground for this project, even temporarily.

## 3. Verify continuity before energizing (Step 3)

- [ ] 🔒 AC equipment-grounding-conductor (EGC) continuity verified with a test instrument
      (experimentation frame — AC-fed).
- [ ] 🔒 DC bonding continuity verified with a test instrument (isolation frame, or any DC bonding
      conductor on the experimentation frame's DC-out branches).
- [ ] 🔒 Single-point-ground continuity confirmed — this location's bond reads back to the same
      system as the mast/coax entry, with **no second/isolated path**.

## 4. Verify bulkhead seals post-move (Step 4)

- [ ] 🔒 Every weathertight bulkhead entry disturbed by the move re-inspected and confirmed sealed:
  - [ ] AC inlet bulkhead (experimentation frame)
  - [ ] DC-out bulkhead(s) (Powerpole or equivalent)
  - [ ] Sensor/signal/telemetry/camera bulkhead gland(s)
  - [ ] Bonding-conductor bulkhead stud/feedthrough — **separate** from the AC/DC/signal glands,
        per `docs/safety-power-frames-bonding.md` §3
- [ ] 🔒 No cable gland reused incorrectly or left loose — a relocated frame is exactly when this
      happens; check each one individually, don't assume "it was fine before the move."

## 5. Sign-off before energizing (Step 5)

- [ ] 🔒 Sign-off obtained before re-energizing at the new location (who signs off is an
      operational decision — record name/role here, not prescribed by this checklist).
- [ ] Date, location description (generalized/relative — no coordinates in the public record),
      and bonding path used (Step 1, option a or b) recorded for the as-built log.

**Sign-off:** ______________________  **Date:** __________  **Bonding path used (a/b):** ______

---

## STOP — call the electrician / AHJ if…

Pulled directly from `docs/safety-power-frames-bonding.md` §7 ("STOP — professional review
required"). Do not self-resolve any of these in the field:

- [ ] ⚠️ A **supplementary grounding electrode** is needed at the new location because no
      pre-existing fixed bonding point is reachable — **licensed electrician**.
- [ ] ⚠️ The experimentation frame's AC feed at the new location will be wired as a
      **subpanel/detached-structure feeder** rather than a simple branch circuit — neutral-ground
      bonding rules differ and must not be assumed — **licensed electrician**.
- [ ] ⚠️ Any new grounding-electrode design, bonding-conductor sizing, or single-point-ground
      verification is needed that isn't already covered by an existing, previously-verified
      bonding point — **licensed electrician / `grounding-safety-inspector`**.
- [ ] ⚠️ The new location requires **trenching or burial** for an AC feed or bonding-conductor run
      — utility locate (811 / local equivalent) required **first**, see `checklists/pre-dig.md`.
- [ ] ⚠️ The new location's siting interacts with mast/guy/foundation geometry (e.g., near guy
      anchors or the mast strike zone) — **structural engineer / tower professional**, cross-check
      `docs/safety-grounding-bonding.md`.
- [ ] ⚠️ Local code edition, permit requirements, or inspection sign-off for the new location are
      unclear — **local AHJ**. Do not assume the prior location's permit/sign-off carries over.

If any box in this section is checked, **do not energize** until the flagged professional has
signed off.

---

## Open questions (not settled by this checklist — do NOT invent answers)

| Question | Status | Owner |
|---|---|---|
| How many fixed bonding points does the site need for the experimentation frame's realistic relocation range (mast base only, or additional pre-installed bonding buses elsewhere)? | ❓ open, per `docs/safety-power-frames-bonding.md` §4 | Electrician + site design |
| Who is authorized to perform the Step 5 sign-off (owner, electrician, or either)? | ❓ open, operational decision | Owner |
| Bonding stud/feedthrough fitting model, conductor gauge, torque value for the bulkhead bonding penetration | 🔎 field-/pro-verify, not invented here | Electrician, per fitting manufacturer spec |

---

## Related

- `docs/safety-power-frames-bonding.md` §3–§4 — source of truth for this checklist's requirements
  (bonding rule, per-location procedure, STOP list). This checklist does not modify that content.
- `docs/safety-grounding-bonding.md` — site-wide single-point-ground philosophy.
- `checklists/pre-dig.md` — utility locate, required before any trenching for a relocated frame's
  AC feed or bonding-conductor run.
- `pi-field-station/experimentation-frame/README.md` §7 — frame relocatability design (bulkhead
  couplings make relocation a disconnect/move/reconnect operation).
- `pi-field-station/power/README.md` §8 — isolation-frame placement (normally fixed at the mast
  base; see "Which frame does this apply to" above).
- Sub-agents: `grounding-safety-inspector` (owner of the underlying safety requirement),
  `field-docs-writer` (this checklist).
