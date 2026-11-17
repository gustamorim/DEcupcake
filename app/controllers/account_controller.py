import re

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from app.auth import login_required
from app.extensions import db
from app.models import User

account_bp = Blueprint("account", __name__)
_DUMMY_HASH = generate_password_hash("senha-para-comparacao-interna")


@account_bp.after_request
def prevent_account_caching(response):
    response.headers["Cache-Control"] = "no-store"
    return response


@account_bp.get("/conta")
@login_required
def index():
    return render_template("account/index.html")


@account_bp.route("/conta/registro", methods=["GET", "POST"])
def register():
    if g.user:
        return redirect(url_for("account.index"))
    values = {"name": "", "email": ""}
    errors = {}
    if request.method == "POST":
        values = {"name": request.form.get("name", "").strip(),
                  "email": request.form.get("email", "").strip().lower()}
        password = request.form.get("password", "")
        if not 2 <= len(values["name"]) <= 100:
            errors["name"] = "Informe seu nome com 2 a 100 caracteres."
        if len(values["email"]) > 254 or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", values["email"]):
            errors["email"] = "Informe um e-mail válido."
        if not 8 <= len(password) <= 128 or not password.strip():
            errors["password"] = "Use uma senha de 8 a 128 caracteres."
        if password != request.form.get("password_confirmation", ""):
            errors["password_confirmation"] = "As senhas precisam ser iguais."
        if not errors:
            user = User(name=values["name"], email=values["email"])
            user.set_password(password)
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                errors["email"] = "Este e-mail já está cadastrado. Entre na sua conta."
            else:
                cart = session.get("cart", {})
                session.clear()
                session["cart"] = cart
                session["user_id"] = user.id
                flash("Conta criada com sucesso.", "success")
                return redirect(url_for("cart.index" if cart else "account.index"))
    return render_template("account/register.html", values=values, errors=errors), 422 if errors else 200


@account_bp.route("/conta/login", methods=["GET", "POST"])
def login():
    if g.user:
        return redirect(url_for("account.index"))
    email = ""
    error = None
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if len(email) > 254 or not 8 <= len(password) <= 128:
            error = "E-mail ou senha inválidos."
        else:
            user = db.session.scalar(db.select(User).where(User.email == email))
            valid = check_password_hash(user.password_hash if user else _DUMMY_HASH, password)
            if user and valid:
                cart = session.get("cart", {})
                session.clear()
                session["cart"] = cart
                session["user_id"] = user.id
                return redirect(url_for("cart.index" if cart else "account.index"))
            error = "E-mail ou senha inválidos."
    return render_template("account/login.html", email=email, error=error), 422 if error else 200


@account_bp.post("/conta/sair")
@login_required
def logout():
    session.clear()
    return redirect(url_for("account.login"))
