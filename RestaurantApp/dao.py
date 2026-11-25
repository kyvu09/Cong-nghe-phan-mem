import hashlib
from RestaurantApp import db
from RestaurantApp.models import User


def auth_user(username, password):
    pw = hashlib.md5(password.strip().encode("utf-8")).hexdigest()
    return User.query.filter(
        User.username == username.strip(),
        User.password == pw,
        User.active == True
    ).first()


def get_user_by_id(user_id):
    return db.session.get(User, int(user_id))

from RestaurantApp.models import (
    Category, Dish, DiningTable, TableStatus,
    Order, OrderStatus, OrderDetail, ItemStatus
)


def load_categories():
    return Category.query.order_by(Category.name).all()


def load_dishes(q=None, cate_id=None):
    query = Dish.query.filter(Dish.active == True)
    if q:
        query = query.filter(Dish.name.contains(q.strip()))
    if cate_id:
        query = query.filter(Dish.category_id == int(cate_id))
    return query.order_by(Dish.category_id, Dish.name).all()


def load_tables():
    return DiningTable.query.order_by(DiningTable.table_number).all()


def get_table_by_id(table_id):
    return db.session.get(DiningTable, int(table_id))


def get_open_order_by_table(table_id):
    return Order.query.filter(
        Order.table_id == table_id,
        Order.status == OrderStatus.OPEN
    ).first()


def get_or_create_open_order(table_id, waiter_id):
    order = get_open_order_by_table(table_id)
    if not order:
        table = get_table_by_id(table_id)
        order = Order(table_id=table.id, waiter_id=waiter_id, status=OrderStatus.OPEN)
        table.status = TableStatus.OCCUPIED
        db.session.add(order)
        db.session.flush()
    return order


def add_item_to_table_order(table_id, waiter_id, dish_id, quantity=1, note=""):
    quantity = int(quantity)
    if quantity <= 0:
        return None

    dish = db.session.get(Dish, int(dish_id))
    if not dish or not dish.active:
        return None

    order = get_or_create_open_order(table_id, waiter_id)
    note = (note or "").strip()

    detail = OrderDetail.query.filter(
        OrderDetail.order_id == order.id,
        OrderDetail.dish_id == dish.id
    ).first()

    if detail:

        detail.quantity += quantity
        if note:
            detail.note = f"{detail.note}; {note}" if detail.note else note

        if detail.status == ItemStatus.COMPLETED:
            detail.status = ItemStatus.PENDING
    else:
        detail = OrderDetail(
            order_id=order.id,
            dish_id=dish.id,
            quantity=quantity,
            served_quantity=0,
            unit_price=dish.price,
            note=note,
            status=ItemStatus.PENDING,
        )
        db.session.add(detail)

    db.session.commit()
    return order