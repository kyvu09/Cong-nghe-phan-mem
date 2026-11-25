import hashlib
from RestaurantApp import app, db
from RestaurantApp.models import User, UserRole, Category, Dish, DiningTable


def hash_pw(raw):
    return hashlib.md5(raw.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        if User.query.count() == 0:
            db.session.add_all([
                User(name="Quản trị viên", username="admin", password=hash_pw("123"), role=UserRole.ADMIN),
                User(name="Phục vụ An", username="waiter", password=hash_pw("123"), role=UserRole.WAITER),
                User(name="Đầu bếp Bình", username="kitchen", password=hash_pw("123"), role=UserRole.KITCHEN),
                User(name="Thu ngân Chi", username="cashier", password=hash_pw("123"), role=UserRole.CASHIER),
            ])

        if DiningTable.query.count() == 0:
            db.session.add_all([DiningTable(table_number=f"{i:02d}") for i in range(1, 9)])

        if Category.query.count() == 0:
            c_lau = Category(name="Lẩu")
            c_chinh = Category(name="Món chính")
            c_khaivi = Category(name="Khai vị")
            c_nuoc = Category(name="Đồ uống")
            db.session.add_all([c_lau, c_chinh, c_khaivi, c_nuoc])
            db.session.flush()

            db.session.add_all([
                Dish(code="LAU01", name="Lẩu hải sản", price=250000, category_id=c_lau.id),
                Dish(code="LAU02", name="Lẩu Thái chua cay", price=280000, category_id=c_lau.id),
                Dish(code="MON01", name="Cơm chiên dương châu", price=75000, category_id=c_chinh.id),
                Dish(code="MON02", name="Bò lúc lắc", price=165000, category_id=c_chinh.id),
                Dish(code="KV01", name="Khoai tây chiên", price=45000, category_id=c_khaivi.id),
                Dish(code="NUOC01", name="Nước suối", price=10000, category_id=c_nuoc.id),
                Dish(code="NUOC02", name="Coca-Cola", price=20000, category_id=c_nuoc.id),
            ])

        db.session.commit()