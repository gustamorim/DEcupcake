import secrets

from flask import Blueprint, abort, flash, g, redirect, request, session, url_for
from sqlalchemy.exc import IntegrityError

from app.auth import login_required
from app.extensions import db
from app.models import Order, OrderItem
from app.services.cart import cart_contents

checkout_bp = Blueprint("checkout", __name__)


@checkout_bp.get("/checkout")
def index():
    return redirect(url_for("cart.index"))


@checkout_bp.post("/carrinho/finalizar")
@login_required
def finalize():
    key = request.form.get("checkout_key", "")
    if not key or not secrets.compare_digest(key.encode(), session.get("checkout_key", "").encode()):
        abort(400, description="O carrinho mudou. Recarregue a página antes de finalizar.")
    rows, _ = cart_contents()
    if not rows:
        flash("Adicione cupcakes ao carrinho antes de finalizar.", "info")
        return redirect(url_for("cart.index"))
    order = Order(user_id=g.user.id, checkout_key=key, items=[
        OrderItem(product_name=row["product"].name, quantity=row["quantity"],
                  unit_price=row["product"].price) for row in rows
    ])
    db.session.add(order)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        # Duas requisições da mesma compra não podem criar dois pedidos.
        existing = db.session.scalar(db.select(Order).where(
            Order.checkout_key == key, Order.user_id == g.user.id))
        if existing is None:
            raise
    session.pop("cart", None)
    flash("Pedido criado com sucesso!", "success")
    return redirect(url_for("orders.index"))
