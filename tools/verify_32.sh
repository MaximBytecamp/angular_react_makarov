#!/bin/sh
# Проверка промежуточных состояний главы 3.2 на копии проекта с react-router: tsc -b, oxlint, vite build.
#   sh tools/verify_32.sh <папка-копии-zayavki>
W="$1"; C="$(cd "$(dirname "$0")" && pwd)"
export PATH=/private/tmp/node24/node-v24.21.0-darwin-arm64/bin:/usr/bin:/bin
S="$W/src"; mkdir -p "$S/pages"
# Конец главы 3.1.
cp "$C/code31/main.tsx" "$C/code31/App.tsx" "$C/code31/index.css" "$S/"
cp "$C/code31/Header.tsx" "$C/code31/RequestCard.tsx" "$S/components/"
for p in BoardPage StatsPage RequestPage NotFoundPage; do cp "$C/code31/$p.tsx" "$S/pages/"; done
check() {
  echo "== $1"
  (cd "$W" && npx tsc -b && npx oxlint && npx vite build --logLevel error && echo "   сборка: ок")
}
cp "$C/code32/board.ts" "$C/code32/BoardProvider.tsx" "$S/"; cp "$C/code32/App-context.tsx" "$S/App.tsx"
check "§2 App читает useBoard, провайдера ещё нет"
cp "$C/code32/main.tsx" "$S/"; check "§2 провайдер в main.tsx"
for p in StatsPage RequestPage BoardPage; do cp "$C/code32/$p.tsx" "$S/pages/"; done
cp "$C/code32/Header.tsx" "$S/components/"; check "§3 страницы на контексте, App ещё передаёт props"
cp "$C/code32/App.tsx" "$S/"; check "§3 итог главы"
