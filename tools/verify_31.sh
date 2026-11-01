#!/bin/sh
# Проверка промежуточных состояний главы 3.1 на копии проекта: tsc -b, oxlint, vite build.
#   sh tools/verify_31.sh <папка-копии-zayavki-с-react-router>
set -e
W="$1"; C="$(cd "$(dirname "$0")" && pwd)"
export PATH=/private/tmp/node24/node-v24.21.0-darwin-arm64/bin:/usr/bin:/bin
S="$W/src"; mkdir -p "$S/pages"
base() {
  cp "$C/code31/main.tsx" "$C/code31/index.css" "$S/"
  cp "$C/code14/Header.tsx" "$C/code16/RequestCard.tsx" "$S/components/"
  cp "$C/code31/BoardPage-2.tsx" "$S/pages/BoardPage.tsx"
  cp "$C/code31/StatsPage.tsx" "$S/pages/"
  rm -f "$S/pages/NotFoundPage.tsx" "$S/pages/RequestPage.tsx"
  cp "$C/code31/App-routes.tsx" "$S/App.tsx"
}
check() {
  echo "== $1"
  (cd "$W" && npx tsc -b && npx oxlint | tail -1 && npx vite build --logLevel error && echo "   сборка: ок")
}
base; check "§2 маршруты / и /stats"
cp "$C/code31/NotFoundPage.tsx" "$S/pages/"; cp "$C/code31/App-notfound.tsx" "$S/App.tsx"; check "§2 маршрут *"
cp "$C/code31/Header-a.tsx" "$S/components/Header.tsx"; check "§3 опыт с <a href>"
cp "$C/code31/Header.tsx" "$S/components/"; check "§3 NavLink"
cp "$C/code31/RequestCard.tsx" "$S/components/"; cp "$C/code31/BoardPage.tsx" "$S/pages/"
cp "$C/code31/RequestPage.tsx" "$S/pages/"; cp "$C/code31/App.tsx" "$S/App.tsx"; check "§4 итог главы"
