---
description: Classify a project artifact with the standard visibility/geospatial header
argument-hint: "[file to classify]"
allowed-tools: Read, Grep, Glob, Edit
---

Classify the artifact: $ARGUMENTS

Inspect the file's actual contents (coordinates, parcel geometry, imagery, filenames, embedded
metadata) and emit the standard classification block:

```yaml
classification:
  visibility: private | public-safe | review-required
  geospatial_sensitivity: none | low | medium | high
  contains_real_coordinates: true | false
  contains_real_parcel_geometry: true | false
  contains_identifiable_imagery: true | false
  safe_for_public_repo: true | false
```

Rules:
- Real coordinates, real parcel geometry, identifiable imagery, or address-derived info ⇒
  `visibility: private`, `safe_for_public_repo: false`.
- If you cannot tell ⇒ default to `review-required` and treat as private.
- If the artifact is a data product (BOM / diagram / doc), also state the doc marker:
  `public-safe` · `private` · `review-required`, and for BOMs mark items
  `Required for first build` / `Nice to have` / `Deferred` / `Do not buy yet`.

Offer to write the classification header into the file (or a sidecar manifest under
`private/manifests/`). For borderline calls, hand off to `geospatial-privacy-steward`.
