from flask import Blueprint, flash, g, redirect, render_template, url_for
from app.auth import login_required
from app.extensions import db
from app.models import Order

order_bp = Blueprint("orders", __name__)


@order_bp.after_request
def prevent_order_caching(response):
    response.headers["Cache-Control"] = "no-store"
    return response


@order_bp.get("/pedidos")
@login_required
def index():
    orders = db.session.scalars(db.select(Order).where(Order.user_id == g.user.id)
                                .order_by(Order.created_at.desc(), Order.id.desc())).all()
    return render_template("orders/index.html", orders=orders)


@order_bp.post("/pedidos/<int:order_id>/excluir")
@login_required
def delete(order_id):
    order = db.first_or_404(db.select(Order).where(Order.id == order_id, Order.user_id == g.user.id))
    db.session.delete(order)
    db.session.commit()
    flash("Pedido excluído.", "success")
    return redirect(url_for("orders.index"))
