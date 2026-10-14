"""
config.py — Loads and validates environment variables for the Desktop Client.

Required env vars (set in .env or system environment):
    FIREBASE_DB_URL        : Firebase Realtime Database URL
    SERVICE_ACCOUNT_PATH   : Path to Firebase Admin SDK service-account JSON
    PRIVATE_KEY_PATH       : Path to the RSA-2048 private key PEM file
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# ── Load .env from the same directory as this script ────────────────────────
_ENV_FILE = Path(__file__).resolve().parent / ".env"
load_dotenv(_ENV_FILE)


# ── Helper ──────────────────────────────────────────────────────────────────
def _require_env(var_name: str) -> str:
    """Return the value of an environment variable or exit with a clear error."""
    value = os.getenv(var_name)
    if not value:
        print(f"[ERROR] Missing required environment variable: {var_name}")
        print(f"        → Copy .env.example to .env and fill in your values.")
        sys.exit(1)
    return value


def _require_file(path_str: str, label: str) -> Path:
    """Resolve a path (relative to desktop_client/) and verify the file exists."""
    path = Path(path_str)
    if not path.is_absolute():
        path = Path(__file__).resolve().parent / path
    if not path.is_file():
        print(f"[ERROR] {label} not found at: {path}")
        sys.exit(1)
    return path


# ── Public configuration values ─────────────────────────────────────────────
FIREBASE_DB_URL: str = _require_env("FIREBASE_DB_URL")
SERVICE_ACCOUNT_PATH: Path = _require_file(
    _require_env("SERVICE_ACCOUNT_PATH"), "Firebase service-account key"
)
PRIVATE_KEY_PATH: Path = _require_file(
    _require_env("PRIVATE_KEY_PATH"), "RSA private key"
)


# ── Quick sanity check when run directly ─────────────────────────────────────
if __name__ == "__main__":
    print(f"   FIREBASE_DB_URL        : {FIREBASE_DB_URL}")
    print(f"   SERVICE_ACCOUNT_PATH   : {SERVICE_ACCOUNT_PATH}")
    print(f"   PRIVATE_KEY_PATH       : {PRIVATE_KEY_PATH}")
