"""Шифрует архивы глав паролем: temy/*/имя.zip → temy/*/имя.zip.enc.

В репозиторий попадают только .enc, сами .zip в .gitignore. Кнопка скачивания в book.js
спрашивает пароль, расшифровывает файл в браузере и отдаёт обычный .zip.

Формат .enc: b"ARZ1", соль 16 байт, вектор 12 байт, AES-256-GCM. Ключ — PBKDF2-SHA256
от пароля (без пробелов по краям, строчными буквами, NFC), ITER повторов.
Если архив не изменился, старый .enc остаётся, чтобы не менять файлы в git зря.

    ARCHIVE_PASSWORD=… python3 tools/lock.py
"""
import os
import sys
import unicodedata
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ROOT = Path(__file__).resolve().parent.parent
MAGIC = b"ARZ1"
ITER = 250_000


def key(password: str, salt: bytes) -> bytes:
    norm = unicodedata.normalize("NFC", password.strip().lower()).encode()
    return PBKDF2HMAC(SHA256(), 32, salt, ITER).derive(norm)


def decrypt(blob: bytes, password: str) -> bytes:
    salt, iv, body = blob[4:20], blob[20:32], blob[32:]
    return AESGCM(key(password, salt)).decrypt(iv, body, None)


def encrypt(data: bytes, password: str) -> bytes:
    salt, iv = os.urandom(16), os.urandom(12)
    return MAGIC + salt + iv + AESGCM(key(password, salt)).encrypt(iv, data, None)


if __name__ == "__main__":
    password = os.environ.get("ARCHIVE_PASSWORD")
    if not password:
        raise SystemExit("нужна переменная ARCHIVE_PASSWORD")
    for archive in sorted(ROOT.glob("temy/*/*.zip")):
        data = archive.read_bytes()
        locked = archive.with_name(archive.name + ".enc")
        if locked.exists():
            try:
                if decrypt(locked.read_bytes(), password) == data:
                    continue
            except Exception:
                pass
        locked.write_bytes(encrypt(data, password))
        print(f"  ✓ {locked.relative_to(ROOT)}")
    if "--verify" in sys.argv:
        for locked in sorted(ROOT.glob("temy/*/*.zip.enc")):
            assert decrypt(locked.read_bytes(), password)[:2] == b"PK", locked
        print("  все .enc открываются паролем")
