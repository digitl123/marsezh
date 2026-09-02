#!/bin/sh
# Пересобирает обе версии и раскладывает их в docs/ — оттуда их отдаёт GitHub Pages.
set -e
cd "$(dirname "$0")"
python3 build.py
python3 build-dark.py
cp index.html      docs/light.html
cp index-dark.html docs/dark.html
echo "docs/ обновлён. Дальше: git add -A && git commit -m 'update' && git push"
