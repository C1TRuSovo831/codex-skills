#!/usr/bin/env bash
# Explicit online installation of the three pinned research skills.
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1 && \
     "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' >/dev/null 2>&1; then
    exec "$candidate" -B "$SCRIPT_DIR/scripts/download_research_skills.py" "$@"
  fi
done
printf '%s\n' '[FAIL] Python 3.8 or newer is required. No skills were downloaded.' >&2
exit 2
