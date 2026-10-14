#!/bin/bash
# Validate JSON records offline against a building block (run local-build/fetch-imports.sh first).
# Usage: local-build/validate.sh [-p] [-b block] record.json...
#   blocks from the local build (build-local/); -p: published register; default block: workflow/model-of-models
set -euo pipefail
REPO=$(cd "$(dirname "$0")/.." && pwd)
IMAGE=${BBP_IMAGE:-ghcr.io/opengeospatial/bblocks-postprocess@sha256:313a22ecfdb8688a6984474bd4d3eebdd493a845bc1e2fe018800867646c5b97}  # pinned; tested version
ARGS=()
while getopts "pb:" o; do
  case $o in
    b) ARGS+=(-b "$OPTARG") ;;
    p) ARGS+=(--published) ;;
    *) exit 2 ;;
  esac
done
shift $((OPTIND - 1))
[ $# -gt 0 ] || { echo "Usage: $0 [-p] [-b block] record.json..."; exit 2; }

MOUNTS=()
FILES=()
for f in "$@"; do
  [ -f "$f" ] || { echo "Not a file: $f"; exit 2; }
  f=$(realpath "$f")
  MOUNTS+=(-v "$f:/records$f:ro")
  FILES+=("/records$f")
done
[ -d "$REPO/.imports-cache" ] || { echo "Run local-build/fetch-imports.sh first"; exit 2; }
docker run --rm --network none --workdir /workspace -v "$REPO:/workspace:ro" "${MOUNTS[@]}" \
  --entrypoint /venv/bin/python "$IMAGE" -I -W ignore local-build/validate.py "${ARGS[@]}" "${FILES[@]}" \
  | sed 's#^\(PASS\|FAIL\) /records#\1 #'
exit "${PIPESTATUS[0]}"
