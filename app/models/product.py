from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db


class Product(db.Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    slug: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(db.Text, nullable=False)
    price: Mapped[Decimal] = mapped_column(db.Numeric(10, 2), nullable=False)
    flavor: Mapped[str] = mapped_column(db.String(30), nullable=False)
    featured: Mapped[bool] = mapped_column(default=False, nullable=False)
