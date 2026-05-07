import os
from pathlib import Path

import asyncpg


ROOT_DIR = Path(__file__).resolve().parents[1]
SERVER_DIR = Path(__file__).resolve().parent


def load_local_env():
    for env_path in (ROOT_DIR / ".env", SERVER_DIR / ".env"):
        if not env_path.exists():
            continue
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key:
                os.environ.setdefault(key, value)


def database_url():
    return (
        os.getenv("SUPABASE_SESSION_POOL_URL")
        or os.getenv("DATABASE_URL")
        or os.getenv("POSTGRES_URL")
    )


async def init_db_pool(app):
    load_local_env()
    dsn = database_url()
    if not dsn:
        app.state.db_pool = None
        return

    app.state.db_pool = await asyncpg.create_pool(
        dsn=dsn,
        min_size=int(os.getenv("DB_POOL_MIN_SIZE", "1")),
        max_size=int(os.getenv("DB_POOL_MAX_SIZE", "5")),
        command_timeout=float(os.getenv("DB_COMMAND_TIMEOUT", "30")),
        server_settings={"application_name": "vlade-api"},
    )


async def close_db_pool(app):
    pool = getattr(app.state, "db_pool", None)
    if pool:
        await pool.close()


def get_db_pool(request):
    pool = getattr(request.app.state, "db_pool", None)
    if pool is None:
        return None
    return pool
