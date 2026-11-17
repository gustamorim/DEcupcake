import os
import secrets

from sqlalchemy.pool import NullPool


def environment_config():
    """Lê a configuração no momento de criar a aplicação."""
    uri = os.environ.get("DATABASE_URL", "").strip() or "sqlite:///cupcake.db"
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql+psycopg://", 1)
    elif uri.startswith("postgresql://"):
        uri = uri.replace("postgresql://", "postgresql+psycopg://", 1)
    is_postgres = uri.startswith("postgresql+")
    return {
        "SQLALCHEMY_DATABASE_URI": uri,
        "SECRET_KEY": os.environ.get("SECRET_KEY") or secrets.token_hex(32),
        "SESSION_COOKIE_SECURE": os.environ.get("VERCEL") == "1",
        "AUTO_INIT_DB": uri.startswith("sqlite:"),
        "SQLALCHEMY_ENGINE_OPTIONS": {
            "poolclass": NullPool,
            "pool_pre_ping": True,
            "connect_args": {"connect_timeout": 10, "prepare_threshold": None},
        } if is_postgres else {},
    }


class Config:
    # O arquivo SQLite fica em instance/, fora dos arquivos públicos.
    SQLALCHEMY_DATABASE_URI = "sqlite:///cupcake.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    MAX_CONTENT_LENGTH = 1024 * 1024
