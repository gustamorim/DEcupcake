import secrets
from decimal import Decimal

from flask import abort, session

from app.extensions import db
from app.models import Product


def quantity_from_form(value):
    try:
        quantity = int(value)
    except (TypeError, ValueError):
        abort(400, description="Informe uma quantidade inteira de 1 a 99.")
    if not 1 <= quantity <= 99:
        abort(400, description="Informe uma quantidade de 1 a 99.")
    return quantity


def cart_contents():
    cart = session.get("cart", {})
    products = db.session.scalars(db.select(Product).where(Product.id.in_(
        [int(key) for key in cart if key.isdecimal()]
    )).order_by(Product.id)).all()
    rows = []
    for product in products:
        quantity = cart.get(str(product.id))
        if isinstance(quantity, int) and 1 <= quantity <= 99:
            rows.append({"product": product, "quantity": quantity,
                         "subtotal": product.price * quantity})
    return rows, sum((row["subtotal"] for row in rows), Decimal("0.00"))


def save_cart(cart):
    session["cart"] = cart
    # Uma alteração no carrinho representa uma nova intenção de compra.
    session["checkout_key"] = secrets.token_urlsafe(32)
