from flask import Blueprint, render_template

from app.extensions import db
from app.models import Product

catalog_bp = Blueprint("catalog", __name__)


@catalog_bp.get("/catalogo")
def index():
    products = db.session.scalars(db.select(Product).order_by(Product.id)).all()
    return render_template("catalog/index.html", products=products)


@catalog_bp.get("/produto/<slug>")
def product(slug):
    item = db.first_or_404(db.select(Product).where(Product.slug == slug))
    return render_template("catalog/product.html", product=item)
