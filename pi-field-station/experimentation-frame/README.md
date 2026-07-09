---
classification:
  visibility: public-safe
  geospatial_sensitivity: none
  contains_real_coordinates: false
  contains_real_parcel_geometry: false
  contains_identifiable_imagery: false
  safe_for_public_repo: true
---

# Experimentation Frame — AC-Powered Multi-Experiment Lab Bench

> **This is a lab bench, not a field-validated deployment.** The experimentation frame is a
> discrete, weathertight, AC-powered enclosure with **no power-budget limits**, built around a
> **bounded baseline of 3–4 concurrent experiment bays** — one power-intensive Jetson-class bay
> plus two to three lower-power Raspberry Pi 5 bays — 24/7, plus room for IP cameras, weather
> instruments, and other experimental loads, **deliberately exposed to full Wisconsin weather** so
> hardware and software get real thermal/weather stress before anything is trusted. Nothing here
> is certified for field deployment until it passes the **graduation gate** into the isolation
> frame (`pi-field-station/power/README.md`) and is proven under real solar/battery/weather
> constraints. Geometry/siting statements are generalized — no coordinates, parcel geometry, or
> address content.

Legend: 🟢 settled · 🔧 assumption (typical/example value — verify) · 🔎 field-verify (measurement/
test task) · ❓ open question · 🔒 safety requirement · ⚠️ pro-review (electrician /
`grounding-safety-inspector`) · ⏸ deferred / do-not-buy-yet

---

## 0. What this frame is, and is not

| This frame IS | This frame is NOT |
|---|---|
| An AC-powered lab bench for **developing and stress-testing** edge-service experiments under real outdoor conditions | A field-validated, certified, or production deployment |
| A place to run **3–4 concurrent** experiments at once, in defined bays (one Jetson-class power-intensive bay + 2–3 Pi 5 lower-power bays, §0B), plus camera/sensor trials | A replacement for the isolation frame's single-experiment solar/battery certification, or an unbounded/open-ended compute farm |
| Explicitly **exposed to full Wisconsin weather** — that exposure is the point: it reveals real degradation before certification | Insulated, shaded, or thermally babied the way the isolation frame is (isolation-frame §7) |
| Grid-AC dependent by design (test/dev bench) | A statement that the *overall project architecture* depends on grid power — per CLAUDE.md, grid power is for testing/fallback only; this frame is the explicit, bounded exception where that's acceptable because it is a bench, not the production path |
| A discrete, weathertight, relocatable module (§0A governing law, shared with the isolation frame) | A shared chassis with the isolation frame — the two are always physically separate enclosures |

**Graduation gate (🟢 settled, owner decision):** an experiment matured here ports into the
isolation frame as a **single 12V load** through that frame's defined experiment port, and is
only then considered on the path to field-certified. See `pi-field-station/power/README.md` §0A
and "Two-frame architecture."

**Jetson-class scope guardrail (🔒 settled boundary):** Jetson-class compute (NVIDIA Jetson —
e.g., Orin Nano ~7–15 W up to AGX Orin ~15–60 W+; **all wattages 🔧 typical/verify, per-module,
not measured for this build**) is authorized **strictly for this experimentation frame**. It is
**not** designed into the isolation frame and must not be assumed compatible with it. Only a
**drastically power-managed, individually certified, single-experiment variant** of a
Jetson-class workload could ever be considered for a future isolation-frame graduation — that is
a **deferred, unlikely, future question**, not something designed in now. Do not size the
isolation frame's battery/array/distribution around any Jetson-class assumption.

**Scope discipline note:** hosting IP cameras and weather instruments **here** is an authorized
lab-bench exception to CLAUDE.md's deferred-backlog items ("no camera sprawl," "no weather-station
expansion") — it is experimentation, not a production commitment. If any experiment here trends
toward becoming a **permanent** camera network, weather-station service, or automation dashboard,
that promotion is a **separate scope decision** routed through `scope-warden` before it is allowed
to graduate — maturing in this frame does not itself authorize permanent deployment of a
deferred-backlog service.

---

## 0A. Governing design law (shared with the isolation frame)

Same law as `pi-field-station/power/README.md` §0A, restated for this frame:

1. **Discrete, self-contained, weathertight enclosure** — its own sealed cabinet, not a shelf or
   open rack, and not shared with the isolation frame.
2. **Every power and sensor coupling passes through a weathertight bulkhead** — AC in, any DC out
   to bench experiments, and all sensor/signal/telemetry/camera lines. No ad-hoc pass-throughs.
3. **Total field flexibility** — this cabinet is a relocatable module, not a fixed installation
   (§8 placement below gives a default/primary recommendation, not a permanent commitment).

| Coupling | Direction | Example bulkhead hardware (🔧 typical/example — verify before purchase) |
|---|---|---|
| AC in | Enclosure wall in | Weatherproof, IP-rated AC inlet connector (e.g., locking twist-lock outdoor inlet) feeding an interior GFCI-protected distribution — **exact hardware and protection scheme is an electrician/`grounding-safety-inspector` decision, not decided here (§2)** | ⚠️ pro-review |
| DC out, 12–19V Jetson-class bus (§2A) | Enclosure wall out (or internal bay, if the DC supply lives inside the cabinet — see §2A) | Bulkhead-mount Anderson Powerpole panel connector(s), matching the isolation frame's connector standard for consistency; higher-current Jetson branches may need a larger Powerpole/connector class than the isolation frame uses — 🔎 verify against actual selected supply current | 🔧 example only |
| DC out, other bench experiments (Pi-class) | Enclosure wall out | Bulkhead-mount Anderson Powerpole panel connector | 🔧 example only |
| Sensor / signal / telemetry / camera lines | Enclosure wall, either direction | Sealed IP68-rated cable gland per cable, or a multi-pin IP-rated circular connector for grouped signal lines | 🔧 example only |
| Data/network uplink to shack | Enclosure wall | Fiber-preferred per CLAUDE.md network discipline (see §5) — bulkhead fiber pass-through / field-terminated connector | 🔧 example only, verify against chosen media converter |
| Thermal-management penetration (if the chosen approach in §1 requires one — e.g., a heat-exchanger core or cold-plate radiator through the wall) | Enclosure wall | Purpose-built, gasketed, weathertight thermal-hardware mounting — **this is itself a bulkhead-class penetration and must meet the same weathertight standard**, not a generic vent cut | 🔒 required if a wall-penetrating thermal solution is chosen (§1) |

Unlike the isolation frame, this cabinet does **not** have a single "experiment port" — by design
it hosts **multiple concurrent** experiment branches, each individually fused/breakered and
bulkhead-coupled (§3).

---

## 0B. Concurrency & load profile (bounded baseline — owner decision, replaces "unbounded multiple")

This section bounds what was previously an open-ended "multiple experiments" statement into a
concrete sizing basis for §1 (thermal), §2/§2A/§2B (AC + DC-rail budget), and §3 (physical bays).

