import secrets

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.extensions import db
from app.models import Product
from app.services.cart import cart_contents, quantity_from_form, save_cart

cart_bp = Blueprint("cart", __name__)


@cart_bp.after_request
def prevent_cart_caching(response):
    response.headers["Cache-Control"] = "no-store"
    return response


@cart_bp.get("/carrinho")
def index():
    rows, total = cart_contents()
    if "checkout_key" not in session:
        session["checkout_key"] = secrets.token_urlsafe(32)
    return render_template("cart/index.html", rows=rows, total=total)


@cart_bp.post("/carrinho/adicionar/<int:product_id>")
def add(product_id):
    product = db.get_or_404(Product, product_id)
    quantity = quantity_from_form(request.form.get("quantity", "1"))
    cart = dict(session.get("cart", {}))
    key = str(product.id)
    cart[key] = quantity_from_form(cart.get(key, 0) + quantity)
    save_cart(cart)
    flash(f"{product.name} adicionado ao carrinho.", "success")
    return redirect(url_for("cart.index"))


@cart_bp.post("/carrinho/atualizar/<int:product_id>")
def update(product_id):
    db.get_or_404(Product, product_id)
    cart = dict(session.get("cart", {}))
    quantity = quantity_from_form(request.form.get("quantity"))
    if str(product_id) in cart:
        cart[str(product_id)] = quantity
        save_cart(cart)
    return redirect(url_for("cart.index"))


@cart_bp.post("/carrinho/remover/<int:product_id>")
def remove(product_id):
    cart = dict(session.get("cart", {}))
    cart.pop(str(product_id), None)
    save_cart(cart)
    return redirect(url_for("cart.index"))
