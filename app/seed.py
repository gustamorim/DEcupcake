from decimal import Decimal

from app.extensions import db
from app.models import Product


def seed_products():
    products = [
        Product(name="Chocolate", slug="chocolate-dos-sonhos",
                description="Massa de chocolate com brigadeiro e cobertura de chocolate.",
                price=Decimal("12.90"), flavor="chocolate", featured=True),
        Product(name="Morango", slug="morango-com-carinho",
                description="Massa de baunilha com geleia e cobertura de morango.",
                price=Decimal("13.90"), flavor="morango", featured=True),
        Product(name="Baunilha", slug="baunilha-por-favor",
                description="Massa de baunilha com cobertura e confeitos.",
                price=Decimal("11.90"), flavor="baunilha", featured=True),
        Product(name="Pistache", slug="pistache-especial",
                description="Massa de baunilha com creme e cobertura de pistache.",
                price=Decimal("15.90"), flavor="pistache", featured=False),
        Product(name="Mirtilo", slug="mirtilo-encantado",
                description="Massa de baunilha com geleia e cobertura de mirtilo.",
                price=Decimal("14.90"), flavor="mirtilo", featured=False),
    ]
    existing = set(db.session.scalars(db.select(Product.slug)))
    db.session.add_all(product for product in products if product.slug not in existing)
    db.session.commit()
