import secrets
from functools import wraps

from flask import abort, g, redirect, request, session, url_for

from app.extensions import db
from app.models import User


def csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


def init_auth(app):
    app.jinja_env.globals["csrf_token"] = csrf_token

    @app.before_request
    def load_user_and_check_csrf():
        user_id = session.get("user_id")
        g.user = db.session.get(User, user_id) if isinstance(user_id, int) else None
        if user_id is not None and g.user is None:
            session.clear()
        if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            expected = session.get("csrf_token", "")
            submitted = request.form.get("csrf_token", "")
            if not expected or not secrets.compare_digest(expected.encode(), submitted.encode()):
                abort(400, description="Formulário expirado ou inválido. Recarregue a página e tente novamente.")


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("account.login"))
        return view(*args, **kwargs)
    return wrapped
