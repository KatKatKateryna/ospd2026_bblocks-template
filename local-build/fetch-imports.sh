#!/bin/bash
# Download everything offline validation needs into .imports-cache/.
# Usage: local-build/fetch-imports.sh [-p]   (default: blocks from build-local/, run ./build.sh first; -p: published register)
set -euo pipefail
cd "$(dirname "$0")/.."
IMAGE=${BBP_IMAGE:-ghcr.io/opengeospatial/bblocks-postprocess@sha256:313a22ecfdb8688a6984474bd4d3eebdd493a845bc1e2fe018800867646c5b97}  # pinned; tested version
ARGS=()
if [ "${1:-}" = "-p" ]; then
  ARGS=(--published)
elif [ ! -f build-local/register.json ]; then
  echo "No build-local/; run ./build.sh first (or -p for published blocks)"
  exit 2
fi
docker pull -q "$IMAGE" > /dev/null
rm -rf .imports-cache.new
docker run --rm --workdir /workspace -v "$(pwd):/workspace" -e IMPORTS_CACHE=/workspace/.imports-cache.new \
  --entrypoint /venv/bin/python "$IMAGE" -I -W ignore local-build/validate.py --fetch "${ARGS[@]}"
rm -rf .imports-cache
mv .imports-cache.new .imports-cache
echo "Ready for offline validation"
