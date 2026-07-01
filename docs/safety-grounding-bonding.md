# Safety, Grounding & Bonding

**Classification:** `public-safe` — generic engineering discipline, no site-identifying information.

> 🔒 Grounding and bonding are **first-class, non-deferrable** requirements. This is a permanent,
> grounded, structural mast — not a casual temporary pole. This document describes **patterns and
> discipline**, not site-specific dimensions or code citations. Site values are field- and
> professional-verified. Engage a **licensed electrician, tower professional, and/or structural
> engineer**, and the **local authority having jurisdiction (AHJ)**, where indicated.

Legend: 🔒 safety requirement · 🟢 settled pattern · 🔎 field-verify · ❓ open question · ⚠️ pro review

---

## Guiding principles

- 🟢 **Single, coordinated grounding system — no isolated ground islands.** The mast/antenna
  grounding must be **bonded to the premises grounding electrode system**, so the whole site sits
  at a common potential during a fault or strike. ⚠️ Coordination with the building's electrical
  ground is an electrician/AHJ item.
- 🟢 **One coax entry point (single-point ground / bulkhead).** All coax and any outdoor conductors
  enter through **one bonded bulkhead/entry panel** where surge protection references ground.
- 🟢 **Bond, then protect.** Bond shields/enclosures/mast to the grounding system; add surge/
  lightning protective devices at the entry.
- 🟢 **Minimize conductive lightning pathways indoors.** Prefer **fiber** for the long outdoor data
  run; **avoid copper Ethernet** as the primary outdoor path (it carries surge energy toward
  equipment).
- 🔎 **Conservative weather assumptions** (wind, ice, and the local strike environment) inform every
  structural and protection decision.

## Layers of protection (concept)

| Layer | Purpose | Pattern | Owner |
|-------|---------|---------|-------|
| Mast/structure ground | Give strike energy a low-impedance path to earth | Ground electrode(s) at mast base, bonded to premises system | ⚠️ Electrician / tower pro |
| Coax bonding at top & bottom | Keep shields at ground potential | Bond coax shields per manufacturer/code practice | ⚠️ Electrician |
| Single-point entry / bulkhead | One controlled point where outdoor lines enter | Bonded bulkhead panel with coax surge arrestors | ⚠️ Electrician |
| Coax surge protection | Clamp transients before they reach the shack | Gas-tube / hybrid arrestors at the bulkhead | 🟢 Design |
| HF feedpoint protection | Protect the HF feed | Arrestor + drip loop + counterpoise/radial plan at/near mast base | 🟢 Design |
| AC/DC service protection | Protect powered equipment | SPDs on relevant power feeds | ⚠️ Electrician |
| Bonding of enclosures | Common potential | Bond field enclosure, Pi chassis, DC distribution to the grounding system | 🟢 Design |

## Mast & structural safety 🔒

- 🔎 Foundation, guy anchors, and tensioning are **field- and professional-verified** — never
  scaled from GIS/aerial/conceptual drawings.
- ⚠️ Foundation and anchor design (holding capacity, concrete, embedment) → **licensed structural
  engineer** where required by the AHJ.
- 🔒 Overhead power-line clearance vs. mast height **and the raising path** is a hard constraint —
  verify before assembly (see `checklists/pre-dig.md` and `checklists/mast-raise.md`).

## Coax & RF entry 🟢

- All coax returns to the shack **through the bonded bulkhead** with surge protection.
- 🟢 VHF/UHF: include lightning/surge protection; bond at the appropriate entry.
- 🟢 HF: feedpoint transformer, arrestor, drip loop, and counterpoise/radial plan at/near the mast
  base unless a better reason is documented. Coax returns through bonded protection.
- Keep the mast top uncluttered; no early side whips or unrelated services.

## Field enclosure & DC 🟢

- Bond the field enclosure, DC distribution, and Pi chassis into the grounding system.
- Low-power DC, minimal idle draw, graceful degradation, recover-after-power-loss.
- Fiber (or fiber-ready) data path preferred over copper for the outdoor run.

## What Claude / this repo must NOT do

- ❌ Do **not** state ground-rod count/depth, wire gauge, bonding-conductor size, arrestor models,
  concrete volumes, torque values, or code article numbers as if they were verified for this site.
  These are 🔎 **field-/pro-verified** and recorded (privately) once determined.
- ❌ Do **not** imply this is a temporary/throwaway install.

## Open questions & verification tasks

| Topic | To confirm | Owner |
|-------|-----------|-------|
| Applicable code editions & articles | ? | Electrician / AHJ |
| Ground electrode type/count/depth | ? | Electrician |
| Bonding conductor sizing | ? | Electrician |
| Coax arrestor selection | ? | Design + vendor specs |
| Foundation & anchor design | ? | Structural engineer (if required) |
| Permit/inspection requirements | ? | Local AHJ |
| Local strike/soil-resistivity environment | ? | Field assessment |

## Related

- `checklists/pre-dig.md` · `checklists/grounding-inspection.md` · `checklists/mast-raise.md`
- `docs/antenna-plan.md` · `docs/field-enclosure.md`
- Sub-agent: `grounding-safety-inspector` (use it for any grounding/bonding/structural question).
