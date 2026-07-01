#!/usr/bin/env bash
#
# Location-leak scanner for the PUBLIC repo.
# Belt-and-suspenders backstop to .gitignore: catches sensitive CONTENT, not just filenames.
#
# Usage:
#   scripts/check-leaks.sh staged   # scan staged files   (used by the pre-commit hook)
#   scripts/check-leaks.sh all      # scan all tracked files (used by CI / manual audit)
#
# Exits non-zero if a likely location leak is found.
# Override a confirmed false positive for one commit with:  ALLOW_UNSANITIZED=1 git commit ...
#
# Detects:
#   - sensitive geospatial file types (even if force-added past .gitignore)
#   - filenames containing location tokens (parcel, survey, aerial, plat, ...)
#   - GPS EXIF metadata in images (requires exiftool; warns if not installed)
#   - decimal lat,lon coordinate-pair patterns in text files

MODE="${1:-staged}"
fail=0

RED=$'\033[31m'; YEL=$'\033[33m'; GRN=$'\033[32m'; RST=$'\033[0m'
note() { printf '  %s✗%s %s\n' "$RED" "$RST" "$1"; fail=1; }
warn() { printf '  %s!%s %s\n' "$YEL" "$RST" "$1"; }

if [ "$MODE" = "all" ]; then
  file_source() { git ls-files; }
else
  file_source() { git diff --cached --name-only --diff-filter=ACM; }
fi

# Sensitive geospatial extensions (must never appear in the public repo)
SENS_EXT='kml|kmz|gpx|geojson|shp|shx|dbf|prj|qgz|qgs|gpkg|gdb'
# Location tokens in filenames
TOKENS='parcel|survey|site-map|property-boundary|aerial|satellite|address|plat|csm'
# Two decimal-degree numbers (>=4 fractional digits) separated by comma/space -> likely lat,lon
COORD='[-+]?[0-9]{1,3}\.[0-9]{4,}[ ,]+[-+]?[0-9]{1,3}\.[0-9]{4,}'

scanned=0
while IFS= read -r f; do
  [ -n "$f" ] || continue
  [ -f "$f" ] || continue
  scanned=$((scanned + 1))
  base=${f##*/}
  ext_lc=$(printf '%s' "${base##*.}" | tr '[:upper:]' '[:lower:]')

  if printf '%s\n' "$ext_lc" | grep -qiE "^($SENS_EXT)$"; then
    note "$f — sensitive geospatial file type (.$ext_lc) must not be in the public repo"
  fi
  if printf '%s\n' "$base" | grep -qiE "$TOKENS"; then
    note "$f — filename contains a location token"
  fi

  case "$ext_lc" in
    jpg|jpeg|png|tif|tiff|heic)
      if command -v exiftool >/dev/null 2>&1; then
        if exiftool -s -n -GPSLatitude -GPSLongitude "$f" 2>/dev/null | grep -qiE 'GPS(Latitude|Longitude)'; then
          note "$f — image contains GPS EXIF metadata"
        fi
      else
        warn "$f — image not scanned for GPS EXIF (install exiftool: brew install exiftool)"
      fi
      ;;
    *)
      if grep -IEq "$COORD" "$f" 2>/dev/null; then
        note "$f — contains a decimal lat,lon coordinate-pair pattern"
      fi
      ;;
  esac
done < <(file_source)

echo
if [ "$fail" -ne 0 ]; then
  if [ "${ALLOW_UNSANITIZED:-}" = "1" ]; then
    printf '%s⚠ leak scan found issues but ALLOW_UNSANITIZED=1 — proceeding.%s\n' "$YEL" "$RST"
    printf '  Make sure this is a confirmed false positive.\n'
    exit 0
  fi
  printf '%sLeak scan FAILED%s (%d file(s) scanned). Do NOT publish these as-is.\n' "$RED" "$RST" "$scanned"
  printf 'Produce a sanitized derivative, or if this is a confirmed false positive:\n'
  printf '  ALLOW_UNSANITIZED=1 git commit ...\n'
  exit 1
fi
printf '%s✓ leak scan clean%s (%d file(s) scanned).\n' "$GRN" "$RST" "$scanned"
exit 0
