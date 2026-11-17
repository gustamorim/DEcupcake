from pathlib import Path

import click
from flask import Flask

from config import Config
from app.extensions import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

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

    # Facilita o primeiro uso: cria tabelas e exemplos na primeira execução.
    with app.app_context():
        db.create_all()
        seed_products()

    return app
