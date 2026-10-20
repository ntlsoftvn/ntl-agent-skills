#!/bin/sh
# Install the Node packages of NTL pptx decks into a cache folder (idempotent) and print the NODE_PATH to use.
#   sh setup_node.sh            -> prints e.g. /Users/me/.cache/ntl-agent-skills/node/node_modules
#   NTL_NODE_CACHE=/tmp/x sh setup_node.sh   to choose the folder (e.g. where the home folder is read-only)
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
command -v node >/dev/null 2>&1 || { echo "node not found: install Node.js 18+ (https://nodejs.org)" >&2; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "npm not found: install Node.js 18+ (https://nodejs.org)" >&2; exit 1; }
CACHE=${NTL_NODE_CACHE:-${XDG_CACHE_HOME:-$HOME/.cache}/ntl-agent-skills/node}
if ! mkdir -p "$CACHE" 2>/dev/null || [ ! -w "$CACHE" ]; then
  CACHE=${TMPDIR:-/tmp}/ntl-agent-skills/node
  mkdir -p "$CACHE"
fi
if [ ! -f "$CACHE/package.json" ] || ! cmp -s "$HERE/package.json" "$CACHE/package.json" || [ ! -d "$CACHE/node_modules/pptxgenjs" ]; then
  cp "$HERE/package.json" "$CACHE/package.json"
  (cd "$CACHE" && npm install --no-audit --no-fund --loglevel=error >&2)
fi
echo "$CACHE/node_modules"
