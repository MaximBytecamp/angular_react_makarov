#!/bin/bash
# Проверка этапов главы 4.2 на копии проекта после главы 4.1: тесты, линтер и сборка на каждом этапе.
#   bash tools/verify_42.sh <папка с проектом после главы 4.1>
set -u
P=$1; C=$(dirname "$0")/code42; A=$(dirname "$0")/code41; B=$(dirname "$0")/proekt3-monitoring/src
run() { echo "== $1"; (cd "$P" && CI=true npx vitest run 2>&1 | grep -E "^ +(Test Files|Tests) " ); }
lint() { (cd "$P" && npx oxlint --deny-warnings 2>&1 | grep -E "jsx-a11y|Found" ); }
cp "$B/index.css" "$P/src/"; cp "$A/SitesPage.tsx" "$A/SitesPage.test.tsx" "$P/src/pages/"
cp "$A/App.test.tsx" "$A/MonitoringProvider.test.tsx" "$P/src/"
for f in SitePage AboutPage NotFoundPage; do cp "$B/pages/$f.tsx" "$P/src/pages/"; done
(cd "$P" && git checkout -q -- .oxlintrc.json); run "0 состояние после 4.1"
cp "$C/index.css" "$P/src/"
cp "$C/SitesPage-div.tsx" "$P/src/pages/SitesPage.tsx"; run "1 карточка на div (ждём 2 падения)"
cp "$C/oxlintrc.json" "$P/.oxlintrc.json"; echo "линтер с jsx-a11y:"; lint
cp "$A/SitesPage.tsx" "$P/src/pages/"
cp "$C/SitesPage-1.test.tsx" "$P/src/pages/SitesPage.test.tsx"; run "2 тест имени карточки (ждём 1 падение)"
cp "$C/SitesPage-2.tsx" "$P/src/pages/SitesPage.tsx"; run "3 название первым"
cp "$C/App.test.tsx" "$P/src/"; run "4 тест заголовка вкладки (ждём 1 падение)"
cp "$C/SitesPage-3.tsx" "$P/src/pages/SitesPage.tsx"; cp "$C/SitePage-1.tsx" "$P/src/pages/SitePage.tsx"
cp "$C/AboutPage.tsx" "$C/NotFoundPage.tsx" "$P/src/pages/"; run "5 заголовки вкладок"
cp "$C/SitesPage.test.tsx" "$P/src/pages/"; cp "$C/MonitoringProvider.test.tsx" "$P/src/"; run "6 тесты по ролям (ждём 2 падения)"
cp "$C/SitesPage.tsx" "$C/SitePage.tsx" "$P/src/pages/"; run "7 роли status и alert"
cp "$C/deploy.yml" "$P/.github/workflows/"
(cd "$P" && npx tsc -b && npx oxlint --deny-warnings >/dev/null && echo "tsc и oxlint --deny-warnings: без ошибок")
