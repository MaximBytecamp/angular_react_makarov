#!/bin/bash
# Проверка этапов главы 4.1 на копии проекта: сколько тестов проходит на каждом этапе.
#   bash tools/verify_41.sh <папка с проектом после П3 и установленными пакетами тестов>
set -u
P=$1; C=$(dirname "$0")/code41; B=$(dirname "$0")/proekt3-monitoring/src
run() { echo "== $1"; (cd "$P" && CI=true npx vitest run 2>&1 | grep -E "^ +(Test Files|Tests) " ); }
cp "$C/vite.config.ts" "$P/"; cp "$C/setupTests.ts" "$P/src/"
rm -f "$P"/src/*.test.ts* "$P"/src/pages/*.test.tsx "$P/src/plural.ts"
cp "$B/pages/SitesPage.tsx" "$P/src/pages/"; cp "$B/status.ts" "$P/src/"
cp "$C/status.test.ts" "$P/src/"; run "1 status.test"
cp "$C/status-slomano.ts" "$P/src/status.ts"; run "2 сломанный status.ts (ждём 1 падение)"
cp "$B/status.ts" "$P/src/"
cp "$C/SitesPage-1.test.tsx" "$P/src/pages/SitesPage.test.tsx"; run "3 три теста страницы"
cp "$C/SitesPage.test.tsx" "$P/src/pages/"; run "4 тесты по требованиям (ждём 2 падения)"
cp "$C/SitesPage-kopiya.test.tsx" "$P/src/pages/SitesPage.test.tsx"; run "5 копия поведения (ждём всё зелёное)"
cp "$C/SitesPage.test.tsx" "$P/src/pages/"
cp "$C/plural.ts" "$C/plural.test.ts" "$C/App.test.tsx" "$C/MonitoringProvider.test.tsx" "$P/src/"
cp "$C/SitesPage.tsx" "$P/src/pages/"; run "6 исправление и все тесты"
(cd "$P" && npx tsc -b && npx oxlint && echo "tsc и oxlint: без ошибок")
