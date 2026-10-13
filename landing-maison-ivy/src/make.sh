#!/bin/bash
# Usage: ./make.sh  (régénère captures + 2 PDF)
set -e
cd "$(dirname "$0")"
export NODE_PATH=/opt/node22/lib/node_modules
SH=$(cd ../assets && pwd)/shots

sed "s#url('fonts/#url('file://$(pwd)/fonts/#g" fonts/local-fonts.css > fonts-abs.css
node logo.js >/dev/null
node sections.js ../maquette/index.html "$SH" | grep -v proxy || true
build () { # $1=script $2=out.pdf
  python3 "$1" "$SH" "" .tmp.html
  node pdf.js .tmp.html .tmp.pdf
  python3 pages.py .tmp.pdf .tmp.html > .pages.json
  python3 "$1" "$SH" .pages.json .tmp.html
  node pdf.js .tmp.html "$2"
  rm -f .tmp.html .tmp.pdf .pages.json
}
build build_analyse.py "../docs/MaisonIvy_1_Analyse_des_options.pdf"
[ -f build_proposition.py ] && build build_proposition.py "../docs/MaisonIvy_2_Proposition_finale.pdf"
echo done
