from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class Order(db.Model):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"), nullable=False, index=True)
    checkout_key: Mapped[str] = mapped_column(db.String(64), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    items: Mapped[list["OrderItem"]] = relationship(cascade="all, delete-orphan", lazy="selectin")

    @property
    def total(self):
        return sum((item.subtotal for item in self.items), Decimal("0.00"))

    @property
    def created_at_local(self):
        # SQLite devolve o horário sem tzinfo; o valor persistido é UTC.
        return self.created_at.replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=-3)))


class OrderItem(db.Model):
    __tablename__ = "order_items"
    __table_args__ = (
        db.CheckConstraint("quantity > 0 AND quantity <= 99"),
        db.CheckConstraint("unit_price >= 0"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(db.ForeignKey("orders.id"), nullable=False, index=True)
    # Guarda o nome e o preço da compra mesmo se o catálogo mudar depois.
    product_name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(db.Numeric(10, 2), nullable=False)

    @property
    def subtotal(self):
        return self.unit_price * self.quantity
