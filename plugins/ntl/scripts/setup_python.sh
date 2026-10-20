#!/bin/sh
# Install python-pptx (used by ntl_deck.py) into a cache folder when `python3 -c "import pptx"` does not already work.
#   sh setup_python.sh            -> prints the python to run build scripts with (ntl_deck.py finds the cache folder itself)
#   NTL_PY_CACHE=/tmp/x sh setup_python.sh   to choose the folder (e.g. where the home folder is read-only)
set -eu
PY=${PYTHON:-python3}
command -v "$PY" >/dev/null 2>&1 || { echo "python3 not found: install Python 3.9+ (https://www.python.org/downloads/)" >&2; exit 1; }
"$PY" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' || { echo "Python 3.9+ needed: $("$PY" --version 2>&1)" >&2; exit 1; }
if ! "$PY" -c "import pptx" >/dev/null 2>&1; then
  CACHE=${NTL_PY_CACHE:-${XDG_CACHE_HOME:-$HOME/.cache}/ntl-agent-skills/python}
  if ! mkdir -p "$CACHE" 2>/dev/null || [ ! -w "$CACHE" ]; then
    CACHE=${TMPDIR:-/tmp}/ntl-agent-skills/python
    mkdir -p "$CACHE"
  fi
  if ! PYTHONPATH="$CACHE" "$PY" -c "import pptx" >/dev/null 2>&1; then
    "$PY" -m pip install --quiet --disable-pip-version-check --target "$CACHE" "python-pptx>=1.0.2" >&2
  fi
  echo "python-pptx installed in $CACHE (ntl_deck.py looks there on its own)" >&2
fi
command -v "$PY"
