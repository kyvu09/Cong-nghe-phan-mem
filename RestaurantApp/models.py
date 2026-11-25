from datetime import datetime
from enum import Enum as PyEnum
from flask_login import UserMixin
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime,
    ForeignKey, Enum, UniqueConstraint, CheckConstraint
)
from sqlalchemy.orm import relationship
from RestaurantApp import db


class UserRole(PyEnum):
    WAITER = "WAITER"
    KITCHEN = "KITCHEN"
    CASHIER = "CASHIER"
    ADMIN = "ADMIN"


class TableStatus(PyEnum):
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"


class OrderStatus(PyEnum):
    OPEN = "OPEN"
    PAID = "PAID"


class ItemStatus(PyEnum):
    PENDING = "PENDING"
    COOKING = "COOKING"
    COMPLETED = "COMPLETED"


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.WAITER)
    active = Column(Boolean, default=True)

    def __str__(self):
        return self.name


class Category(db.Model):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    dishes = relationship("Dish", backref="category", lazy=True)

    def __str__(self):
        return self.name


class Dish(db.Model):
    __tablename__ = "dish"
    __table_args__ = (
        CheckConstraint("price > 0", name="ck_dish_price_positive"),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(20), nullable=False, unique=True)
    name = Column(String(150), nullable=False)
    price = Column(Float, nullable=False)
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)

    def __str__(self):
        return f"[{self.code}] {self.name}"


class DiningTable(db.Model):
    __tablename__ = "dining_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    table_number = Column(String(10), nullable=False, unique=True)
    status = Column(Enum(TableStatus), nullable=False, default=TableStatus.AVAILABLE)
    orders = relationship("Order", backref="table", lazy=True)

    def __str__(self):
        return f"Bàn {self.table_number}"


class Order(db.Model):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    table_id = Column(Integer, ForeignKey("dining_table.id"), nullable=False)
    waiter_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.OPEN)

    waiter = relationship("User", foreign_keys=[waiter_id])
    details = relationship("OrderDetail", backref="order", lazy=True, cascade="all, delete-orphan")
    invoice = relationship("Invoice", backref="order", uselist=False, lazy=True)


class OrderDetail(db.Model):
    __tablename__ = "order_detail"
    __table_args__ = (
        UniqueConstraint("order_id", "dish_id", name="uq_order_dish"),
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    dish_id = Column(Integer, ForeignKey("dish.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    served_quantity = Column(Integer, nullable=False, default=0)
    unit_price = Column(Float, nullable=False)
    note = Column(String(255), default="")
    status = Column(Enum(ItemStatus), nullable=False, default=ItemStatus.PENDING)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    dish = relationship("Dish")

    @property
    def pending_quantity(self):
        return max(self.quantity - self.served_quantity, 0)


class Invoice(db.Model):
    __tablename__ = "invoice"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, unique=True)
    cashier_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    subtotal = Column(Float, nullable=False)
    discount = Column(Float, nullable=False, default=0.0)
    vat = Column(Float, nullable=False, default=0.0)
    total_amount = Column(Float, nullable=False)

    cashier = relationship("User", foreign_keys=[cashier_id])


class Notification(db.Model):
    __tablename__ = "notification"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_detail_id = Column(Integer, ForeignKey("order_detail.id"), nullable=True)
    message = Column(String(255), nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)