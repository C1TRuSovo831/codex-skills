#!/usr/bin/env bash
# Offline installer for the skill snapshots in this repository.
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"

for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1 && \
     "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' >/dev/null 2>&1; then
    exec "$candidate" "$SCRIPT_DIR/scripts/install.py" "$@"
  fi
done

printf '%s\n' '[FAIL] Installer cannot start: Python 3.8 or newer is required.' >&2
printf '%s\n' 'No skills were installed. Install Python, then rerun this command.' >&2
printf '%s\n' 'Official Python downloads: https://www.python.org/downloads/' >&2
exit 2