| Bay type | Count | Example hardware | Typical draw per bay (🔧 assumption — verify) |
|---|---|---|---|
| **Power-intensive bay** | **1** | Jetson-class module + peripherals (carrier board, storage, camera/sensor inputs) | **up to ~60 W**, 🔧 typical/vendor-published ceiling for an AGX-Orin-class module + peripherals, not measured for this build |
| **Lower-power bay** | **2–3** | Raspberry Pi 5 + sensors/accessories | **~10–15 W each**, 🔧 typical/vendor-published, not measured for this build |

**Aggregate worst-case design load (all bays active simultaneously):**

| Component | Figure (🔧 assumption) |
|---|---|
| Intensive bay | ~60 W |
| Lower-power bays (upper end: 3 × 15 W) | ~45 W |
| Compute subtotal | ~105 W |
| Overhead/headroom (🔧 ~20%: network switch, fiber media converter, AC-DC conversion losses, thermal-system fan/pump power) | ~21 W |
| **Aggregate worst-case design load** | **≈ 130 W** |

**How this number is used:** it is the **design/sizing input** handed to §1 (thermal-management
approach selection), §2 (AC circuit-sizing input for the electrician), §2A (Jetson DC-rail supply
sizing), and §2B (Pi-class DC-rail supply sizing) — **not** a hard power ceiling. This frame's
governing philosophy (§2) remains "not power-budget-limited the way the isolation frame is"; this
number instead replaces the previously vague "several times a single module's figure" language
with a concrete, bounded, verify-before-build target. 🔎 **Verification task: re-run this table
with real per-bay measurements once hardware is in hand, before finalizing the AC circuit,
DC-rail supplies, or thermal-management BOM.**

---

## 1. Thermal — the dominant design constraint (flag prominently)

**High-wattage compute inside a sealed, weathertight enclosure through a full Wisconsin summer is
the real design problem this frame has to solve — more so than power distribution.** The
weathertight-bulkhead law (§0A) means the easy answer — "cut some vents" — is not available
without deliberately trading away IP rating. This section exists to make that trade-off explicit
and force it to be a **documented decision**, not a default.

### Why Jetson-class compute changes the thermal picture

- The **bounded load profile is now defined in §0B**: 1 power-intensive Jetson-class bay (up to
  ~60 W) + 2–3 lower-power Pi 5 bays (~10–15 W each) + overhead, aggregating to a **≈130 W
  worst-case design load (🔧 assumption)**. Everything below uses that figure, replacing the
  earlier open-ended "several times a module's figure" language.
- Pi-class (Pi 5) bays run a real but comparatively modest ~10–15 W each — meaningfully more than
  a Pi 4B, but still an order of magnitude below the intensive bay. Thermal load from the Pi-class
  bays alone would likely still be manageable with ordinary vented/desiccant enclosure practice,
  specifically the **IP66 cabinet + Gore protective vent** pattern the owner has field-proven (see
  `pi-field-station/power/README.md` §7) — but see the next point: the *intensive* bay dominates
  the total, so the Pi-class bays' modest load doesn't change the overall thermal-approach
  decision on its own.
- **A Gore vent solves pressure/moisture, not Jetson-class heat rejection.** Important
  distinction: the Gore vent pattern that is likely the *whole* thermal answer for the low-power
  isolation frame is **only a pressure-equalization/moisture-vapor-management device** here — it
  passes essentially no meaningful heat flow. It does **not** substitute for one of the
  heat-rejection approaches below when Jetson-class compute is present.
- **The intensive bay dominates the aggregate.** At up to ~60 W, the single Jetson-class bay is
  roughly half (or more) of the entire ≈130 W aggregate design load by itself (§0B) — the
  heat-rejection approach below must be sized to the **aggregate**, not just the intensive bay in
  isolation, but the intensive bay is the reason a Gore-vent-only approach is inadequate.
- 🔎 **Verification task (blocking):** before finalizing cabinet size or a thermal-management
  approach, confirm the §0B aggregate (**≈130 W worst-case, all bays active**) against real
  per-bay measurements once hardware is in hand, and check that total against a conservative local
  summer ambient design temperature. **Do not assume a generic ambient figure — field-verify or
  use a locally appropriate design-temperature reference**, and do not finalize the enclosure/
  thermal BOM before this calculation exists.

### Thermal-management options (a decision to make, not a fixed spec)

| Approach | How it works | IP-rating impact | Complexity / field-repair burden | Added power draw | Maintenance |
|---|---|---|---|---|---|
| **(a) Sealed air-to-air heat exchanger** | Two independent air loops (interior/exterior) exchange heat across a finned core without mixing air — enclosure stays fully sealed | **Preserves full weathertight rating** — no direct air exchange with outside; **can be paired with a Gore vent for pressure/moisture equalization on the otherwise-sealed shell** — the two solve different problems (heat vs. pressure) and are not redundant | Moderate — one more powered component (its own fan(s)) to size, mount, and eventually service | Its own fan power draw, on top of the compute load it's rejecting | Exterior fins/core need periodic cleaning; fans are a wear item |
| **(b) Filtered/louvered forced ventilation with weather protection** | Rain-hooded, filtered/screened intake and exhaust draw outside air directly through the cabinet | **Reduces effective IP rating** — outside air (and some moisture/dust, filtered but not eliminated) now enters the enclosure; this is a real trade against the weathertight-bulkhead law and should be treated as a documented exception, not the default | Lower parts complexity than (a), but adds a maintenance burden (filter changes) and a condensation-control tension with the vented/desiccant practice already in use | Fan power draw, generally less than a full heat-exchanger unit | Filter replacement/cleaning on a defined interval; higher inspection frequency justified |
| **(c) Cold-plate / thermal-management loop** | A cold plate bonded to the Jetson module's heatsink carries heat via heat pipe or liquid loop to an external finned radiator that penetrates the wall through a dedicated, gasketed thermal bulkhead (§0A) | Enclosure interior stays sealed; the wall penetration itself must meet bulkhead weathertight standard | **Highest complexity and field-repair burden** — more parts, a fluid loop (if liquid) is a new failure mode, harder to diagnose/repair by a small field team | Loop pump (if liquid) or none (if pure heat-pipe/passive) | Loop integrity checks; more specialized than (a) or (b) |

**None of these three is selected here.** 🔒 **This is a required design decision, sized against
the §0B aggregate worst-case load (≈130 W), made after the load-vs-ambient calculation above, and
validated with a physical mockup before the cabinet BOM is finalized.** The choice directly drives
cabinet size, mounting layout (§3), and the BOM (§9). Per §0B point 3, the selected
thermal-management hardware is physically carried by the **power-intensive bay** (§3).

**Default framing, not a decision:** option (a) best preserves the weathertight law the rest of
this architecture depends on and is the natural first thing to evaluate; options (b) and (c) are
legitimate alternatives if (a) proves undersized or overly complex for the actual measured load —
this is a decision to work through with real numbers, not a foregone conclusion.

