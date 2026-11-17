import os
import secrets


class Config:
    # O arquivo SQLite fica em instance/, fora dos arquivos públicos.
    SQLALCHEMY_DATABASE_URI = "sqlite:///cupcake.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    MAX_CONTENT_LENGTH = 1024 * 1024
