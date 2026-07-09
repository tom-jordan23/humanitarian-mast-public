# pi-field-station/ — Raspberry Pi edge services

The field enclosure at the mast base runs **edge services, not full remote radio operation.** No
primary transmit-radio functions here during the first build.

First-build services: Pi field station · lighting controller · BirdNET-ready microphone support ·
environmental sensors · DC power distribution · fiber/data termination · basic telemetry. (Possible
receive-only SDR *later*.)

Design standard: **low-power DC first**, solar-capable, minimal idle draw, **recovers automatically
after power loss**, remotely monitorable, no cloud dependency for core operation, fully documented
and reproducible.

```
services/               Service definitions / notes
scripts/                Small, inspectable scripts
config/                 Plain, documented configuration
systemd/                systemd units (self-restarting, idempotent boot)
power/                  ISOLATION FRAME: 12V DC solar power node spec + BOM (power/README.md)
experimentation-frame/  EXPERIMENTATION FRAME: AC-powered multi-experiment lab bench (NOT
                         field-validated) — experimentation-frame/README.md
```

## Two-frame power architecture (owner decision — settled)

DC power is split across two discrete, weathertight enclosures, each coupled only through
weathertight bulkheads (no ad-hoc pass-throughs):

- **Isolation frame** (`power/README.md`) — solar + battery, 12V, **one experiment/payload at a
  time**. This is the field-certification frame; default/primary siting is the mast base.
- **Experimentation frame** (`experimentation-frame/README.md`) — AC-powered, no power-budget
  limits, **multiple concurrent experiments** (including Jetson-class edge-AI compute),
  deliberately exposed to full weather. Explicitly a lab bench, **not field-validated**; default/
  primary siting is near the shack/AC source. Final placement for both is soft-open pending the
  field-enclosure mounting-point milestone.

**Graduation gate:** an experiment matures in the experimentation frame → ports into the
isolation frame as a single 12V load through its defined experiment port → is certified under
real solar/battery/weather. See `power/README.md` for the full architecture.

The Pi must support: local control · local logging · remote access over the site network ·
**recovery after reboot** · clear service documentation. Use the `field-station-engineer` sub-agent.
