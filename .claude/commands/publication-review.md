---
description: Run the pre-publication privacy gate on an artifact before private → public
argument-hint: "[file or directory to review]"
allowed-tools: Read, Grep, Glob, Bash, Task
---

Run the **pre-publication review gate** on: $ARGUMENTS
(If no target is given, review everything currently staged in `private/sanitized-exports/` and any
file being proposed for the public repo.)

Delegate the judgment to the `geospatial-privacy-steward` sub-agent. It must answer each question
explicitly:

1. Does it include the real address?
2. A parcel number?
3. Real coordinates?
4. Real parcel geometry?
5. A real KML / KMZ / GPX / GeoJSON file (or shapefile / QGIS project)?
6. County GIS, Google Maps, or aerial imagery?
7. Road names or nearby landmarks?
8. EXIF GPS metadata? (For images, actually check — e.g. `exiftool` / `mdls` — don't assume.)
9. Does the filename reveal the location?
10. Could a motivated reader identify the home site from this artifact?

**If ANY answer is yes → do NOT publish.** Instead, describe exactly what would leak and produce a
sanitized derivative staged in `private/sanitized-exports/`.

Report the verdict as a table (question · yes/no · evidence), the overall
`safe_for_public_repo: true|false`, and — if unsafe — the specific sanitization steps needed.