**Valid pairing, not a substitute:** if option (a) or (c) is selected (enclosure stays sealed), a
**Gore protective vent can and should still be added** for pressure equalization and moisture-vapor
management on the sealed shell — mirroring the isolation frame's field-proven baseline (§0, and
`pi-field-station/power/README.md` §7) — as long as its low-temperature rating and mounting
orientation are verified the same way (🔎 same verification pattern as the isolation frame; treat
as a separate task here, not assumed carried over). **A Gore vent is never, by itself, a
substitute for options (a)/(b)/(c) when Jetson-class heat load is present.**

---

## 2. AC power — safety items deferred to `grounding-safety-inspector`

**This document does not decide AC safety.** It states what must be specified and by whom. Do
not treat any AC wiring detail below as settled until the referenced pro-review items are closed.

| Item | Why it matters | Owner |
|---|---|---|
| GFCI/GFI protection on the outdoor AC circuit | Required for outdoor/wet-location AC per standard code practice | ⚠️ `grounding-safety-inspector` / licensed electrician |
| Service disconnect (local means of disconnect at or near the enclosure) | Lets someone de-energize the cabinet without going back to the panel | ⚠️ electrician |
| Circuit sizing, breaker rating, conductor gauge for the feed to this enclosure | Must match actual load (now including Jetson-class + thermal-management draw, §1) and code requirements — **not estimated here** | ⚠️ electrician |
| Enclosure/AC-equipment bonding into the site's single-point grounding system | Must **not** create a second/isolated ground — same single-point-ground discipline as the mast and the isolation frame (`docs/safety-grounding-bonding.md`) | ⚠️ `grounding-safety-inspector` |
| Weatherproof/wet-location rating of all AC-side components (inlet, receptacles, breakers) | Outdoor exposure requires wet-location-listed hardware, not indoor-rated parts | ⚠️ electrician |
| Surge protection on the AC feed | Coordinate with the mast's overall surge-protection plan | ⚠️ `grounding-safety-inspector` |

Once those are specified, this document records the **resulting distribution pattern** (not the
safety decisions themselves):

| Item | Pattern | Status |
|---|---|---|
| Distribution topology inside the cabinet | Star/home-run from a fused or breakered AC distribution block — each experiment branch individually protected, mirroring the isolation frame's DC star topology for consistency | 🟢 settled *pattern*; actual breaker/fuse sizing = ⚠️ electrician |
| Number of experiment branches (first build) | **3–4 bays** (1 power-intensive + 2–3 lower-power), per the bounded profile in §0B — replaces the earlier open "sized for multiple" language | 🟢 settled count; exact physical layout = ❓ open |
| Load capacity | Explicitly **not power-budget-limited** the way the isolation frame is (owner decision) — bounded only by the AC circuit's actual rated capacity, which is an electrician-specified number. **The §0B aggregate worst-case design load (≈130 W, 🔧 assumption) is the sizing input handed to the electrician** — do not size the circuit for Pi-class loads alone and add Jetson-class hardware later without re-verifying | 🔒 do not exceed the electrician-specified circuit rating; 🔎 re-verify against §0B once real hardware is measured |

### 2A. Regulated DC rail for Jetson-class loads (the power-intensive bay)

Jetson-class carrier boards commonly accept DC input in roughly the **12–19V** range (🔧 typical/
verify against the specific module and carrier board selected — this varies by product). Rather
than powering the Jetson-class experiment from its own wall-wart-style AC adapter, provide a
regulated DC feed to the power-intensive bay (§0B, §3):

| Item | Pattern | Status |
|---|---|---|
| DC bus voltage | Regulated 12–19V DC (exact voltage set by the Jetson-class hardware actually selected) | 🔧 assumption — verify against chosen module/carrier board before specifying the supply |
| Source | One AC-DC power supply unit inside the cabinet, sized to the **intensive bay's ~60 W (§0B) + margin** | 🔧 sizing basis is §0B's per-bay figure — not invented here, confirm against real hardware |
| Distribution | Single fused branch feeding the power-intensive bay (§3) — same star/home-run discipline as §2's AC distribution and the isolation frame's DC bus (§5 of `pi-field-station/power/README.md`) | 🟢 settled pattern |
| Coupling | Bulkhead-mount Powerpole (or a higher-current-rated equivalent if branch current exceeds standard Powerpole class — 🔎 verify) per §0A | 🔧 example only |
| Relationship to the isolation frame's DC bus | **Not the same bus, not battery-backed, no autonomy claim.** This is a grid-AC-derived DC rail for bench convenience — it carries none of the isolation frame's solar/battery/LVD/telemetry apparatus | 🔒 do not conflate the two — keep them architecturally and physically distinct |

### 2B. Regulated DC rail for Pi-class loads (the 2–3 lower-power bays)

Raspberry Pi 5 boards use a **5V** supply (commonly USB-C PD-class input, up to ~27 W per board
per vendor spec — 🔧 typical, verify). Rather than a separate wall-wart per bay, provide a shared
regulated 5V feed sized to the lower-power bays defined in §0B:

