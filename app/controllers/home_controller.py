from flask import Blueprint, render_template

from app.extensions import db
from app.models import Product

home_bp = Blueprint("home", __name__)


@home_bp.get("/")
def index():
    products = db.session.execute(
        db.select(Product).where(Product.featured.is_(True)).order_by(Product.id).limit(3)
    ).scalars().all()
    return render_template("home/index.html", products=products)
