# bom/ — Bills of Materials

Every BOM item is marked with one of:

- **Required for first build**
- **Nice to have**
- **Deferred**
- **Do not buy yet**

Planned files: `first-build-bom.md`, `deferred-items.md`, `vendor-notes.md`.

Deferred (do not buy yet, do not derail the first build): rotator, beam/Yagi, remote transmit
radio, remote tuner (unless later justified), cameras, APRS, airband, LoRa, LTE failover, multiple
SDR services, weather-station expansion, high-power AC loads, solar/battery expansion beyond
validating the DC architecture.

Use the `field-docs-writer` and `scope-warden` sub-agents.
