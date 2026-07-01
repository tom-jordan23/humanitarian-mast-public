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
services/   Service definitions / notes
scripts/    Small, inspectable scripts
config/     Plain, documented configuration
systemd/    systemd units (self-restarting, idempotent boot)
```

The Pi must support: local control · local logging · remote access over the site network ·
**recovery after reboot** · clear service documentation. Use the `field-station-engineer` sub-agent.
