#!/bin/sh
# Render a .pptx to PDF and PNG pages for visual QA:  sh render.sh deck.pptx out_dir [dpi]
# Uses Keynote on macOS when installed, else LibreOffice (soffice); PNGs need poppler (pdftoppm).
# Keynote may not draw native charts: check chart slides in PowerPoint or LibreOffice.
set -eu
[ $# -ge 2 ] || { echo "usage: render.sh deck.pptx out_dir [dpi]" >&2; exit 2; }
IN=$(cd "$(dirname "$1")" && pwd)/$(basename "$1"); OUT=$2; DPI=${3:-60}
mkdir -p "$OUT"; OUT=$(cd "$OUT" && pwd); PDF="$OUT/$(basename "${IN%.*}").pdf"
if [ "$(uname)" = "Darwin" ] && [ -d "/Applications/Keynote.app" ]; then
  osascript -e "tell application \"Keynote\"
    set d to open POSIX file \"$IN\"
    export d to POSIX file \"$PDF\" as PDF
    close d saving no
  end tell" >/dev/null
elif command -v soffice >/dev/null 2>&1; then
  soffice --headless --convert-to pdf --outdir "$OUT" "$IN" >/dev/null
else
  echo "no renderer: install LibreOffice (soffice) or, on macOS, Keynote; skipping visual QA" >&2; exit 3
fi
if command -v pdftoppm >/dev/null 2>&1; then
  pdftoppm -r "$DPI" -png "$PDF" "$OUT/slide"
  ls "$OUT"/slide-*.png
else
  echo "pdftoppm not found (install poppler): only the PDF was written: $PDF" >&2
  echo "$PDF"
fi
