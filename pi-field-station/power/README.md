---
classification:
  visibility: public-safe
  geospatial_sensitivity: none
  contains_real_coordinates: false
  contains_real_parcel_geometry: false
  contains_identifiable_imagery: false
  safe_for_public_repo: true
---

# 12V DC Solar Power Node — ISOLATION FRAME (Solar/Battery Certification)

> **"One-and-done" testbed spec — ISOLATION FRAME.** This is the DC power architecture for the
> **isolation frame**: a discrete, solar/battery-powered, single-experiment field enclosure that
> **certifies field-readiness** under real solar/battery/weather conditions. It hosts the
> first-build **edge services** (exactly **one Raspberry Pi 5**, environmental sensors,
> lighting-controller logic, fiber termination, telemetry) as its current payload. It is
> explicitly **not** sized to
> power a transmit radio — the QRP rig is battery-powered separately and is **not** on this bank.
> Geometry/siting statements here are generalized ("full southern sun," "between a willow and a
> birch") — no coordinates, parcel geometry, or address content.

## Two-frame architecture (owner decision — settled 🟢)

The DC power design is split across **two physically separate, discrete, weathertight
enclosures**. This document specifies the **isolation frame only**. The companion frame is
specified separately:

| Frame | Power | Enclosure | Role | Doc |
|---|---|---|---|---|
| **Isolation frame** (this doc) | Solar + battery, 12V | Discrete, weathertight, small | **ONE experiment/payload at a time.** Certifies field-readiness under real solar/battery/weather. | `pi-field-station/power/README.md` |
| **Experimentation frame** | AC-powered, no power limits | Discrete, weathertight, larger, deliberately weather-exposed | **3–4 concurrent experiment bays** (1 power-intensive Jetson-class + 2–3 lower-power Pi 5) — a lab bench, explicitly **NOT field-validated**. | `pi-field-station/experimentation-frame/README.md` |

**Graduation gate (🟢 settled):** an experiment is developed and matured in the experimentation
frame → it is ported into the isolation frame as a **single 12V load** through the isolation
frame's defined **weathertight experiment port** (§0A) → it is then certified under real
solar/battery/weather conditions. Nothing is considered "field-validated" until it has passed
through this gate. The isolation frame's current payload — the first-build edge-service bundle
(exactly one Pi 5, sensors, lighting-controller logic, fiber termination, telemetry) — is treated
as the baseline occupant of that single-experiment slot; the load table in §1 documents that
payload.

**Jetson-class compute is explicitly out of scope for this frame.** The experimentation frame is
authorized to host Jetson-class edge-AI hardware (NVIDIA Jetson — several to tens of watts per
module); this isolation frame's battery/array/distribution is **not** sized for that load class
and must not be assumed compatible with it. Only a drastically power-managed, individually
certified, single-experiment variant could ever be considered here in the future — a deferred,
unlikely question, not a first-build design target. See
`pi-field-station/experimentation-frame/README.md` §0 and §1.

Legend: 🟢 settled · 🔧 assumption (typical/example value — verify) · 🔎 field-verify (measurement/
test task) · ❓ open question · 🔒 safety requirement · ⚠️ pro-review (electrician / structural /
`grounding-safety-inspector`) · ⏸ deferred / do-not-buy-yet

---

## 0A. Governing design law — discrete enclosure & weathertight bulkhead coupling

**Applies to both frames** (isolation and experimentation). This is the architecture-level rule
this document and its companion must both satisfy:

1. **Discrete, self-contained, weathertight enclosure.** Each frame is its own sealed box — not a
   shared chassis, not an open rack, not a shelf inside another enclosure. See §7 for the
   isolation frame's enclosure spec.
2. **Every power and sensor coupling passes through a weathertight bulkhead — no ad-hoc
   pass-throughs.** No drilled holes with silicone, no cable pushed through a compression fitting
   improvised in the field. Every conductor crossing the enclosure wall uses a rated bulkhead
   connector or a rated cable gland selected for that signal class.

| Coupling | Direction | Example bulkhead hardware (🔧 typical/example — verify before purchase) |
|---|---|---|
| DC in, from PV array | Enclosure wall in | IP-rated circular connector (e.g., M12/circular-DIN-style locking connector rated for outdoor PV-side current), **or** a sealed cable gland (IP68-rated, PG/NPT thread) if the PV leads are directly terminated inside | 🔧 example only |
| DC out, to the load bus / experiment | Enclosure wall out | **Bulkhead-mount Anderson Powerpole** panel connector (keeps the Powerpole standard from §5 continuous across the enclosure wall) | 🔧 example only |
| Sensor / signal / telemetry lines | Enclosure wall, either direction | Sealed cable gland (IP68-rated) per cable, **or** a multi-pin IP-rated circular connector if several signal lines are grouped | 🔧 example only |
| AC in (experimentation frame only — N/A to this isolation-frame doc) | — | See `pi-field-station/experimentation-frame/README.md`; AC-safety hardware selection is deferred to `grounding-safety-inspector`, not decided here | ⚠️ pro-review |

3. **Defined weathertight experiment port (isolation frame's single-payload interface) — one bay
   of the shared cross-frame module interface.** The isolation frame's "one experiment at a time"
   rule is implemented as **one defined bulkhead DC output**, and that port is now formally **the
   same standardized "Experiment Module" interface** the experimentation frame uses for its 3–4
   backplane bays — see `pi-field-station/experimentation-frame/README.md` §3B for the full
   interface definition (connector set, rail classes, mechanical/thermal envelope). This isolation
   port is specifically **one QRP-solar-class bay instance** of that shared interface — not a
   bespoke port. Today it feeds the fixed first-build edge-service bundle (§1); a future graduated
   experiment (§ Two-frame architecture, above) connects through the **same port**, swapped, not
   added alongside it, *provided it is a QRP-solar-class module* (see the compatibility row
   below). See §5 for the distribution-side detail and the port's fusing.

| Experiment port spec | Value | Status |
|---|---|---|
| Interface standard | One bay of the shared cross-frame **Experiment Module interface** — see `pi-field-station/experimentation-frame/README.md` §3B | 🟢 settled, cross-referenced |
| Rail class delivered | **Regulated 5V DC** (QRP-solar-class — matches the experimentation frame's §2B Pi-class rail), sourced from this enclosure's own 12V→5V buck converter (§5, §11 BOM item 12) — the buck converter's output *is* the experiment port's supply, the Pi 5 is simply today's occupant | 🟢 settled — reframes the buck converter as the port's regulated source, not a Pi-only accessory |
| Connector set | **Powerpole (PP-series, same shell family used throughout both frames)** for DC power + **RJ45** (to the internal network switch/fiber media converter) + a small keyed **signal connector** (telemetry/status lines) — identical positions/types to an experimentation-frame Pi-class bay, so a QRP-solar-class module is physically plug-compatible in both places | 🟢 settled pattern, per §3B |
| Compatibility | **QRP-solar-class modules only.** This port does **not** provide the experimentation frame's 12–19V Jetson-class rail (§2A) or any active heat rejection — an intensive-class (Jetson) module is **not** compatible here and stays experimentation-only, consistent with the existing graduation-gate rule | 🔒 required constraint, per §3B compatibility matrix |
| Payload today | First-build edge-service bundle (exactly one Pi 5, sensors, lighting-controller logic, fiber termination, telemetry) — see §1 load table | 🟢 settled |
| Swap behavior | **Insert-then-switch, no live hot-swap** (matches the experimentation-frame backplane's rule, §3A): de-energize via the port's switch, disconnect at the bulkhead, swap, reconnect, re-energize — no enclosure-internal rewiring required | 🟢 settled design intent |
| Rated current | Sized to the branch fuse selected in §5 (🔧 example convention, not a final number) | 🔎 verify once actual port hardware is selected |

4. **Total field flexibility — both frames are relocatable modules.** Neither frame is
   permanently plumbed into a fixed site location by design. Each is a self-contained enclosure
   that can be disconnected at its bulkheads and physically relocated. §8 gives a **default/
   primary placement recommendation** for the isolation frame, not a fixed requirement.

---

## 0. Scope boundary

- **In scope:** DC power generation (solar), storage (LiFePO4), conversion, distribution,
  protection, and telemetry for the field enclosure's edge services.
- **Compute population constraint (🔒 settled, owner decision): ≤ 1 Pi in the isolation frame.**
  Exactly **one Raspberry Pi 5** is the compute payload here — this reinforces the
  one-experiment-at-a-time discipline in §0A. Multiple concurrent Pi/Jetson-class compute is the
  experimentation frame's job (`pi-field-station/experimentation-frame/README.md`), not this
  frame's.
- **Not in this budget:** the QRP transmit rig (owner-carried, separate battery — the spare 8Ah
  LiFePO4 is being repurposed for that and is **deliberately excluded** from this fixed bank so we
  never mix mismatched cells), the LED lighting **fixture** load itself (only the lighting
  controller's own logic/relay draw is budgeted here — fixture current is sized later, when the
  lighting BOM is set, and added to this bus as its own fused branch), 24/7 BirdNET, cameras, LTE,
  and any solar/battery expansion beyond validating this architecture. Anything that pushes this
  node toward those items → `scope-warden`.

---

## 1. Load table & daily energy budget

All current/power figures below are **🔧 typical-value assumptions**, not measured or vendor-
verified for this build. Each has a matching verification task in §12.

**Compute pinned: exactly one Raspberry Pi 5** (owner decision, replaces the earlier Pi 4B
placeholder — see the ≤1-Pi constraint in §0). Pi 5 typical power figures are **notably higher**
than Pi 4B's in third-party published measurements (higher clocks, PCIe, faster I/O) — the figure
below is a 🔧 design assumption, not a vendor/measured number for this specific board+peripheral
combination.

| Load | Typical draw (🔧 assumption) | Duty cycle | Daily Wh (raw) |
|---|---|---|---|
| **Raspberry Pi 5**, headless (OS, SSH, logging, telemetry logger) | ~5 W avg at 5V, board-side (idle ~3.5 W, bumps under I/O/service load — higher peak than Pi 4B) | 24 h/day | ~120 Wh |
| Environmental sensor(s) (I2C temp/humidity/pressure) | <0.2 W incl. interface overhead | 24 h/day | ~5 Wh |
| Power telemetry shunt monitor (I2C, INA226-class) | ~0.03 W | 24 h/day | ~0.7 Wh |
| Lighting-controller **logic only** (relay/driver control board — **not** the LED fixture load, sized separately) | ~0.5 W standby/logic | 24 h/day | ~12 Wh |
| Fiber media converter (field-box end of the fiber run, per CLAUDE.md's fiber-preferred network) | ~2.5 W | 24 h/day | ~60 Wh |
| BirdNET mic + duty-cycled inference bump (**optional, first-build only if duty-cycled** — not 24/7) | +2.5 W above Pi baseline while active | ~3 h/day example window (dawn/dusk) | +7.5 Wh |
| **Raw subtotal — base (no BirdNET)** | | | **197.7 Wh** |
| **Raw subtotal — with duty-cycled BirdNET** | | | **205.2 Wh** |

Add a **🔧 15% system loss factor** (wiring/connector drop, DC-DC buck-converter inefficiency,
controller self-consumption — not itemized separately, folded in as a first-pass margin):

| Scenario | Raw Wh/day | +15% loss | Design Wh/day |
|---|---|---|---|
| Base (no BirdNET) | 197.7 | ×1.15 | ~227 Wh |
| With duty-cycled BirdNET | 205.2 | ×1.15 | ~236 Wh |

**Design daily energy budget: 240 Wh/day** (🔧 recalculated for Pi 5 — rounds up from the
BirdNET-included case, small margin). This **replaces the prior Pi-4B-based 210 Wh/day figure — a
delta of +30 Wh/day (≈ +14%)**, driven entirely by Pi 5's higher typical draw. See §2 for how this
recalculation was checked against the existing 50 Ah / 2-day battery sizing — **the owner has
decided not to upsize the battery now**; the existing bank still clears the 2-day target with
reduced margin, and the expansion path (§10) remains the documented route if real telemetry later
shows this margin is inadequate.

**Boundary conditions, stated explicitly:**
- 24/7 BirdNET, cameras, LTE modules, and powering the QRP rig from this bank are **not** in this
  budget. If any of those get proposed, the load table must be re-run — route the proposal through
  `scope-warden` first.
- The LED lighting **fixture** current is a separate branch to be sized once the lighting BOM
  exists (`lighting-controller/`); this bus reserves headroom for it (see §11) but does not invent
  a number for it here.
- **≤ 1 Pi constraint (§0):** this load table assumes exactly one Pi 5. A second Pi, or any
  additional concurrent compute payload, does not belong in this frame — see the experimentation
  frame instead.

---

## 2. Autonomy & battery sizing — 1-day vs. 2-day

**Design DoD assumption: 80%** for LiFePO4 (🔧 conservative design target for cycle-life margin;
LiFePO4 can technically go deeper, but 80% is a common practice figure for daily-cycling solar
service — verify against the chosen battery's datasheet).

**Formula:** `Battery Wh = Daily load Wh × autonomy days ÷ DoD`, then `Ah = Wh ÷ 12.8V nominal`
(4S LiFePO4 nominal pack voltage).

| Autonomy | Battery Wh needed | Ah needed | Nearest standard SKU | Usable Wh at 80% DoD | True autonomy at 210 Wh/day |
|---|---|---|---|---|---|
| **1-day** | 210 × 1 ÷ 0.8 = 262.5 Wh | 20.5 Ah | 25 Ah (small margin) | 25×12.8×0.8 = 256 Wh | ~1.22 days |
| **2-day** | 210 × 2 ÷ 0.8 = 525 Wh | 41.0 Ah | 50 Ah (comfortable margin) | 50×12.8×0.8 = 512 Wh | ~2.44 days |

*(Table above is the original Pi-4B-era sizing math, kept for reference — the SKU/formula logic
that follows in this section is unchanged.)*

### Pi 5 recheck — does the existing 50 Ah bank still clear the design target? (🔧 recalculated)

Re-running the same formula at the **Pi-5-adjusted 240 Wh/day** figure (§1), against the
**already-selected** 25 Ah and 50 Ah SKUs (not re-selecting new SKUs):

| Autonomy | Battery Wh needed at 240 Wh/day | Ah needed | Existing SKU | Usable Wh at 80% DoD | True autonomy at 240 Wh/day | vs. original (210 Wh/day) |
|---|---|---|---|---|---|---|
| **1-day** | 240 × 1 ÷ 0.8 = 300 Wh | 23.4 Ah | 25 Ah (still fits, thinner margin) | 256 Wh | ~1.07 days | was ~1.22 days |
| **2-day** | 240 × 2 ÷ 0.8 = 600 Wh | 46.9 Ah | 50 Ah (still fits, thinner margin) | 512 Wh | **~2.13 days** | was ~2.44 days |

**Result: the existing 50 Ah bank still meets the ≥2-day design target** (2.13 true days ≥ 2)
even with the Pi 5 delta — it just does so with less headroom than the original Pi-4B-era
estimate (2.44 days). 🔒 **Owner decision: do not upsize the battery now.** The reduced-but-still-
adequate margin is accepted; monitor real usage via telemetry (§9) and use the documented
expansion path (§10 — "add a second same-model battery in parallel") if actual field data later
shows this margin is genuinely insufficient, rather than upsizing preemptively on a 🔧 unverified
assumption. 🔎 **Verification task: measure real Pi 5 draw once hardware is in hand (in-line
meter, not the 🔧 5 W design assumption) and re-run this table with the measured figure** — see
§12.

### Cost-delta reasoning (owner's decision rule: 2-day wins if the incremental cost is small)

- The jump under consideration is **25 Ah → 50 Ah** — roughly double capacity, not double cost.
  Small-format 12V LiFePO4 units in this range typically carry a **large fixed-cost component**
  (cell-matching, BMS board, terminals, enclosure, certification) shared across the whole unit; the
  **marginal $/Ah for the larger unit is usually lower**, not higher, than for the smaller one. So
  the 50 Ah unit is very unlikely to cost 2× the 25 Ah unit — it is a market pattern, not a verified
  number for a specific vendor. 🔧 **Verification task: get real vendor quotes for both sizes before
  purchase; do not treat this reasoning as a price commitment.**
- The **engineering effort is identical either way** — same BMS integration, same fusing, same
  Powerpole distribution, same enclosure cutouts, same telemetry wiring, same grounding bond. You
  are not paying twice to "build" a 2-day system vs. a 1-day system; you are paying for more cells
  inside the same harness. That is exactly what the "one-and-done" design goal (§13) is trying to
  buy — settle the architecture once, don't revisit it later because a 1-day bank turned out to be
  thin.
- 1-day autonomy (25 Ah) leaves almost no margin (1.22 true days against a 1-day target) — one
  cloudy/snow-covered-panel day plus one below-freezing no-charge day (see §3) would already draw
  it down close to the LVD trip point. 2-day (50 Ah) gives real margin (2.44 true days) against
  exactly that combination, which is common in a Wisconsin winter.
- **Recommendation: 2-day autonomy, 50 Ah LiFePO4.** This matches the owner's expectation. The
  generator remains the fallback for anything beyond this, per the owner's stated floor — this bank
  is not being sized to eliminate generator use entirely.

---

## 3. Battery — recommendation & required BMS features

| Spec | Value | Status |
|---|---|---|
| Chemistry | LiFePO4, 12V nominal (4S, ~12.8–13.6V operating range) | 🟢 settled |
| Capacity | 50 Ah | 🟢 settled (from §2) |
| Configuration | **Single battery**, not stacked — keeps BMS/wiring simple for a first build | 🟢 settled |
| Spare 8 Ah LiFePO4 | Explicitly **excluded** — repurposed as portable/QRP battery, not mixed into this bank | 🟢 settled (owner decision) |
| BMS: over-voltage / under-voltage / over-current / short-circuit protection | Required baseline BMS functions | 🔒 safety, standard on any reputable LiFePO4 pack — verify on datasheet |
| **BMS: low-temperature charge cutoff** | Must halt charging below ~0°C (32°F) internally, regardless of what the charge controller does upstream | 🔒 **mandatory** — charging LiFePO4 below freezing causes permanent lithium-plating damage; this is a hard requirement for Wisconsin winter, not optional |
| BMS: discharge-at-low-temp behavior | LiFePO4 can typically discharge (not charge) at lower temperatures than it can charge — confirm the pack's actual discharge floor | 🔎 verify on datasheet |
| BMS communication (Bluetooth/UART/CAN reporting SoC, per-cell voltage, temperature) | Desirable for telemetry (§10) but not mandatory — a shunt-based estimate is a workable fallback | 🔧 nice-to-have, verify against selected product |

### Cold-weather placement/insulation strategy (see also §7 Enclosure)

- Default plan is **passive**: insulated enclosure liner + BMS low-temp charge cutoff as the
  control mechanism. **Do not add an active battery heater in the first build** — it adds load,
  complexity, and a new failure mode, and works against the low-idle-draw / minimal-complexity
  design standard.
- The battery lives in its own **insulated, unvented compartment**, physically separate from the
  Gore-vented electronics bay — see §7's "Thermal zoning" for why the enclosure is split this way
  (a Gore vent is an air-exchange path and would otherwise fight this insulation strategy).
- If field telemetry over a winter shows the passive approach is genuinely inadequate (e.g., the
  BMS cutoff triggers so often that the system can't stay charged through the season), that is a
  documented, justified follow-up — route it through `scope-warden` rather than adding it
  preemptively.

---

## 4. Charge controller — MPPT, sized for 200 W with headroom

| Item | Value | Status |
|---|---|---|
| Panel array | 2 × 100 W, 12V-nominal, wired in parallel | 🟢 settled (owner-approved) |
| Typical panel electrical characteristics (per-panel) | Voc ≈ 22 V, Vmp ≈ 18 V, Isc ≈ 6.1 A, Imp ≈ 5.6 A | 🔧 assumption/example — verify against the actual panel spec sheet before wiring |
| Combined array (parallel) | Isc ≈ 12.2 A, Imp ≈ 11.2 A, Vmp ≈ 18 V | 🔧 derived from above |
| Controller input sizing convention | Size continuous input ≥ combined Isc × 1.25 safety margin ≈ 15.3 A | 🔧 common low-voltage PV design convention — verify against controller datasheet and any applicable code |
| **Recommended controller rating** | **MPPT, 20–30 A, true LiFePO4 charge profile**, sized with headroom for future array growth (a 30 A-class MPPT commonly supports on the order of ~400 W PV at a 12V system voltage per typical vendor derating charts) | 🟢 settled target rating; specific product = ❓ open, example only |
| LiFePO4 charge profile | Absorption/float voltages matched to a 4S LiFePO4 pack (commonly ~14.2–14.6 V absorb / ~13.6 V float, but exact numbers are chemistry/BMS-specific) | 🔎 verify the controller's LiFePO4 preset actually matches the chosen battery's spec — do not assume the default preset is correct without checking |

**Why MPPT, not PWM:** these panels' Vmp (~18 V) sits well above the battery's operating range
(~13–14.6 V). A PWM controller would simply clamp that gap and waste the difference; an MPPT
controller tracks the panel's actual maximum-power point across temperature and irradiance and
recovers meaningfully more usable energy from the same 200 W array. At this Vmp/Vbatt gap it isn't
a close call — MPPT is the correct choice.

**Low-temp cutoff coordination:** the **BMS low-temp cutoff is the mandatory backstop** (§3) —
treat it as authoritative regardless of what the controller does. If the selected MPPT controller
supports an external battery-temperature sensor and its own temperature-compensated charging, that
is a useful **secondary** refinement, not a substitute for the BMS feature. 🔎 verify whether the
chosen controller model supports a remote temp sensor before assuming this refinement is available.

---

## 5. DC distribution

| Element | Pattern | Status |
|---|---|---|
| Connector standard | **Anderson Powerpole** throughout (battery, distribution, branch loads) | 🟢 settled — matches ham-radio field-standard practice, genderless, field-serviceable, compatible with existing 12V gear |
| Distribution topology | **Star / home-run from a central fused bus** — not daisy-chained. Each branch gets its own fused wire back to the bus. | 🟢 settled design pattern (this is what makes future branches cheap — see §13) |
| Main bus | Fused positive distribution block (blade-fuse ATC/ATO, or ANL/MIDI-class for the main feed if current warrants) at the battery output | 🟢 settled pattern; exact model = ❓ open |
| Branch fusing | Every branch (Pi buck converter, lighting-controller logic, fiber media converter, sensor bus, spare positions) individually fused close to its takeoff point | 🔒 safety pattern; common low-voltage convention is to fuse very close to the source tap (example figure often cited: within ~7 in / 18 cm) — 🔧 convention, not verified for this layout |
| Wire gauge | Select by **(a)** branch fuse/max current and **(b)** actual one-way run length, targeting ≤3% voltage drop — standard low-voltage DC ampacity/voltage-drop method | 🔎 field-verify once physical layout and cable lengths are fixed; **do not treat any single gauge as final**. Illustrative only: a short (<1 ft), ≤30 A main battery-to-bus jumper is commonly done in 10 AWG — not a spec for this build. |
| LVD (low-voltage disconnect) | Dedicated **auto-reconnect** LVD/"battery-protect" relay ahead of the load bus, independent of the BMS's internal cutoff | 🔒 required feature — protects the battery earlier than the BMS's hard cutoff, and (paired with an under-voltage warning to the Pi) allows a graceful shutdown instead of an abrupt one. Specific product = ❓ open, verify auto-reconnect voltage/hysteresis on datasheet before purchase. |
| **Experiment port termination** | The load-bus branch that leaves the enclosure does so through the **bulkhead-mount Powerpole experiment port** defined in §0A, not a bare internal terminal — this is what makes the payload swappable without opening the enclosure's internal wiring | 🟢 settled pattern, ties to §0A |

---

## 6. Grounding & surge — coordinate with `grounding-safety-inspector`

This power node's DC ground is **not a separate ground system** — it must tie into the site's
single, coordinated mast/premises ground per `docs/safety-grounding-bonding.md`. The following
items are flagged for `grounding-safety-inspector` / electrician review, not decided here:

| Item | Why it matters | Owner |
|---|---|---|
| DC negative / system-ground bonding point | Must bond to the **same single-point site/mast ground** — no separate/isolated ground rod for this power node, no ground loops | ⚠️ `grounding-safety-inspector` / electrician |
| Panel frame + mounting-rack equipment ground | Frames need an equipment-grounding conductor bonded to the same system | ⚠️ electrician |
| PV input surge protection (SPD) | DC-rated surge/lightning protection on the PV leads where they enter the enclosure — more important if the panel ends up on a run away from the enclosure (§8) | ⚠️ coordinate with the mast's coax/entry surge-protection plan |
| Enclosure metal bonding (if metal enclosure) | Bond enclosure body into the same grounding system | ⚠️ electrician |
| Single-point verification | Confirm, once the physical layout is fixed, that there is exactly **one** bonding point for this node into the site ground — no second path | 🔒 safety, verify at commissioning |

🔒 **Do not treat any grounding detail above as settled by this document.** This document only
identifies *what* must bond to the single-point system, not conductor sizes, electrode details, or
code citations.

---

## 7. Enclosure — IP66 + Gore vent baseline, thermally zoned

**Assessment: the owner's existing "small weatherproof enclosure" is very likely undersized once
the actual parts are laid out.** A 50 Ah LiFePO4 battery, MPPT controller, Pi + case, 12V→5V buck
converter, fused distribution block, LVD relay, telemetry shunt, and wiring service loops need
real interior volume plus room to inspect/disconnect/repair without fighting the box. 🔎
**Verification task: do a literal dry-fit mockup with real (or example-dimensioned) parts before
committing to an enclosure** — don't guess the existing box will work.

### Baseline strategy: IP66 cabinet + Gore protective vent (field-proven, 🟢 settled pattern)

The owner has **field-proven** this exact pattern — an IP66 cabinet fitted with a Gore protective
vent for passive pressure equalization and moisture-vapor/condensation management while preserving
the IP rating — in a prior tropical-climate deployment (Indonesia). That is a strong basis for
adopting it as the **baseline** condensation/pressure strategy here. Because the isolation frame's
electronics bay is low-power (no active cooling load, per §1's lean load table), **this is likely
the whole thermal/condensation answer for that bay** — contrast with the experimentation frame,
where a Gore vent alone is explicitly *not* sufficient for Jetson-class heat rejection
(`pi-field-station/experimentation-frame/README.md` §1).

| Requirement | Pattern | Status |
|---|---|---|
| Sizing | Bigger than the current small box — sized to fit battery + controller + Pi + distribution + wiring service loops with room to work | 🔎 verify by mockup; exact dimensions = ❓ open |
| Weatherproof rating | **IP66** outdoor-rated cabinet (field-proven baseline) | 🟢 settled target rating; specific product = ❓ open |
| **Vented, not sealed (electronics bay only — see thermal zoning below)** | **Gore protective vent** (or equivalent membrane vent) to equalize pressure/humidity without admitting rain or insects, preserving the IP66 rating — avoid an airtight gasketed box, which traps condensation | 🟢 settled pattern, field-proven by the owner in a prior tropical deployment |
| Moisture control | Desiccant packs as auxiliary control in the vented electronics bay; inspect/replace on a maintenance interval | 🟢 settled pattern; add to field-box test checklist (§13) |
| Enclosure siting relative to sun | Keep the electronics/battery enclosure **shaded** — reduces battery heat soak in summer and works with the cold-weather liner strategy. This argues for decoupling the enclosure from the panel's sun-exposure needs (§8). | 🟢 settled pattern |
| **Discrete/self-contained** | This enclosure houses **only** the isolation frame (battery, controller, distribution, one experiment payload) — no shared chassis with the experimentation frame, which is a **separate physical enclosure** (`pi-field-station/experimentation-frame/README.md`) | 🟢 settled, per §0A governing law |
| **All penetrations are bulkhead couplings** | PV DC in, load-bus DC out (experiment port), and any sensor/telemetry lines cross the enclosure wall **only** through the rated bulkhead connectors/glands in §0A — no drilled-and-siliconed ad-hoc pass-throughs | 🔒 required pattern, per §0A |

### Wisconsin-winter deltas vs. the tropical baseline (the new/unproven part)

The tropical field-proof covers moisture/humidity/pressure. It does **not** by itself cover
sub-freezing operation — that is new territory for this pattern and needs explicit design
attention, not an assumption that "it worked in the tropics, so it'll work here."

| Delta | Risk | Mitigation | Status |
|---|---|---|---|
| Vent low-temperature rating | Some membrane vents lose function or become brittle at deep cold | 🔎 **Verify the specific selected vent's low-temp rating before purchase** — many Gore vents are commonly rated to roughly **-40°C**, but this is a 🔧 typical/example figure, not confirmed for the actual part chosen | 🔎 verification task, blocking part selection |
| Icing / snow burial over the vent | A snow- or ice-covered membrane can't equalize pressure or pass moisture vapor — defeats the vent's purpose and risks a sealed-box condensation problem instead | Mount the vent **facing down or in a sheltered orientation** (e.g., underside or a protected side of the enclosure) so snow doesn't accumulate directly over it; avoid a top-facing or upward orientation | 🟢 settled design pattern; exact mounting geometry = 🔎 verify at enclosure selection |
| Interior frost/condensation from low internal heat + large diurnal swings | The isolation frame's electronics draw very little heat (§1) — unlike a warmer, human-occupied cabinet, there's little internal heat to keep surfaces above the dew point through a cold night/day swing | Pair the Gore vent with **desiccant** (already settled above), **conformal coating** on exposed PCBs/connections where practical, and **smart component placement** (keep sensitive components off the coldest surfaces, away from the vent's direct airflow path) | 🔧 assumption/pattern — verify conformal-coating compatibility with selected boards before applying |

### Thermal zoning — insulated battery compartment vs. vented electronics bay (🔒 required, resolves the vent-vs-insulation tension)

**The core tension:** a Gore vent is, by design, an air-exchange/moisture-vapor path — that is
exactly what fights the LiFePO4 cold-charge-cutoff mitigation, which wants the battery **insulated
and buffered** from ambient swings (§3). Venting the whole enclosure and insulating the whole
enclosure are contradictory goals if both are applied to the same airspace.

**Resolution: split the enclosure into two internal compartments**, not one shared airspace:

| Compartment | Contents | Treatment |
|---|---|---|
| **Battery compartment** | LiFePO4 battery only | **Insulated, buffered, not vented** — rigid foam insulation liner (§3), no Gore vent in this compartment's walls, sited away from any sun-facing wall. This is where the passive-insulation + BMS-low-temp-cutoff strategy (§3) actually applies. |
| **Electronics bay** | MPPT controller, Pi, distribution block, LVD, telemetry shunt, buck converter, wiring | **Gore-vented, not insulated** — this is where the IP66 + Gore vent baseline (above) applies. This bay's contents don't have the LiFePO4 cold-charge sensitivity, so venting for pressure/moisture management doesn't conflict with a charge-safety requirement here. |

| Zoning requirement | Pattern | Status |
|---|---|---|
| Internal partition | A physical divider inside the single outer enclosure separates the two compartments — this is **not** two separate outer boxes, just two managed airspaces within one IP66 shell | 🟢 settled design intent; partition material/construction = ❓ open |
| Cross-compartment wiring | Battery-to-electronics-bay conductors (main battery leads, BMS communication/temperature-sensor leads) cross the internal partition through a **sealed grommet or small internal bulkhead-style pass-through** — same discipline as the outer-wall bulkheads in §0A, applied internally, so the vented bay's humid/cold air doesn't leak into the insulated battery compartment through a loose wire hole | 🔒 required pattern |
| Net effect | Battery stays in its insulated, unvented, buffered compartment (cold-charge mitigation intact, §3); electronics bay gets the field-proven IP66+Gore-vent moisture/pressure management without compromising the battery's thermal buffer | 🟢 settled design logic |

---

## 8. Placement — standalone vs. mast base

**This enclosure is a relocatable module, not a fixed installation** (per §0A, total field
flexibility). The recommendation below is a **default/primary placement**, not a permanent
commitment — final placement is a **soft-open** decision pending the shade study and the
field-enclosure mounting-point milestone. Because every coupling is a bulkhead connector, moving
the frame later means disconnect-relocate-reconnect, not re-wiring.

**Decision framework** (per the owner's inputs):

**(a) Solar exposure.** The mast base sits **between a willow and a birch** — both **deciduous**,
so shading is seasonal, not constant. A "looks clear" check in winter (bare canopy) can be
misleading for summer (full canopy), and vice versa — and the two seasons matter differently here:
winter is when the LiFePO4 cold-charge-cutoff issue makes every clear-sky charging hour valuable
and days are shortest, while summer is when canopy is fullest and shading risk is highest. 🔎
**Verification task: do an actual sun-path/shade study at the literal candidate panel location(s),
checked across seasons** (field observation and/or a shade-analysis tool that accounts for tree
height and sun angle by season) — do not assume the site's general "full southern sun" statement
applies unmodified at the exact mast-base spot.

**(b) Grounding integration.** Keeping the electronics enclosure **at the mast base** lets it bond
directly into the mast's single-point ground system with the shortest, simplest bonding path (§6).
Moving the electronics elsewhere to chase sun would create a **second location** needing its own
bonding conductor back to the same ground system — a second coordination point that works against
single-point-ground discipline.

**(c) Cable-run length/loss.** PV wiring (panel → controller) tolerates a longer run more
gracefully than relocating the battery/controller/Pi cluster would: PV-side current is comparatively
low, and reasonable run length is largely absorbed by correct wire gauge and the MPPT controller's
tracking. The battery/distribution/Pi cluster, by contrast, has denser interconnects (bus, fusing,
LVD, buck converter, telemetry) that are much better kept short and in one place.

### Recommendation

- **Keep the battery/controller/Pi/distribution enclosure at the mast base.** It wants shade (§7)
  and it wants the shortest bonding path (§6) — both favor staying put.
- **Decouple the panel location if (and only if) the shade study shows the mast base is
  meaningfully shaded.** Mount the 2×100W array on a small, separate, unshaded rack/post clear of
  the willow/birch canopy, and run properly fused, correctly gauged PV extension wiring back to the
  MPPT controller at the mast-base enclosure. This preserves the single-point-ground architecture
  and adds only one comparatively low-risk cable run.
- If the shade study shows the mast base area is actually clear enough, mount the panel there
  directly and skip the extra run — simplest option, prefer it if genuinely viable. **Do not assume
  this without the shade study** — two flanking deciduous trees is a real reason to check, not
  dismiss.

---

## 9. Telemetry & recovery

### What to log (locally, no cloud)

| Signal | Source | Why |
|---|---|---|
| Battery voltage | Shunt monitor or BMS report | Basic health, trend |
| Current in (charge) | MPPT controller telemetry (if the model exposes it) or shunt | Charge behavior, panel performance |
| Current out (load) | Shunt monitor | Load-bus behavior, catches unexpected draw |
| SoC | **Prefer coulomb-counting** (shunt-based) or BMS-reported SoC over voltage-only estimates — LiFePO4's voltage curve is very flat across most of its usable range, so open-circuit-voltage SoC is unreliable | 🔧 verify against the chosen BMS's actual reporting capability |
| Solar input (W) | MPPT controller, **only if the selected model exposes a data/telemetry port** — many budget MPPT units don't | 🔎 verify against controller datasheet **before** purchase — this is a controller-selection criterion |
| Enclosure/battery temperature | Dedicated temperature sensor (e.g., 1-Wire or I2C) | Correlates with LiFePO4 cold-charge-cutoff events and condensation risk |

### Access model — respecting the "no permanent automation dashboard" scope limit

First-build "monitoring" = **SSH into the Pi and read a local log**, or run a small **one-shot**
status script — **not** a persistent always-on web dashboard (that is explicitly deferred per
CLAUDE.md/scope). Pattern: a systemd-timer-driven logger polls the shunt/BMS/controller on an
interval and appends to a plain local log (flat CSV or SQLite — no database server, no cloud). A
lightweight on-demand status script (single CLI/SSH command, or a single HTTP GET if wanted later)
is acceptable; a persistent dashboard application is out of first-build scope — route to
`scope-warden` if that's later requested.

### Recover-after-power-loss behavior (first-build acceptance requirement)

| Event | Required recovery behavior | Status |
|---|---|---|
| Pi power loss/reboot | Auto-power-on when DC is (re)applied — no physical switch requiring a person present; all field-station services **enabled** (not just started) via systemd so they self-start on boot | 🔒 required, implementation lives in `pi-field-station/systemd/` |
| Hung service/OS | Documented systemd `Restart=` policy + watchdog (Pi hardware watchdog + `WatchdogSec`, if supported by the OS image) so the system self-recovers without a truck roll | 🔒 required; exact unit config = implementation task |
| LVD trip | Auto-reconnect once battery recovers above a defined recovery voltage (with hysteresis) — **no manual reset switch required in the field** | 🔒 required feature — verify against the selected LVD/battery-protect product's datasheet |
| BMS cold-charge cutoff | Auto-resumes charging once battery temperature rises back above the cutoff threshold — no manual intervention needed | 🔒 required feature — verify against BMS datasheet |
| **Net requirement** | After any combination of power loss, cold-cutoff, or LVD trip, the system returns to normal operation **unattended** once conditions allow | 🔒 matches `docs/milestones.md` acceptance criteria — exercise this explicitly in the test checklist below |

---

## 10. Expansion path — the "one-and-done" promise

Grow later **without redesigning** the architecture:

| Growth axis | How it's absorbed | Why it doesn't force a redesign |
|---|---|---|
| More battery Ah | Add a second **same-model/chemistry/BMS-type** LiFePO4 battery in parallel via the same fused bus | Star/home-run topology (§5) means "add a branch," not "rewire" — this is also why the mismatched 8Ah spare is excluded now, so a future parallel addition is never fighting a cell mismatch |
| More panel W | MPPT controller already sized with headroom (~400 W capability target, §4) above today's 200 W array | No controller swap needed for a modest future addition |
| More branch loads | Fuse block has spare fused positions; Powerpole connectors are rated well above today's actual branch currents | "Add a fused wire," not "re-terminate everything" |
| Physical growth (extra battery/panel run) | Enclosure sized with spare interior volume and spare cable-gland/knockout positions reserved (§7) | Avoids a second enclosure swap alongside a capacity upgrade |

**Owner-accepted note (🟢 settled, ties to §1/§2's Pi 5 recalculation):** the owner has explicitly
accepted that this frame may need to be **resized later for larger projects**, if a future
graduated experiment or measured real-world load genuinely outgrows the current 50 Ah / 240 Wh-
day-class design. This expansion path (first row above — add a second same-model battery in
parallel) is the accepted mechanism for that resize. It is **not** being invoked now for the Pi 5
delta (§1/§2 show the existing 50 Ah bank still clears the ≥2-day target) — it is recorded here as
the agreed *future* release valve, so a real future need doesn't require re-litigating the
architecture.

---

## 11. Bill of materials

Every line is marked **required / nice-to-have / deferred / do-not-buy-yet**. Model numbers and
prices below are **example/typical only** — none are asserted as verified for this build.

| # | Item | Function | Example spec (🔧 not verified) | Qty | Status |
|---|---|---|---|---|---|
| 1 | LiFePO4 battery, 12.8V nominal, 50 Ah, integrated BMS w/ low-temp charge cutoff | Storage | Example product class only | 1 | **Required** |
| 2 | MPPT solar charge controller, 12/24V auto-detect, 20–30 A, true LiFePO4 profile | Charging | Example product class only | 1 | **Required** |
| 3 | Solar panel, 100 W, 12V-nominal, monocrystalline | Generation | Example product class only | 2 | **Required** (owner-approved 200 W) |
| 4 | PV combiner / MC4 parallel branch connectors | Wiring | — | 1 set | **Required** |
| 5 | PV disconnect breaker (DC-rated, PV-rated) between panels and controller | Safety isolation | — | 1 | **Required** |
| 6 | Anderson Powerpole connector sets (30A-class) | Distribution standard | — | as needed | **Required** |
| 7 | Fused DC distribution bus/block (blade-fuse, multi-circuit) | Branch fusing | — | 1 | **Required** |
| 8 | Inline main fuse, battery-to-bus | Safety | Sized to controller max output + margin — 🔎 verify | 1 | **Required** |
| 9 | LVD / battery-protect module, auto-reconnect | Battery protection | — | 1 | **Required** |
| 10 | Current/voltage shunt monitor (I2C, INA226-class) | Telemetry | — | 1 | **Required** |
| 11 | Battery/ambient temperature sensor (1-Wire or I2C) | Telemetry, cold-cutoff visibility | — | 1–2 | **Required** |
| 12 | 12V→5V DC-DC buck converter — **the experiment port's regulated source** (§0A), Pi 5 is today's occupant | Power conversion | Efficient, adequate current headroom — Pi 5's official supply class (5V/5A, 27W peak) draws more current than Pi 4B's; 🔎 verify the buck converter covers Pi 5's peak, not just its ~5W average | 1 | **Required** |
| 13 | Fiber media converter (DC-powered, field-box end) | Network termination | — | 1 | **Required** (per fiber-preferred network) |
| 14 | **IP66 outdoor cabinet, internally partitioned** into an insulated battery compartment + a Gore-vented electronics bay — larger than existing small box | Housing | Sized by mockup, §7 | 1 | **Required**, size open |
| 15 | Rigid foam insulation liner (battery compartment only) | Cold-weather buffering | — | as needed | **Required** |
| 16 | **Gore protective vent** (electronics bay only), mounted facing down/sheltered | Pressure equalization + moisture-vapor management, preserves IP66 | Field-proven pattern (owner); low-temp rating (commonly ~-40°C) and specific part = 🔧 not verified for this build | 1 | **Required** |
| 16a | Desiccant packs (electronics bay) | Auxiliary moisture control | — | as needed | **Required** |
| 16b | Internal partition / sealed grommet between battery compartment and electronics bay | Thermal zoning (§7) | — | 1 partition + as-needed grommets | **Required** |
| 16c | Conformal coating (exposed PCBs/connections, electronics bay) | Interior frost/condensation mitigation | — | as needed | **Nice-to-have** — verify board compatibility before applying |
| 17 | Sealed cable glands (IP68-rated), PV/ground/telemetry penetrations | Weatherproof bulkhead entry (§0A) | — | as needed | **Required** |
| 17a | IP-rated circular bulkhead connector, PV DC-in (or gland-terminated per row 17, if directly wired) | Weatherproof PV bulkhead coupling (§0A) | Example/typical only | 1 | **Required** |
| 17b | Bulkhead-mount Anderson Powerpole panel connector + RJ45 + signal connector, load-bus DC-out (**the experiment port** — one bay of the shared Experiment Module interface, §0A, experimentation-frame §3B) | Weatherproof, swappable single-experiment interface | Example/typical only | 1 set | **Required** |
| 18 | Bonding conductor, enclosure/DC-negative → single-point site ground | Grounding | Sized/spec by electrician | 1 run | **Required** — ⚠️ spec by `grounding-safety-inspector`/electrician |
| 19 | PV-input DC surge protection device (SPD) | Surge protection | — | 1 | **Required** — ⚠️ coordinate with mast surge-protection plan |
| 20 | Panel mounting rack/tilt frame | Structure | Depends on placement decision (§8) | 1 | **Required**, siting open |
| 21 | Battery heater pad | Active cold-weather aid | — | — | **⏸ Do not buy yet** — deferred unless winter telemetry shows passive strategy is inadequate |
| 22 | Second/expansion LiFePO4 battery, additional panels | Capacity growth | — | — | **⏸ Deferred** — expansion path only, not first build |
| 23 | Cloud monitoring subscription / vendor cloud tier | Remote monitoring | — | — | **⏸ Do not buy yet** — against no-cloud-dependency discipline |
| 24 | Persistent web dashboard software/service | Monitoring UI | — | — | **⏸ Deferred** — out of first-build scope; route through `scope-warden` if wanted later |
| 25 | MPPT controller with RS485/Bluetooth telemetry output (upgrade over a bare unit) | Telemetry | — | — | **Nice-to-have** — only needed if controller-side solar-W logging is wanted; shunt-based bus monitoring is otherwise sufficient |

---

## 12. Verification tasks (collected)

| # | Task | Ties to |
|---|---|---|
| 1 | Measure real Pi 5 + sensor draw once hardware is in hand (in-line meter, not the 🔧 5 W design assumption) | §1 load table, §2 recheck |
| 2 | Measure real lighting-controller logic draw and fiber media-converter draw | §1 load table |
| 3 | Get real vendor quotes for 25Ah vs 50Ah LiFePO4 before purchase | §2 cost-delta reasoning |
| 4 | Confirm BMS low-temp charge cutoff threshold and discharge floor on datasheet | §3 |
| 5 | Verify actual panel Voc/Vmp/Isc/Imp against the real panel spec sheet | §4 |
| 6 | Verify MPPT controller's LiFePO4 profile voltages match the chosen battery | §4 |
| 7 | Verify MPPT controller supports a remote battery-temp sensor, if used | §4 |
| 8 | Wire-gauge/voltage-drop calc once physical layout and cable lengths are fixed | §5 |
| 9 | Verify LVD auto-reconnect voltage/hysteresis on datasheet | §5, §9 |
| 10 | Grounding/bonding point, conductor sizing, SPD selection | §6 — ⚠️ `grounding-safety-inspector`/electrician |
| 11 | Enclosure dry-fit mockup with real/example-dimensioned parts before purchase | §7 |
| 12 | **Sun-path/shade study at the literal candidate panel location(s), across seasons** | §8 — blocks final panel siting |
| 13 | Confirm whether selected MPPT controller exposes solar-W telemetry before purchase | §4, §9 |
| 14 | Confirm systemd watchdog support on the chosen Pi OS image | §9 |
| 15 | Select/verify bulkhead connector hardware (PV-in, experiment-port DC-out, sensor glands) against actual current/voltage and IP-rating needs before purchase | §0A |
| 16 | Confirm experiment-port bulkhead connector current rating matches the load-bus branch fuse once both are selected | §0A, §5 |
| 17 | **Verify the selected Gore vent's actual low-temperature rating and confirm the vendor's cabinet+vent assembly holds true IP66 with the vent installed** | §7, blocking part selection |
| 18 | Confirm vent mounting orientation prevents snow/ice accumulation once the physical enclosure/mounting geometry is set | §7 |
| 19 | Verify conformal coating (if used) is compatible with the selected boards/connectors | §7 |

---

## 13. Field-box test checklist (power node)

- [ ] 🔎 Battery charges from panels under real sun; controller shows/logs expected charge current
- [ ] 🔎 Load bus (Pi + sensors + lighting logic + fiber converter) draws within expected range of
      the §1 budget once measured
- [ ] 🔒 LVD trips at its configured low-voltage threshold and does **not** require a manual reset
      to recover
- [ ] 🔒 BMS refuses to charge below its low-temperature cutoff (bench-test with a temp reference,
      not by waiting for real winter, if practical) and resumes automatically once warm
- [ ] 🔒 Single-point grounding continuity verified — no second ground path (⚠️
      `grounding-safety-inspector` sign-off)
- [ ] Enclosure vent/desiccant inspected; no condensation evidence after a full weather cycle
- [ ] 🔎 **Winter vent inspection:** after a snow/ice event, confirm the Gore vent is not buried or
      iced over and is still functioning (mounting orientation validated, §7)
- [ ] 🔒 **Thermal zoning check:** confirm the battery compartment stays measurably warmer/more
      buffered than the vented electronics bay during a cold-weather log period, and that no
      humid/cold air is leaking across the internal partition at the wiring pass-through (§7)
- [ ] 🔒 **Full power-cycle test:** disconnect battery + panels, reconnect, confirm the Pi boots,
      all field-station systemd services come up automatically, and telemetry logging resumes
      **without any manual step**
- [ ] 🔒 **Simulated LVD-trip recovery test:** artificially drop bus voltage below LVD threshold,
      confirm auto-reconnect and clean Pi reboot once voltage recovers
- [ ] Telemetry log (voltage, current in/out, SoC, temperature) reviewed for a full day/night cycle
      and matches expected pattern
- [ ] 🔒 **Bulkhead integrity check:** every conductor crossing the enclosure wall (PV-in,
      experiment-port DC-out, sensor/telemetry lines) passes through a rated bulkhead
      connector/gland — no ad-hoc pass-throughs found on inspection (§0A)
- [ ] 🔎 **Experiment-port swap test:** disconnect the experiment-port bulkhead connector and
      reconnect (simulating a future graduated-experiment swap); confirm no internal enclosure
      wiring is disturbed and the load bus re-energizes cleanly

---

## 14. Design-load estimate — scope-warden condition closure

This document's §1 load table is the **as-required design-load estimate** for the isolation
frame's current payload, closing scope-warden condition 1 in
`docs/scope-ruling-dc-power-node.md` §4 ("document the design load explicitly ... so the 200W
array / 2-day battery sizing is traceable to a real load estimate"). See §1 for the itemized
load table and §2 for how it drives battery sizing. Actual figures remain 🔧 assumptions pending
the measurement tasks in §12 — this closes the *documentation* condition, not the *measurement*
verification tasks.

---

## Related

- `pi-field-station/README.md` — overall edge-services scope, design standard, and two-frame
  architecture overview.
- `pi-field-station/experimentation-frame/README.md` — the companion AC-powered, multi-experiment,
  **not field-validated** lab-bench frame. Experiments graduate from there into this isolation
  frame via the experiment port (§0A) before being considered field-certified.
- `lighting-controller/README.md` — lighting-controller logic (control draw budgeted here; fixture
  load sized separately).
- `docs/safety-grounding-bonding.md` — single-point-ground / bonded-entry discipline this node must
  bond into.
- `docs/safety-power-frames-bonding.md` — `grounding-safety-inspector`'s bonding/AC-safety/surge
  requirements specific to the two-frame outdoor power architecture; source of truth for
  grounding/bonding/AC-safety content (this document is source of truth for power/load
  engineering).
- `docs/scope-ruling-dc-power-node.md` — scope-warden's ratification of this node, including the
  design-load-documentation condition closed in §14 above.
- Sub-agents: `field-station-engineer` (this document's owner), `grounding-safety-inspector`
  (§6 grounding/surge items, and AC-safety items for the companion experimentation frame),
  `scope-warden` (BirdNET duty-cycling boundary, no-dashboard, no-expansion-beyond-validation
  limits, two-frame scope boundary).
