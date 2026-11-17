from pathlib import Path
import os

import click
from flask import Flask

from config import Config, environment_config
from app.extensions import db


def create_app(test_config=None):
    on_vercel = os.environ.get("VERCEL") == "1"
    app = Flask(__name__, instance_relative_config=True,
                static_folder=None if on_vercel else "../public/static",
                static_url_path="/static")
    app.config.from_object(Config)
    app.config.update(environment_config())
    if test_config:
        app.config.update(test_config)

    if on_vercel:
        if not os.environ.get("DATABASE_URL") or not os.environ.get("SECRET_KEY"):
            raise RuntimeError("Configure DATABASE_URL e SECRET_KEY no painel da Vercel.")
        if not app.config["SQLALCHEMY_DATABASE_URI"].startswith("postgresql+"):
            raise RuntimeError("Use PostgreSQL em DATABASE_URL na Vercel.")
        # Os arquivos são servidos pelo CDN a partir de public/static/.
        app.add_url_rule("/static/<path:filename>", endpoint="static", build_only=True)
    elif app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite:"):
        Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)

    from app.models import Product
    from app.controllers import register_controllers
    from app.seed import seed_products
    from app.auth import init_auth

    init_auth(app)
    register_controllers(app)

    @app.template_filter("brl")
    def brl(value):
        return f"R$ {value:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")

    @app.cli.command("init-db")
    def init_db():
        """Cria as tabelas e adiciona produtos de exemplo sem duplicá-los."""
        db.create_all()
        seed_products()
        click.echo("Banco inicializado com sucesso.")

    # PostgreSQL é inicializado explicitamente com `flask --app run init-db`.
    # Evita disputar criação de tabelas entre instâncias da Vercel.
    if app.config["AUTO_INIT_DB"]:
        with app.app_context():
            db.create_all()
            seed_products()

    return app
