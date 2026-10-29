"""Архивы проекта zayavki для глав модуля 1: состояние в начале и в конце главы.

Основа — проект, созданный командой из главы 1.1 (tools/shots_11.py project):
настройки, package.json и package-lock.json берутся из него, папки node_modules
и dist в архив не попадают. Файлы src/ накладываются из tools/codeNN.

    python3 tools/pack.py           # собрать все архивы в папки глав
    python3 tools/pack.py --check   # собрать и проверить: npm ci, tsc -b, oxlint, vite build
"""
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import cdp  # noqa: E402
import shots_11 as s11  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TOOLS = Path(__file__).parent
BASE = s11.PROJECT
SKIP = {"node_modules", "dist", "src"}

# Состояние проекта: файл в src/ → источник (путь от tools/ или готовый текст).
AFTER_11 = {"App.tsx": s11.KARKAS_APP, "index.css": s11.KARKAS_CSS}
AFTER_12 = {
    "App.tsx": "code12/App.tsx", "index.css": "code12/index.css",
    "components/Header.tsx": "code12/Header.tsx",
    "components/RequestForm.tsx": "code12/RequestForm.tsx",
    "components/RequestCard.tsx": "code12/RequestCard.tsx",
}
AFTER_13 = {**AFTER_12, "App.tsx": "code13/App.tsx", "components/RequestCard.tsx": "code13/RequestCard.tsx"}
AFTER_14 = {
    **AFTER_13, "App.tsx": "code14/App.tsx", "index.css": "code14/index.css",
    "components/Header.tsx": "code14/Header.tsx", "components/RequestCard.tsx": "code14/RequestCard.tsx",
}
AFTER_15 = {
    **AFTER_14, "App.tsx": "code15/App.tsx", "index.css": "code15/index.css",
    "requests.ts": "code15/requests.ts", "components/RequestCard.tsx": "code15/RequestCard.tsx",
}

AFTER_16 = {
    **AFTER_15, "App.tsx": "code16/App.tsx", "index.css": "code16/index.css",
    "requests.ts": "code16/requests.ts", "components/RequestCard.tsx": "code16/RequestCard.tsx",
    "components/RequestForm.tsx": "code16/RequestForm.tsx",
}

AFTER_17 = {
    **AFTER_16, "App.tsx": "code17/App.tsx", "index.css": "code17/index.css",
    "storage.ts": "code17/storage.ts", "notify.ts": "code17/notify.ts",
}

AFTER_21 = {**AFTER_17, "App.tsx": "code21/App.tsx"}

ARCHIVES = [
    ("11-node-npm-vite", "zayavki-konec-1-1.zip", AFTER_11),
    ("12-jsx-i-komponenty", "zayavki-nachalo-1-2.zip", AFTER_11),
    ("12-jsx-i-komponenty", "zayavki-konec-1-2.zip", AFTER_12),
    ("13-props", "zayavki-nachalo-1-3.zip", AFTER_12),
    ("13-props", "zayavki-konec-1-3.zip", AFTER_13),
    ("14-sostoyanie-i-sobytiya", "zayavki-nachalo-1-4.zip", AFTER_13),
    ("14-sostoyanie-i-sobytiya", "zayavki-konec-1-4.zip", AFTER_14),
    ("15-spiski-i-usloviya", "zayavki-nachalo-1-5.zip", AFTER_14),
    ("15-spiski-i-usloviya", "zayavki-konec-1-5.zip", AFTER_15),
    ("16-formy", "zayavki-nachalo-1-6.zip", AFTER_15),
    ("16-formy", "zayavki-konec-1-6.zip", AFTER_16),
    ("17-sohranenie-i-otpravka", "zayavki-nachalo-1-7.zip", AFTER_16),
    ("17-sohranenie-i-otpravka", "zayavki-konec-1-7.zip", AFTER_17),
    ("21-effekty", "zayavki-nachalo-2-1.zip", AFTER_17),
    ("21-effekty", "zayavki-konec-2-1.zip", AFTER_21),
]


def assemble(state: dict[str, str], dest: Path) -> None:
    """Папка zayavki в dest: основа проекта и файлы src/ из state."""
    for item in BASE.iterdir():
        if item.name in SKIP or item.name.endswith(".tsbuildinfo"):
            continue
        (shutil.copytree if item.is_dir() else shutil.copy)(item, dest / item.name)
    src = dest / "src"
    src.mkdir()
    shutil.copy(BASE / "src/main.tsx", src / "main.tsx")
    for rel, source in state.items():
        (src / rel).parent.mkdir(parents=True, exist_ok=True)
        if "\n" in source:
            (src / rel).write_text(source)
        else:
            shutil.copy(TOOLS / source, src / rel)


def pack(state: dict[str, str], archive: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp) / "zayavki"
        project.mkdir()
        assemble(state, project)
        archive.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
            for path in sorted(project.rglob("*")):
                zf.write(path, path.relative_to(tmp))
    print(f"  ✓ {archive.relative_to(ROOT)}  {archive.stat().st_size // 1024} КБ")


def check(archive: Path) -> None:
    """Распаковка в пустую папку и те же команды, что выполняет студент."""
    env = {"PATH": f"{cdp.NODE_BIN}:/usr/bin:/bin", "HOME": str(Path.home()),
           "npm_config_update_notifier": "false", "npm_config_fund": "false", "npm_config_audit": "false"}
    with tempfile.TemporaryDirectory() as tmp:
        zipfile.ZipFile(archive).extractall(tmp)
        project = Path(tmp) / "zayavki"
        for cmd in (["npm", "ci", "--prefer-offline"], ["npx", "tsc", "-b"], ["npx", "oxlint"], ["npx", "vite", "build"]):
            run = subprocess.run(cmd, cwd=project, env=env, capture_output=True, text=True)
            noisy = cmd[1] == "oxlint" and "Found 0 warnings and 0 errors" not in run.stdout
            if run.returncode or noisy:
                raise SystemExit(f"{archive.name}: {' '.join(cmd)}\n{run.stdout}{run.stderr}")
    print(f"    проверен: npm ci, tsc -b, oxlint, vite build")


if __name__ == "__main__":
    for chapter, name, state in ARCHIVES:
        target = ROOT / "temy" / chapter / name
        pack(state, target)
        if "--check" in sys.argv:
            check(target)