| Item | Pattern | Status |
|---|---|---|
| DC bus voltage | Regulated 5V DC (matches Pi 5's USB-C PD input) | 🔧 assumption — verify against actual Pi 5 power-input spec/revision used |
| Source | One AC-DC 5V supply (or a powered multi-port USB-C hub fed from the cabinet's internal AC) sized to **2–3 bays × ~10–15 W each (§0B) + margin** | 🔧 sizing basis is §0B's per-bay figures — not invented here, confirm against real hardware and actual bay count (2 vs. 3) |
| Distribution | One fused/protected branch per lower-power bay — same star/home-run discipline as §2A | 🟢 settled pattern |
| Coupling | Bulkhead-mount Powerpole-to-USB-C adapter, or a panel-mount USB-C bulkhead connector, per bay (§0A) | 🔧 example only |
| Relationship to the isolation frame's single Pi 5 | **Architecturally distinct.** The isolation frame's one Pi 5 runs off its own battery-backed 12V→5V buck converter (`pi-field-station/power/README.md` §5); this 5V rail is grid-AC-derived, multi-bay, and not battery-backed | 🔒 do not conflate the two |

---

## 3. Cabinet — weatherproof, standardized swappable experiment bays

### 3–4 standardized experiment bays (🟢 settled physical architecture, per §0B)

This is the physical implementation of §0B's bounded concurrency profile — **not** an open rack,
but **3–4 discrete, standardized bays**, each independently swappable:

| Bay | Count | Power feed | Physical role |
|---|---|---|---|
| **Power-intensive bay** | 1 | §2A's 12–19V Jetson-class DC rail | **Carries the selected thermal-management hardware (§1)** — the heat-rejection solution is physically mounted at/with this bay, since it dominates the aggregate heat load |
| **Lower-power bay** | 2–3 | §2B's 5V Pi-class DC rail | Standard Pi 5 + sensor/accessory mounting; benefits from the intensive bay's thermal solution only incidentally (shared cabinet airspace), not a dedicated requirement |

| Requirement | Pattern | Status |
|---|---|---|
| Enclosure class | Outdoor-rated (IP/NEMA class appropriate for exposed installation), sized to fit 3–4 bays **and** whatever thermal-management hardware §1 selects for the intensive bay | 🔎 select by mockup once bay dimensions and thermal approach are known; exact dimensions = ❓ open |
| Bay standardization | Each of the 3–4 bays is a **defined mounting footprint with its own backplane connector set** (§3A — internal to the cabinet, distinct from the enclosure's external bulkhead penetrations in §0A, which remain the AC inlet plus any sensor/camera leads that actually exit the cabinet) — a bay's payload can be swapped without touching another bay's wiring, reinforcing total-field-flexibility | 🟢 settled pattern |
| Interior mounting | Modular mounting (e.g., DIN rail and/or a perforated equipment panel) within each bay so individual experiment payloads can be added/removed without disturbing others | 🟢 settled pattern; hardware = 🔧 example only |
| **Power-intensive bay mounting/airflow** | Mounting slot/bracket sized for Jetson dev-kit/carrier-board form factor (not Pi-sized), with clearance for **active heatsinks/fans** on the module itself, and positioned so the chosen thermal-management approach (§1) can actually reach it — e.g., within the sealed-loop's internal air path (option a), in the forced-ventilation airflow path (option b), or within cold-plate mounting reach (option c) | ❓ open — depends on §1's thermal decision; exact form-factor dimensions not invented here, verify against the specific Jetson module/carrier selected |
| **Lower-power bay mounting/airflow** | Mounting slot sized for Pi 5 + case; Pi 5's official-class active cooler (heatsink+fan) may be needed for sustained load per bay — verify against actual duty cycle | 🔧 assumption — verify once actual Pi 5 workload/duty cycle for each bay is known |
| Experiment isolation | Each bay gets its **own** fused/breakered branch (§2A/§2B) and its **own** bulkhead penetration(s) — one bay's fault or removal should not disturb another's wiring | 🟢 settled pattern |
| Weatherproofing | **IP66 + Gore protective vent**, same field-proven pattern as the isolation frame, per §0/§1 — used for pressure/moisture management across the shared cabinet airspace **and**, if a sealed thermal-management option (a/c) is chosen, on the whole sealed shell. The Jetson-class *heat* path is handled separately per §1 — a Gore vent alone is not adequate for that load | 🟢 settled pattern for pressure/moisture; Jetson heat-rejection approach is a separate, larger decision (§1) |
| Thermal strategy (overall) | **Deliberately less insulated/babied than the isolation frame** — the point of this frame is to expose hardware to real seasonal thermal swing before it's trusted; active climate control for *ambient* cabinet temperature is not added in the first build, but **active heat rejection for the power-intensive bay (§1) is a separate and necessary decision**, not the same thing as "climate control" | 🟢 settled pattern (ambient) / 🔒 required decision (intensive-bay heat rejection, §1) |
| Spare capacity | If a 4th bay slot is not populated at first build, reserve its mounting footprint and bulkhead knockouts rather than leaving zero headroom | 🟢 settled pattern |

---

## 3A. Backplane & bay interface (reusable pluggable-bay design)

**Owner decisions governing this section:** **no live hot-swap** required (insert, connect, then
switch on is fine — no pre-charge/staggered-pin complexity needed); **no existing rack/DIN
inventory to match** (clean slate, pick the best field-replicable standard, not a bespoke design).
This is a **parallel-track lab-bench design** — it does not gate or delay the mast build — and is
deliberately kept simple rather than maximally elegant, per the charter's field-replicability
standard.

### Standard evaluation (pick one, don't invent bespoke)

| Standard | SBC payload fit | Insert-then-switch fit | Field-replicability/rebuildability | Enclosure footprint/complexity | Verdict |
|---|---|---|---|---|---|
| **DIN-rail modular carriers** | Good — many COTS DIN-rail Pi/industrial-SBC carriers exist | Fine — carrier clips on/off, wiring is flying-leads/terminal-block, no true "bay connector" concept | Very high — DIN rail is ubiquitous, hand-tool serviceable, no custom fabrication | Low | Strong *mounting* mechanism, but doesn't by itself define a single per-bay connector/keying scheme — see recommendation below |
| **Eurocard / DIN 41612 subrack** | **Poor without custom work** — Pi 5/Jetson boards are not native Eurocard form factor; needs **bespoke SBC carrier adapter PCBs** per board type | Good — true blind-mate card-edge connectors | Low for a small field team — subrack + custom carrier cards need PCB design/fab, a real barrier to "rebuildable by a small field team" | High — 3U/6U subrack depth/weight is oversized for 3–4 bays | **Rejected** — custom carrier-card fabrication burden contradicts field-replicability and the "keep it simple, don't delay the mast" constraint |
| **19″ subrack + sleds** | Good — sleds are simple fabricated trays, no custom PCB needed | Workable, but true blind-mate rear connectors need precision rail alignment; a flying pigtail avoids that but gives up some of the "slide-in" elegance | High — 19″ rack hardware and connectors are widely available and well understood | Moderate-high — full 19″ width is likely oversized for a compact field cabinet; a shortened/partial rack is possible but is itself a deviation from the "known standard" | Reasonable second choice, but adds rack-rail mechanical overhead not clearly justified for 3–4 bays in a modest enclosure |
| **Passive keyed-connector backplane** (a wiring harness/distribution panel with one defined connector set per bay position; SBC physically held by a simple standoff/DIN-rail tray, independent of the electrical interface) | **Best fit** — decouples "how the board is mounted" (simple tray/standoff/DIN, per §3) from "how it's powered/networked" (defined connector set below) — no custom carrier card needed for either Pi 5 or Jetson-class boards | **Best fit for insert-then-switch** — no blind-mate precision required; connect a short keyed pigtail, then flip the bay switch | **Best fit** — built from COTS panel-mount connectors and hand-wireable harness, fully documentable with a plain pinout table (matches this project's "plain, inspectable config" ethos), no PCB fabrication required | Low — fits inside a modest cabinet, no rack rails needed | **Recommended** |

**Recommendation: passive keyed-connector backplane**, using simple standoff/DIN-rail trays (per
§3's existing mounting pattern) to physically hold each bay's SBC carrier, decoupled from a
**separate, defined per-bay connector set** (below) that carries power, data, and signal. This
combines the mounting simplicity of DIN-rail/standoff practice with a genuinely defined,
documented, keyed interface — without Eurocard's custom-carrier-card burden or a full 19″ rack's
footprint. **The backplane itself is passive** (power/data distribution only, no active
electronics on it) — see DC-DC conversion placement below.

### Per-bay interface (insert-then-switch, no live hot-swap)

Each bay gets a **defined connector set**, not one exotic combo connector — this keeps every
individual connector a standard, field-replaceable, sourceable part:

| Line | Connector | Notes |
|---|---|---|
| DC power | **Anderson Powerpole (PP-series, standard shell family)** for the 5V Pi-class rail (§2B) bays; a **physically different, non-mating connector family** for the 12–19V Jetson-class rail (§2A) bay — e.g., Anderson **SB-series** (a distinctly larger, incompatible shell from PP-series, common in the solar/EV DIY space) | 🔒 **This is the mechanical keying mechanism.** PP15/PP30/PP45 shells are *intentionally interchangeable with each other* by design (that's the whole point of the Powerpole standard) — so varying current rating **within** the PP family does **not** reliably prevent mis-mating. Keying instead comes from using a **genuinely different, non-mating connector family** for the higher-voltage rail. 🔧 exact connector families/models are examples — verify true physical non-interchangeability before purchase, this is a safety-relevant selection |
| Data | Standard **RJ45**, one straight-through Cat5e/6 patch cable per bay to the interior Ethernet switch (§5, §9 BOM item 13) | 🟢 fully standard, trivially field-replaceable with an off-the-shelf cable |
| Signal / status / telemetry | A small keyed multi-pin connector (🔧 example: JST-VH-class or similar small locking connector), carrying: thermal-system fault/status line (intensive bay, §1/§6), a spare telemetry pair, and a spare GPIO pair reserved for future sensor use | 🔧 example only — exact pin allocation is ❓ open, finalize once sensor/telemetry needs for each bay class are set |

**Fusing and switching (🔒 required, implements "insert-then-switch, no live hot-swap"):**

| Item | Pattern | Status |
|---|---|---|
| Per-bay fuse | Inline fuse on each bay's power branch, sized to that bay's rail class and max current (§2A for the intensive bay, §2B for each lower-power bay) | 🔒 required, same star/home-run individually-fused-branch discipline as §2/§2A/§2B |
| Per-bay switch | A physical on/off switch or breaker per bay, mounted on the bay's own faceplate (not buried inside the harness) so a technician can de-energize **that one bay** without touching the others | 🔒 required |
| Swap procedure | (1) flip the bay's switch OFF, (2) disconnect the bay's power/data/signal connectors, (3) remove the module (tray/standoff-mounted, §3), (4) install the replacement module, (5) reconnect connectors, (6) flip the switch back ON | 🔒 required procedure — **no live hot-swap**, no pre-charge/staggered-pin/blind-mate complexity needed anywhere in this design |
| Mechanical keying against mis-seating | Connector-family keying (above) prevents feeding the 12–19V Jetson rail into a Pi-class bay or vice versa; bay faceplates are labeled with rail class + bay number | 🔒 required pattern; 🔎 verify actual connector shells are non-interchangeable before purchase |

### Where DC-DC conversion lives (backplane stays passive)

**DC-DC conversion happens centrally, at the rail source — not on the backplane, and not
per-bay.** The backplane/harness distributes **already-regulated** voltage:

- The 12–19V Jetson-class rail is generated by the single AC-DC supply defined in §2A and
  distributed, already regulated, to the intensive bay's connector.
- The 5V Pi-class rail is generated by the AC-DC supply (or powered hub) defined in §2B and
  distributed, already regulated, to each lower-power bay's connector.
- If an individual module needs further on-board regulation (e.g., a carrier board's own internal
  regulator), that is the **module's own concern**, not the backplane's — keeping the backplane a
  **passive power/data distribution harness only**, per the design law in §0A.

This also keeps protection (fuse + switch) on the **infrastructure side** (bay/backplane), not on
the swappable module itself — modules stay simple, cheap, and interchangeable; safety devices stay
in one maintained location per bay.

---

## 3B. Common cross-frame module interface (the graduation gate, made physical)

This defines **one standardized "Experiment Module" interface**, used identically by **both**
frames — this is what makes the graduation gate (§0) a physical reality, not just a policy
statement: a certified module can be physically unplugged from an experimentation-frame bay and
plugged into the isolation frame's experiment port (`pi-field-station/power/README.md` §0A),
because both are the same interface.

### Module definition

An **Experiment Module** = {compute board (Pi 5 or Jetson-class) + a simple carrier tray/standoff
mount + the §3A connector set (power + RJ45 + signal)}. The **mechanical tray/mounting envelope is
common across module classes** — one physical tray standard, sized by mockup once real hardware is
chosen (❓ open) — so a bay's *slot* doesn't need a different shape per class. What differs between
classes is strictly the **electrical rail** the module is wired for, enforced by the §3A
connector-family keying, not by tray geometry.

### Module classes and where each fits

| Module class | Rail | Typical power/thermal envelope (🔧 assumption) | Fits an experimentation-frame bay? | Fits the isolation-frame experiment port? |
|---|---|---|---|---|
| **QRP-solar-class** (Pi 5-class) | Regulated **5V** — experimentation frame's §2B rail, or the isolation frame's 12V→5V buck-converter output (`pi-field-station/power/README.md` §0A/§5/§11 BOM item 12) | ~10–15 W (🔧), passive/heatsink-only cooling assumed adequate | **Yes** — any of the 2–3 lower-power bays | **Yes — this is the only class the isolation frame's experiment port supports** |
| **Intensive-class** (Jetson-class) | Regulated **12–19V** — experimentation frame's §2A rail only | up to ~60 W (🔧), **requires active heat rejection** (§1) | **Yes** — the single power-intensive bay only | **No.** The isolation frame has no 12–19V rail and no active heat-rejection hardware — an intensive-class module is **not** compatible with the isolation frame's experiment port, consistent with the existing graduation-gate rule (`pi-field-station/power/README.md` "Jetson-class compute is explicitly out of scope for this frame") |

**Net effect:** the graduation path (§0) works cleanly for a QRP-solar-class module (e.g., a
matured Pi 5 experiment moves from an experimentation-frame lower-power bay straight into the
isolation frame's experiment port using the same connector set) and is **structurally blocked**
for an intensive-class module, which is exactly the intended boundary — Jetson-class stays
experimentation-only by construction, not just by policy.

### Interface summary (both frames reference this table)

| Element | QRP-solar-class spec | Intensive-class spec |
|---|---|---|
| Power connector | Powerpole (PP-series) | SB-series (or other genuinely non-PP-mating family) — §3A |
| Data connector | RJ45 | RJ45 |
| Signal connector | Small keyed multi-pin connector (§3A) | Small keyed multi-pin connector (§3A), including the thermal-fault-status line |
| Protection location | Fuse + switch on the host bay/port, not on the module | Fuse + switch on the host bay/port, not on the module |
| Hot-swap | Not supported anywhere — insert-then-switch only | Not supported anywhere — insert-then-switch only |
| Thermal expectation | Passive/heatsink cooling only — no active heat rejection provided or required | Active heat rejection **required**, provided only by the experimentation frame's power-intensive bay (§1) |

🔎 **Verification tasks:** finalize the common tray/mounting envelope dimensions once real Pi 5
and Jetson-class carrier hardware is selected; verify the chosen PP-series and SB-series (or
equivalent) connector shells are genuinely non-interchangeable before purchase; confirm the
isolation frame's buck converter (§0A cross-reference) can be wired to present the exact same
connector set defined here.

---

## 4. Environmental exposure — the deliberate stress-test premise

- This frame is explicitly sited/built to experience **real Wisconsin weather extremes** (summer
  heat, winter cold, humidity, precipitation, wind) on its contents, within the bounds of the
  weathertight cabinet itself.
- The cabinet must still be weathertight (§0A, §3) — "exposed to weather" means thermal/seasonal
  exposure of what's inside a sealed (or deliberately, documentedly partially-vented per §1
  option b) enclosure, **not** an open-air or leaky enclosure by accident.
- **Jetson-class heat load (§1) is now the dominant summer stress case** — winter cold is more of
  a concern for Pi-class/lighter experiments and for condensation, but summer heat rejection with
  Jetson-class compute running is the harder problem and should be the first scenario tested.
- Data from this exposure (does a given Pi/Jetson/camera/sensor survive a Wisconsin summer and
  winter reliably? does it need a case modification, a different mount, a different duty cycle,
  more heat rejection margin?) is exactly the information the graduation gate uses before an
  experiment is trusted in the isolation frame.
- 🔎 **Verification task:** log a full seasonal cycle (or as much of one as the build timeline
  allows) — with particular attention to peak-summer thermal performance once Jetson-class
  hardware is installed — before treating any experiment as graduation-ready.

---

## 5. Network — fiber-preferred, same discipline as the rest of the site

Per CLAUDE.md's network architecture: prefer **fiber** for the data path to this enclosure and
**avoid copper Ethernet as the primary long outdoor run** (conductive lightning pathway). This
applies regardless of where this frame ends up sited (§8) — even a "near the shack" placement
should not casually default to a long exposed copper run without the same lightning-pathway
reasoning applied to the isolation frame's data path.

| Item | Pattern | Status |
|---|---|---|
| Uplink to shack | Fiber, terminated at a media converter inside the cabinet | 🟢 settled pattern, per CLAUDE.md |
| Inside-cabinet networking (experiment-to-switch, short runs within the sealed enclosure) | Short copper Ethernet inside the cabinet is acceptable — the lightning-pathway concern is specifically about the **long outdoor run**, not short intra-enclosure wiring | 🟢 settled pattern |
| Switch/media converter power | Off the cabinet's internal AC-derived DC supply (not budgeted here — this frame has no power limit) | 🟢 settled |

---

## 6. Telemetry & recovery

### What to log (locally, no cloud)

| Signal | Source | Why |
|---|---|---|
| AC presence / power state | Simple presence sensor or per-branch current sensor | Confirms the cabinet has power; catches an unexpected outage |
| Per-branch current (Pi-class and Jetson-class branches) | Inline current sensor per branch, if instrumented | Diagnoses which experiment is drawing what — feeds directly into §1's load calculation and eventual graduation sizing |
| Cabinet interior temperature/humidity | Dedicated temp/humidity sensor | Correlates with the deliberate weather-exposure premise (§4); also validates whichever thermal-management approach (§1) is chosen |
| Thermal-management system status (if option a or c is chosen) | Fan/pump status or simple runtime indicator on the heat-rejection hardware | A failed heat exchanger/loop is now a **safety-relevant** failure mode for Jetson-class hardware, not just a comfort issue — worth logging |
| Per-Pi / per-Jetson heartbeat/liveness | Simple local heartbeat log per unit (systemd + local log, no cloud) | Confirms each experiment is alive and recovering after events |

Same **no-cloud, no-persistent-dashboard** access model as the isolation frame
(`pi-field-station/power/README.md` §9): SSH + local log / one-shot status script, not a
persistent web dashboard. A persistent dashboard remains explicit deferred-backlog scope —
route to `scope-warden` if requested.

### Recover-after-power-loss (first-build acceptance requirement — same discipline as the isolation frame)

| Event | Required recovery behavior | Status |
|---|---|---|
| Grid outage / AC power loss and restoration | All experiment Pis/Jetsons auto-power-on when AC is restored; all field-station-pattern services enabled (not just started) via systemd so they self-start on boot | 🔒 required |
| Hung service/OS on any individual experiment unit | Documented systemd `Restart=` policy + watchdog where supported, mirroring `pi-field-station/systemd/` conventions | 🔒 required |
| Thermal-management fault (fan/pump failure on the Jetson heat-rejection system) | 🔒 **Should trigger a defined protective response** (e.g., throttle or shut down the affected Jetson branch) rather than allowing continued operation into an unmanaged thermal event — exact mechanism is an implementation task, not invented here | 🔒 required behavior, implementation = ❓ open |
| One experiment's fault | Must not take down another experiment's branch — this is the reason for individually fused/breakered, bulkhead-isolated branches (§2, §3) | 🔒 required, structural requirement not just software |
| **Net requirement** | After a grid outage, every experiment in the cabinet returns to normal operation **unattended** once AC is restored | 🔒 matches the isolation frame's recovery discipline |

---

## 7. Total field flexibility / relocatability

- This cabinet is a **self-contained, relocatable module** (§0A) — every coupling (AC in, DC out,
  sensor/telemetry/network lines, and any thermal-management wall penetration) is a bulkhead
  connector, so relocating it later is disconnect → move → reconnect, not a rewiring job.
- Because it is grid-AC-fed, relocation is bounded by where an AC feed can reasonably and safely
  be run — this is itself an electrician-scoped question if the frame moves any meaningful
  distance from the existing AC source.
- A sealed heat-exchanger or cold-plate thermal system (§1, options a/c) is itself a relocatable,
  bulkhead-mounted assembly by the same design law — it should not be field-improvised in a way
  that ties the cabinet to one specific spot.

---

## 8. Placement — default/primary recommendation (soft-open)

**Recommendation: site the experimentation frame near the shack / existing AC source and under
weather protection appropriate for an exposed lab bench** (e.g., near an eave or existing outdoor
AC circuit) — the opposite siting logic from the isolation frame:

| Factor | Isolation frame (recap) | Experimentation frame |
|---|---|---|
| Power source | Solar/battery — wants sun exposure decoupled from the electronics box (see isolation-frame §8) | AC — wants **proximity to an existing AC circuit**, not sun exposure |
| Grounding proximity | Wants the mast base for shortest single-point-ground bonding path | Still must bond into the same single-point-ground system (§2), but has no mast-proximity requirement driving its siting |
| Weather relationship | Wants to be **shaded/buffered** (isolation-frame §7) | **Deliberately weather-exposed** by design (§4) — proximity to the shack is about AC/data convenience, not weather avoidance |
| Thermal servicing | N/A | If a forced-ventilation or heat-exchanger system (§1) needs periodic filter/fin service, proximity to the shack also means proximity for maintenance access |

**This is a soft-open / default recommendation, not a fixed commitment** — per §0A and §7, both
frames are relocatable modules. Final placement for both frames is pending the field-enclosure
mounting-point milestone; do not pour concrete or finalize conduit/bulkhead penetration positions
for either frame before that siting is settled.

---

## 9. Bill of materials

Every line is marked **required / nice-to-have / deferred / do-not-buy-yet**. Model numbers and
prices below are **example/typical only** — none are asserted as verified for this build.

| # | Item | Function | Example spec (🔧 not verified) | Qty | Status |
|---|---|---|---|---|---|
| 1 | Weatherproof outdoor cabinet/enclosure, sized for **3–4 bays** | Housing, multi-experiment | Sized by mockup, §3 — dimensions depend on §1's thermal decision | 1 | **Required** |
| 2 | Weatherproof AC inlet connector (bulkhead) | AC coupling (§0A, §2) | Example only — final spec ⚠️ electrician | 1 | **Required** |
| 3 | GFCI protection device | AC safety | — | 1 | **Required** — ⚠️ spec by `grounding-safety-inspector`/electrician, do not select without pro review |
| 4 | Interior AC distribution block / breakered multi-outlet strip, rated for outdoor-cabinet use | Branch distribution (§2) | Example only | 1 | **Required** |
| 5 | Local AC service disconnect | Safety | — | 1 | **Required** — ⚠️ electrician |
| 6 | DIN rail / standoff mounting tray, per bay (module physical mount, §3/§3A) | Modular mounting (§3) | — | 3–4 bays | **Required** |
| 6a | Passive backplane harness / distribution panel (power/data distribution only, no active electronics — §3A) | Bay interconnect | Example/typical only — hand-wired or simple panel, not a custom PCB | 1 | **Required** |
| 6b | Per-bay Powerpole (PP-series) connector sets — lower-power bays | DC coupling, Pi-class rail (§2B, §3A) | Example/typical only | 2–3 sets | **Required** |
| 6c | Per-bay SB-series (or equivalent genuinely non-PP-mating) connector set — intensive bay | DC coupling, Jetson-class rail (§2A, §3A), **mechanical keying** | Example/typical only — verify true non-interchangeability with PP-series before purchase | 1 set | **Required**, safety-relevant selection |
| 6d | Per-bay RJ45 panel-mount couplers + patch cables | Data coupling (§3A, §5) | Standard COTS parts | 3–4 | **Required** |
| 6e | Per-bay small keyed signal connector (e.g., JST-VH-class) | Signal/telemetry/thermal-status coupling (§3A) | Example only — pin allocation ❓ open | 3–4 | **Required** |
| 6f | Per-bay inline fuse + faceplate-mounted switch | Per-bay protection, insert-then-switch (§3A) | Sized to bay rail class/current — not invented here | 3–4 sets | **Required** |
| 7 | Raspberry Pi 5 units + cases (lower-power bay payloads) | Compute, per bay | 🔧 baseline population per §0B: **2–3 units** | 2–3 | **Required** for the active lower-power bays; do not pre-buy beyond the §0B baseline |
| 8 | Jetson-class module + carrier board (power-intensive bay payload, e.g., AGX-Orin-class) | Compute, intensive bay | Example product class only — 🔧 wattage figures per §0B, not verified | 1 | **Required** once the intensive-bay experiment is actually being stood up — do not pre-buy |
| 9 | AC-DC power supply unit, regulated 12–19V DC output | Jetson-class DC rail (§2A) | Sized to ~60 W (§0B) + margin — not invented here | 1 | **Required** once Jetson-class hardware is added |
| 9a | AC-DC power supply unit / powered USB-C hub, regulated 5V DC output | Pi-class DC rail (§2B) | Sized to 2–3 bays × ~10–15 W (§0B) + margin | 1 | **Required** once Pi-class bays are populated |
| 11 | Sealed IP68 cable glands / multi-pin circular connectors | Sensor/signal/telemetry **cabinet-wall** bulkhead coupling (§0A — distinct from the internal per-bay connectors in items 6b–6e) | Example only | as needed | **Required** |
| 12 | Fiber media converter (cabinet end) | Network uplink (§5) | — | 1 | **Required**, per fiber-preferred network discipline |
| 13 | Short-run interior Ethernet switch/cabling | Intra-cabinet networking (§5) | — | 1 | **Required** |
| 14 | Cabinet interior temp/humidity sensor | Telemetry (§6) | — | 1 | **Required** |
| 15 | Per-branch current sensor(s) | Telemetry (§6) | — | as needed | **Nice-to-have** — useful for future graduation-sizing, not blocking |
| 16 | Gore protective vent(s) + desiccant, mounted facing down/sheltered | Pressure equalization + condensation control | Field-proven pattern (owner); low-temp rating and specific part = 🔧 not verified for this build | as needed | **Required**, mirrors isolation-frame practice — pairs with whichever thermal-management option (item 17) is selected |
| 17 | **Thermal-management hardware for Jetson-class heat load** — sealed air-to-air heat exchanger, **or** filtered/louvered forced-ventilation kit with rain hoods, **or** cold-plate/heat-pipe loop with wall-penetrating radiator | Heat rejection (§1) | **Approach not yet selected — this line is a placeholder pending the §1 decision and load-calc/mockup; do not purchase before that decision is made** | 1 system | **Required, but selection is a blocking open decision (§1)** — do not buy yet |
| 18 | Thermal-system status sensor (fan/pump runtime or fault indicator) | Telemetry, safety (§6) | — | 1 | **Required** once a thermal-management system (item 17) is selected |
| 19 | Bonding conductor, cabinet → single-point site ground | Grounding | Sized/spec by electrician | 1 run | **Required** — ⚠️ spec by `grounding-safety-inspector`/electrician |
| 20 | IP camera(s), for camera experiments | Experimental payload | — | as needed | **Nice-to-have / experimental** — lab-bench use only, see §0 scope note; do **not** treat as a permanent camera network |
| 21 | Weather instrument(s), for sensor experiments | Experimental payload | — | as needed | **Nice-to-have / experimental** — lab-bench use only, see §0 scope note; do **not** treat as a permanent weather-station service |
| 22 | Active climate control (heater/cooler) for *ambient* cabinet temperature (distinct from Jetson heat rejection, item 17) | Thermal management | — | — | **⏸ Do not buy yet** — contradicts the deliberate weather-exposure premise (§4) unless telemetry later justifies it |
| 23 | Cloud monitoring subscription / vendor cloud tier | Remote monitoring | — | — | **⏸ Do not buy yet** — against no-cloud-dependency discipline |
| 24 | Persistent web dashboard software/service | Monitoring UI | — | — | **⏸ Deferred** — out of first-build scope; route through `scope-warden` |
| 25 | LTE modem / permanent cellular failover | Connectivity | — | — | **Do-not-buy-yet** — explicit deferred-backlog item, not authorized by this frame's AC/multi-experiment flexibility |
| 26 | Permanent production camera network hardware (multiple fixed cameras, NVR, etc.) | Surveillance/production camera system | — | — | **Do-not-buy-yet** — "camera sprawl" is explicit deferred backlog; item 20 above is experimentation only |

---

## 10. Verification tasks (collected)

| # | Task | Ties to |
|---|---|---|
| 1 | GFCI, service disconnect, circuit sizing (against the §0B ≈130 W aggregate + margin), bonding, and wet-location-rating specification | §2 — ⚠️ `grounding-safety-inspector`/electrician, blocking |
| 2 | Confirm actual AC circuit rated capacity clears the §0B aggregate before populating all 3–4 bays | §2 |
| 3 | **Re-measure the §0B bay-level assumptions (intensive bay ~60 W, lower-power bays ~10–15 W each) with real hardware, and re-sum against a conservative local summer ambient design temperature** | §0B, §1 — blocking, precedes thermal-approach selection |
| 4 | **Select and mock-test a thermal-management approach (a/b/c), sized to the §0B aggregate, before finalizing cabinet size or BOM** | §0B, §1, §3, §9 |
| 5 | Verify Jetson-class module/carrier board DC input voltage/current requirements against the specific hardware selected | §2A |
| 5a | Verify Pi 5 DC input current draw (per unit) and confirm the §2B 5V supply is sized for the actual 2–3-bay count selected | §2B |
| 6 | Cabinet dry-fit mockup for **3–4 bays** once experiment count/size and thermal approach are known | §3 |
| 7 | Select bulkhead connector hardware (AC inlet, DC-out including higher-current Jetson branches, sensor glands, thermal-system penetration) against actual current/voltage/IP-rating needs | §0A |
| 8 | Confirm fiber media converter power draw and mounting fit inside cabinet | §5 |
| 9 | Log a full seasonal thermal/humidity cycle — with particular attention to peak-summer performance once Jetson-class hardware is installed — before treating any experiment as graduation-ready | §4 |
| 10 | Confirm systemd watchdog support on each experiment Pi/Jetson OS image | §6 |
| 11 | Define the protective response for a thermal-management fault (throttle/shutdown mechanism) | §6 |
| 12 | Bonding conductor sizing and single-point-ground verification | §2 — ⚠️ `grounding-safety-inspector`/electrician |
| 13 | Verify this frame's selected Gore vent's low-temp rating and mounting orientation (icing/snow) — same verification pattern as the isolation frame, not assumed carried over | §1, §3 |
| 14 | **Verify the selected PP-series and SB-series (or equivalent) connector shells are genuinely non-interchangeable** before purchase — this is the mechanical-keying safety mechanism | §3A |
| 15 | Finalize the common module tray/mounting envelope dimensions once real Pi 5 and Jetson-class carrier hardware is selected | §3B |
| 16 | Confirm the isolation frame's experiment port can be wired to present the exact §3A/§3B connector set (Powerpole + RJ45 + signal connector) | §3B — cross-check against `pi-field-station/power/README.md` §0A |
| 17 | Finalize per-bay signal-connector pin allocation once sensor/telemetry needs for each bay class are set | §3A |

---

## 11. Field-box test checklist (experimentation frame)

- [ ] 🔒 GFCI trips correctly on a test fault and cabinet AC de-energizes as expected (⚠️
      electrician-supervised test)
- [ ] 🔒 Single-point grounding continuity verified — no second ground path (⚠️
      `grounding-safety-inspector` sign-off)
- [ ] 🔒 Bulkhead integrity check — every AC, DC, sensor/telemetry, and thermal-system conductor/
      penetration crossing the enclosure wall uses a rated bulkhead connector/gland (§0A)
- [ ] 🔒 **Full power-cycle test:** de-energize and re-energize the AC feed, confirm every active
      experiment (Pi-class and Jetson-class) boots, all its systemd services come up
      automatically, and telemetry logging resumes **without any manual step**
- [ ] 🔎 One experiment's branch fault (e.g., pull its fuse/breaker) does not disturb another
      experiment's operation
- [ ] 🔒 **Thermal load test:** with Jetson-class hardware running under representative load on
      the hottest available test day (or a heated bench simulation), confirm the selected
      thermal-management approach (§1) holds interior temperature within the hardware's rated
      range; confirm the defined fault-response (§6) triggers correctly if the thermal system is
      deliberately disabled during the test
- [ ] Enclosure vent/desiccant inspected; no condensation evidence after a full weather cycle
- [ ] 🔎 **Winter vent inspection:** after a snow/ice event, confirm the Gore vent is not buried or
      iced over and is still functioning
- [ ] Cabinet interior temp/humidity log reviewed across a representative period and compared
      against the deliberate weather-exposure premise (§4)
- [ ] Fiber uplink verified functional; no unplanned copper long-run substituted
- [ ] 🔒 **Insert-then-switch swap test:** with a bay's switch OFF, disconnect and remove its
      module, install a replacement, reconnect, then switch back ON — confirm no other bay is
      disturbed and no live connector mating/unmating occurred (§3A)
- [ ] 🔎 **Mechanical keying check:** confirm the Jetson-class (SB-series) connector physically
      cannot be mated into a Pi-class (PP-series) bay socket, and vice versa (§3A)
- [ ] 🔎 **Cross-frame module portability test:** move a QRP-solar-class module from an
      experimentation-frame lower-power bay to the isolation frame's experiment port (power
      removed from both first) and confirm it connects with the shared connector set (§3B) without
      modification — this is the graduation gate exercised physically, not just as policy

---

## Related

- `pi-field-station/power/README.md` — the **isolation frame** (solar/battery certification,
  single-experiment, **Pi-class only — Jetson-class is explicitly out of scope there**).
  Experiments graduate from this frame into that one via the isolation frame's defined experiment
  port.
- `pi-field-station/README.md` — overall edge-services scope and the two-frame architecture
  overview.
- `docs/safety-grounding-bonding.md` — single-point-ground / bonded-entry discipline this frame
  must bond into; AC-safety items in §2 are owned by `grounding-safety-inspector`, not this
  document.
- `docs/safety-power-frames-bonding.md` — `grounding-safety-inspector`'s bonding/AC-safety/surge
  requirements specific to the two-frame outdoor power architecture (also flags the camera/
  weather-instrument scope tension raised in §0 for `scope-warden`).
- `docs/scope-ruling-dc-power-node.md` — scope-warden's ratification of the isolation frame's
  lean-load discipline; this experimentation frame is the explicit, bounded lab-bench exception
  where multi-experiment AC and Jetson-class loads are allowed, pending graduation.
- Sub-agents: `field-station-engineer` (this document's owner), `grounding-safety-inspector`
  (all AC-safety and bonding items in §2, and any wall-penetrating thermal-hardware review),
  `scope-warden` (any experiment trending toward a permanent deferred-backlog service — cameras,
  weather-station expansion, dashboard, LTE — and confirming Jetson-class stays bounded to this
  frame).
