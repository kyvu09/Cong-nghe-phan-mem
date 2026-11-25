# HƯỚNG DẪN LÀM ĐỀ TÀI 10: QUẢN LÝ NHÀ HÀNG GỌI MÓN
*(Phong cách đơn giản giống hệt `SaleApp`: tập trung 100% code Python + HTML Form + Bootstrap 5, không viết file JS, không viết file CSS)*

---

## MỤC LỤC
1. [Bản đồ chuyển đổi từ `SaleApp` sang `RestaurantApp`](#1-bản-đồ-chuyển-đổi-từ-saleapp-sang-restaurantapp)
2. [Bước 0: Chuẩn bị môi trường & Database MySQL](#2-bước-0-chuẩn-bị-môi-trường--database-mysql)
3. [Bước 1: Tạo khung dự án, `models.py`, nạp dữ liệu mẫu & Đăng nhập phân quyền](#3-bước-1-tạo-khung-dự-án-modelspy-nạp-dữ-liệu-mẫu--đăng-nhập-phân-quyền)
4. [Bước 2: Yêu cầu 4 — Quản lý thực đơn (Flask-Admin)](#4-bước-2-yêu-cầu-4--quản-lý-thực-đơn-flask-admin)
5. [Bước 3: Yêu cầu 1 — Nhận đơn hàng tại bàn (Phục vụ)](#5-bước-3-yêu-cầu-1--nhận-đơn-hàng-tại-bàn-phục-vụ)
6. [Bước 4: Yêu cầu 2 — Bếp nhận danh sách chế biến & Thông báo phục vụ](#6-bước-4-yêu-cầu-2--bếp-nhận-danh-sách-chế-biến--thông-báo-phục-vụ)
7. [Bước 5: Yêu cầu 3 — Thanh toán & In hóa đơn (Thu ngân)](#7-bước-5-yêu-cầu-3--thanh-toán--in-hóa-đơn-thu-ngân)
8. [Bước 6: Yêu cầu 5 — Báo cáo doanh thu & Biểu đồ tròn (Quản lý)](#8-bước-6-yêu-cầu-5--báo-cáo-doanh-thu--biểu-đồ-tròn-quản-lý)
9. [Kịch bản Demo & 5 câu hỏi hay gặp khi bảo vệ](#9-kịch-bản-demo--5-câu-hỏi-hay-gặp-khi-bảo-vệ)

---

## 1. Bản đồ chuyển đổi từ `SaleApp` sang `RestaurantApp`

### 1.1. Giữ nguyên kiến trúc 6 file Python của `SaleApp`
Bạn chỉ cần dùng đúng 6 file Python cốt lõi giống hệt bài mẫu `SaleApp`, **không cần thư mục `static/js/` hay `static/css/`**:

| File ở `SaleApp` | File ở `RestaurantApp` | Công việc đảm nhiệm |
| :--- | :--- | :--- |
| `__init__.py` | `RestaurantApp/__init__.py` | Cấu hình Flask, SQLAlchemy (`restaurantdb`), LoginManager, hằng số VAT 10% & giảm 5%. |
| `models.py` | `RestaurantApp/models.py` | 8 bảng CSDL + `Enum` vai trò & trạng thái. |
| `dao.py` | `RestaurantApp/dao.py` | Toàn bộ hàm truy vấn DB cho cả 5 yêu cầu. |
| `utils.py` | `RestaurantApp/utils.py` | Hàm tính tiền hóa đơn (`calculate_bill`) + decorator phân quyền (`role_required`). |
| `admin.py` | `RestaurantApp/admin.py` | **YC 4** (Quản lý thực đơn có kiểm tra quy định) & **YC 5** (Thống kê doanh thu). |
| `index.py` | `RestaurantApp/index.py` | Routes xử lý Form `GET/POST` cho Đăng nhập, **YC 1**, **YC 2**, **YC 3**. |

> **Mẹo làm gọn không cần viết JS / CSS:**
> - **Gọi món (YC 1) & Cập nhật bếp (YC 2):** Dùng `<form method="post">` thuần như trang `login.html` của `SaleApp`, xử lý hoàn toàn trong Python rồi `redirect`.
> - **Thời gian thực cho Bếp & Thông báo (YC 2):** Dùng thẻ HTML chuẩn `<meta http-equiv="refresh" content="5">` — trang tự cập nhật mỗi 5 giây mà **không cần 1 dòng JS nào**.
> - **In hóa đơn đẹp (YC 3):** Dùng class có sẵn `d-print-none` của Bootstrap 5 để tự ẩn menu/nút khi bấm in (`window.print()`), **không cần viết file CSS**.
> - **Biểu đồ tròn (YC 5):** Chỉ dùng đúng ~10 dòng CDN `Chart.js` nhúng trực tiếp trong `admin/stats.html` (y hệt cách học ở môn CNPM) để vẽ biểu đồ tròn theo yêu cầu đề.

### 1.2. Cây thư mục gọn nhẹ trong `BTL_deTai10`

```text
BTL_deTai10/
├── run.py                      # Chạy dự án (thay main.py)
├── init_db.py                  # Chạy 1 lần để tạo bảng & nạp dữ liệu mẫu
├── requirements.txt            # Thư viện y hệt SaleApp
├── huong-dan.md
└── RestaurantApp/
    ├── __init__.py
    ├── models.py
    ├── dao.py
    ├── utils.py
    ├── admin.py
    ├── index.py
    └── templates/
        ├── layout/
        │   ├── base.html
        │   ├── header.html
        │   └── footer.html
        ├── login.html
        ├── waiter/
        │   ├── tables.html     # Sơ đồ bàn (YC 1)
        │   └── order.html      # Gọi món & Phiếu gọi món (YC 1)
        ├── kitchen/
        │   └── index.html      # Danh sách chế biến (YC 2)
        ├── cashier/
        │   ├── index.html      # Danh sách bàn cần thanh toán (YC 3)
        │   └── invoice.html    # Chi tiết & in hóa đơn (YC 3)
        └── admin/
            ├── index.html      # Trang chủ / đăng nhập admin (YC 4)
            └── stats.html      # Báo cáo doanh thu & biểu đồ tròn (YC 5)
```

---

## 2. Bước 0: Chuẩn bị môi trường & Database MySQL

### 2.1. Tạo `requirements.txt` ở thư mục gốc `BTL_deTai10`
```txt
Flask==3.1.3
Flask-Admin==2.2.1
Flask-Login==0.6.3
Flask-SQLAlchemy==3.1.1
PyMySQL==1.2.3
SQLAlchemy==2.1.6
WTForms==3.3.2
```

Mở Terminal trong PyCharm tại `BTL_deTai10` và chạy:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2.2. Tạo database MySQL mới tên `restaurantdb`
Chạy trong MySQL Workbench:
```sql
CREATE DATABASE IF NOT EXISTS restaurantdb
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

### 2.3. Kiểm tra Bước 0
- [ ] Terminal đã kích hoạt `(.venv)` và cài xong thư viện.
- [ ] MySQL đã có database `restaurantdb`.

---

## 3. Bước 1: Tạo khung dự án, `models.py`, nạp dữ liệu mẫu & Đăng nhập phân quyền

> **Mục tiêu Bước 1:** Tạo đủ 8 bảng trong MySQL, nạp sẵn dữ liệu đúng ví dụ đề (*Bàn 05, Lẩu hải sản 250.000đ, Nước suối 10.000đ*) và chạy được đăng nhập phân luồng 4 vai trò.

### 3.1. Tạo `RestaurantApp/__init__.py`

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "restaurant-btl-detai10-secret-key"

# Thay <MAT_KHAU_MYSQL> bằng mật khẩu root MySQL trên máy bạn
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:<MAT_KHAU_MYSQL>@localhost/restaurantdb?charset=utf8mb4"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Các hằng số quy định của đề bài (YC 3)
app.config["VAT_RATE"] = 0.10              # Thuế VAT 10%
app.config["DISCOUNT_THRESHOLD"] = 500000  # Hóa đơn > 500.000 VNĐ được giảm
app.config["DISCOUNT_RATE"] = 0.05         # Giảm 5%

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = "login_my_user"
```

### 3.2. Tạo `RestaurantApp/models.py`

> **Giải thích nhanh 2 điểm quan trọng để trả lời khi bảo vệ:**
> 1. `UniqueConstraint("order_id", "dish_id")` trong `OrderDetail`: chặn trùng món ngay từ CSDL, bắt buộc **cộng dồn số lượng** (YC 1).
> 2. Cột `served_quantity` trong `OrderDetail`: lưu số lượng bếp đã làm xong. Nếu bàn gọi 1 Lẩu (bếp làm xong -> `quantity=1, served_quantity=1`), sau đó gọi thêm 1 Lẩu nữa -> `quantity=2`, Bếp chỉ hiển thị phần cần nấu thêm là `pending_quantity = quantity - served_quantity = 1`.

```python
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
    WAITER = "WAITER"      # Phục vụ
    KITCHEN = "KITCHEN"    # Bếp
    CASHIER = "CASHIER"    # Thu ngân
    ADMIN = "ADMIN"        # Quản trị viên / Quản lý


class TableStatus(PyEnum):
    AVAILABLE = "AVAILABLE"  # Trống
    OCCUPIED = "OCCUPIED"    # Đang có khách


class OrderStatus(PyEnum):
    OPEN = "OPEN"            # Phiếu đang mở
    PAID = "PAID"            # Đã thanh toán


class ItemStatus(PyEnum):
    PENDING = "PENDING"      # Chờ nấu
    COOKING = "COOKING"      # Đang nấu
    COMPLETED = "COMPLETED"  # Hoàn tất


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
    code = Column(String(20), nullable=False, unique=True)  # YC 4: Mã duy nhất
    name = Column(String(150), nullable=False)
    price = Column(Float, nullable=False)                   # YC 4: Giá > 0
    active = Column(Boolean, default=True)                  # Xóa mềm giữ lịch sử HĐ
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)

    def __str__(self):
        return f"[{self.code}] {self.name}"


class DiningTable(db.Model):
    __tablename__ = "dining_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    table_number = Column(String(10), nullable=False, unique=True)  # VD: "01", "05"
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
        UniqueConstraint("order_id", "dish_id", name="uq_order_dish"),  # YC 1: Không trùng món
    )
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    dish_id = Column(Integer, ForeignKey("dish.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    served_quantity = Column(Integer, nullable=False, default=0)
    unit_price = Column(Float, nullable=False)  # Lưu giá tại thời điểm gọi
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
```

### 3.3. Tạo `init_db.py` (ở thư mục gốc `BTL_deTai10`) và chạy tạo bảng

```python
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
        print("Tao bang va du lieu mau thanh cong!")
```

Chạy lệnh:
```powershell
python init_db.py
```

### 3.4. Tạo `RestaurantApp/utils.py`, `dao.py`, `index.py` và `run.py`

1. **`RestaurantApp/utils.py`** (chứa decorator kiểm tra vai trò; Bước 5 sẽ thêm hàm tính tiền vào đây):
```python
from functools import wraps
from flask import redirect, url_for, abort
from flask_login import current_user


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("login_my_user"))
            if current_user.role not in roles:
                return abort(403)
            return f(*args, **kwargs)
        return wrapped
    return decorator
```

2. **`RestaurantApp/dao.py`** (khởi đầu với phần đăng nhập, các bước sau viết nối thêm vào file này):
```python
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
```

3. **`RestaurantApp/index.py`**:
```python
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user
from RestaurantApp import app, db, login, dao
from RestaurantApp.models import UserRole

STATUS_LABELS = {
    "PENDING": "Chờ nấu",
    "COOKING": "Đang nấu",
    "COMPLETED": "Hoàn tất",
}


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.context_processor
def common_attributes():
    return {"status_labels": STATUS_LABELS}


def redirect_by_role(user):
    if user.role == UserRole.ADMIN:
        return redirect("/admin")
    if user.role == UserRole.WAITER:
        return redirect(url_for("waiter_tables"))
    if user.role == UserRole.KITCHEN:
        return redirect(url_for("kitchen_dashboard"))
    if user.role == UserRole.CASHIER:
        return redirect(url_for("cashier_dashboard"))
    return redirect(url_for("login_my_user"))


@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect_by_role(current_user)
    return redirect(url_for("login_my_user"))


@app.route("/login", methods=["GET", "POST"])
def login_my_user():
    if current_user.is_authenticated:
        return redirect_by_role(current_user)

    err_msg = None
    if request.method == "POST":
        u = dao.auth_user(
            username=request.form.get("username", ""),
            password=request.form.get("password", ""),
        )
        if u:
            login_user(u)
            return redirect_by_role(u)
        err_msg = "Tài khoản hoặc mật khẩu chưa đúng!"

    return render_template("login.html", err_msg=err_msg)


@app.route("/logout")
def logout_my_user():
    logout_user()
    return redirect(url_for("login_my_user"))


# 3 route tạm cho Bước 1 (sẽ thay thế ở Bước 3, 4, 5)
@app.route("/waiter")
def waiter_tables():
    return "Trang Phục vụ - <a href='/logout'>Đăng xuất</a>"


@app.route("/kitchen")
def kitchen_dashboard():
    return "Trang Bếp - <a href='/logout'>Đăng xuất</a>"


@app.route("/cashier")
def cashier_dashboard():
    return "Trang Thu ngân - <a href='/logout'>Đăng xuất</a>"
```

4. **`run.py`** (ở thư mục gốc `BTL_deTai10`):
```python
from RestaurantApp import app
import RestaurantApp.index
# import RestaurantApp.admin  # Bỏ comment ở Bước 2 sau khi tạo admin.py

if __name__ == "__main__":
    app.run(debug=True)
```

### 3.5. Tạo giao diện nền (chỉ Bootstrap 5 giống `SaleApp`)

1. **`RestaurantApp/templates/layout/base.html`**:
```html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Quản lý nhà hàng{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"></script>
    {% block head %}{% endblock %}
</head>
<body>
<div class="d-print-none">
    {% include 'layout/header.html' %}
</div>

<div class="container mt-3 mb-5">
    {% block content %}{% endblock %}
</div>

<div class="d-print-none">
    {% include 'layout/footer.html' %}
</div>
</body>
</html>
```

2. **`RestaurantApp/templates/layout/header.html`**:
```html
<nav class="navbar navbar-expand-sm navbar-dark bg-dark">
    <div class="container-fluid">
        <a class="navbar-brand" href="/">NHÀ HÀNG GỌI MÓN</a>
        <div class="collapse navbar-collapse">
            <ul class="navbar-nav me-auto">
                {% if current_user.is_authenticated %}
                    {% if current_user.role.value in ['WAITER', 'ADMIN'] %}
                    <li class="nav-item"><a class="nav-link" href="/waiter">Phục vụ</a></li>
                    {% endif %}
                    {% if current_user.role.value in ['KITCHEN', 'ADMIN'] %}
                    <li class="nav-item"><a class="nav-link" href="/kitchen">Bếp</a></li>
                    {% endif %}
                    {% if current_user.role.value in ['CASHIER', 'ADMIN'] %}
                    <li class="nav-item"><a class="nav-link" href="/cashier">Thu ngân</a></li>
                    {% endif %}
                    {% if current_user.role.value == 'ADMIN' %}
                    <li class="nav-item"><a class="nav-link" href="/admin">Quản trị</a></li>
                    {% endif %}
                {% endif %}
            </ul>
            <ul class="navbar-nav">
                {% if current_user.is_authenticated %}
                <li class="nav-item">
                    <span class="nav-link text-warning">Chào {{ current_user.name }}</span>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/logout">Đăng xuất</a>
                </li>
                {% else %}
                <li class="nav-item">
                    <a class="nav-link" href="/login">Đăng nhập</a>
                </li>
                {% endif %}
            </ul>
        </div>
    </div>
</nav>
```

3. **`RestaurantApp/templates/layout/footer.html`**:
```html
<footer class="bg-light text-center py-3 mt-4 border-top">
    <small class="text-muted">Đề tài 10 - Quản lý nhà hàng gọi món</small>
</footer>
```

4. **`RestaurantApp/templates/login.html`** (giống y hệt `SaleApp/templates/login.html`):
```html
{% extends 'layout/base.html' %}
{% block title %}Đăng nhập{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-5">
        <h3 class="text-info text-center mt-3">ĐĂNG NHẬP HỆ THỐNG</h3>
        {% if err_msg %}
        <div class="alert alert-danger">{{ err_msg }}</div>
        {% endif %}
        <form method="post">
            <div class="mb-3">
                <label class="form-label">Tài khoản</label>
                <input type="text" class="form-control" name="username" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Mật khẩu</label>
                <input type="password" class="form-control" name="password" required>
            </div>
            <button class="btn btn-primary w-100" type="submit">Đăng nhập</button>
        </form>
    </div>
</div>
{% endblock %}
```

### 3.6. Checklist kiểm tra Bước 1
- [ ] `python init_db.py` tạo đủ 8 bảng trong MySQL `restaurantdb`.
- [ ] `python run.py` mở `http://127.0.0.1:5000/login` không lỗi.
- [ ] Thử đăng nhập `waiter / 123`, `kitchen / 123`, `cashier / 123` -> tự chuyển đúng trang theo vai trò.

---

## 4. Bước 2: Yêu cầu 4 — Quản lý thực đơn (Flask-Admin)

> **Mục tiêu Bước 2:** Quản trị viên thêm/sửa/xóa món ăn trên `/admin` đúng 2 quy định: **mã duy nhất**, **giá > 0 và thuộc nhóm món hợp lệ**.

### 4.1. Tạo `RestaurantApp/admin.py`

```python
from flask import redirect, flash, request
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from flask_login import current_user, logout_user
from wtforms.validators import DataRequired, NumberRange, ValidationError

from RestaurantApp import app, db
from RestaurantApp.models import Category, Dish, DiningTable, OrderDetail, UserRole


class AdminOnlyView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.ADMIN

    def inaccessible_callback(self, name, **kwargs):
        return redirect("/admin")


class MyCategoryView(AdminOnlyView):
    column_list = ["id", "name"]
    column_labels = {"id": "ID", "name": "Nhóm món"}
    column_searchable_list = ["name"]
    form_columns = ["name"]


class MyDishView(AdminOnlyView):
    column_list = ["code", "name", "price", "category", "active"]
    column_labels = {
        "code": "Mã món",
        "name": "Tên món ăn",
        "price": "Đơn giá (VNĐ)",
        "category": "Nhóm món",
        "active": "Đang bán",
    }
    column_searchable_list = ["code", "name"]
    column_filters = ["category", "price", "active"]
    form_columns = ["code", "name", "price", "category", "active"]

    # Ràng buộc quy định YC 4 ngay trên Form
    form_args = {
        "code": {"validators": [DataRequired(message="Mã món không được để trống!")]},
        "name": {"validators": [DataRequired(message="Tên món không được để trống!")]},
        "price": {
            "validators": [
                DataRequired(message="Vui lòng nhập giá!"),
                NumberRange(min=1, message="Giá món phải lớn hơn 0!"),
            ]
        },
        "category": {"validators": [DataRequired(message="Vui lòng chọn nhóm món hợp lệ!")]},
    }

    def on_model_change(self, form, model, is_created):
        model.code = model.code.strip().upper()

        # Kiểm tra mã món duy nhất (YC 4)
        existed = Dish.query.filter(Dish.code == model.code).first()
        if existed and (is_created or existed.id != model.id):
            raise ValidationError(f"Mã món '{model.code}' đã tồn tại!")

        # Kiểm tra giá > 0 và nhóm món hợp lệ (YC 4)
        if model.price is None or model.price <= 0:
            raise ValidationError("Giá món phải lớn hơn 0 VNĐ!")
        if not model.category:
            raise ValidationError("Món ăn phải thuộc nhóm món hợp lệ!")

    def delete_model(self, model):
        # Xóa mềm nếu món đã nằm trong hóa đơn cũ để tránh lỗi khóa ngoại
        if OrderDetail.query.filter_by(dish_id=model.id).first():
            model.active = False
            self.session.commit()
            flash("Món đã từng được gọi nên chuyển sang 'Ngừng bán' thay vì xóa cứng.", "warning")
            return True
        return super().delete_model(model)


class MyTableView(AdminOnlyView):
    column_list = ["id", "table_number", "status"]
    column_labels = {"id": "ID", "table_number": "Số bàn", "status": "Trạng thái"}
    form_columns = ["table_number", "status"]


class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render("admin/index.html")


class MyStatView(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/stats.html")

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.ADMIN


class MyLogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")

    def is_accessible(self):
        return current_user.is_authenticated


admin = Admin(app=app, name="QUẢN LÝ NHÀ HÀNG", theme=Bootstrap4Theme(), index_view=MyAdminIndexView())
admin.add_view(MyCategoryView(Category, db.session, name="Nhóm món"))
admin.add_view(MyDishView(Dish, db.session, name="Thực đơn"))
admin.add_view(MyTableView(DiningTable, db.session, name="Bàn ăn"))
admin.add_view(MyStatView(name="Báo cáo doanh thu", endpoint="stats"))
admin.add_view(MyLogoutView(name="Đăng xuất", endpoint="admin_logout"))
```

### 4.2. Thêm `/login-admin` trong `RestaurantApp/index.py` & bật `admin` trong `run.py`

Thêm vào `RestaurantApp/index.py`:
```python
@app.route("/login-admin", methods=["POST"])
def admin_login_process():
    u = dao.auth_user(
        username=request.form.get("username", ""),
        password=request.form.get("password", ""),
    )
    if u and u.role == UserRole.ADMIN:
        login_user(u)
        return redirect("/admin")
    return render_template("admin/index.html", err_msg="Tài khoản không đúng hoặc không có quyền quản trị!")
```

Mở comment `import RestaurantApp.admin` trong `run.py`.

Tạo **`RestaurantApp/templates/admin/index.html`** (giống `SaleApp/templates/admin/index.html`, thêm kiểm tra đúng quyền `ADMIN`):
```html
{% extends 'admin/master.html' %}
{% block body %}
{% if current_user.is_authenticated and current_user.role.value == 'ADMIN' %}
    <h3 class="text-info text-center mt-3">CHÀO MỪNG QUẢN TRỊ VIÊN</h3>
    <p class="text-center">Chọn các mục trên thanh menu để quản lý Thực đơn, Nhóm món, Bàn ăn và Báo cáo doanh thu.</p>
{% else %}
    <h3 class="text-info text-center mt-3">ĐĂNG NHẬP QUẢN TRỊ</h3>
    {% if err_msg %}
    <div class="alert alert-danger">{{ err_msg }}</div>
    {% endif %}
    <form method="post" action="/login-admin">
        <div class="form-group mb-3">
            <label>Tài khoản</label>
            <input type="text" class="form-control" name="username" required>
        </div>
        <div class="form-group mb-3">
            <label>Mật khẩu</label>
            <input type="password" class="form-control" name="password" required>
        </div>
        <button class="btn btn-primary" type="submit">Đăng nhập</button>
    </form>
{% endif %}
{% endblock %}
```

Tạo tạm **`RestaurantApp/templates/admin/stats.html`** (sẽ hoàn thiện ở Bước 6):
```html
{% extends 'admin/master.html' %}
{% block body %}
<h3 class="text-info text-center">BÁO CÁO DOANH THU (Sẽ làm ở Bước 6)</h3>
{% endblock %}
```

### 4.3. Checklist kiểm tra Bước 2
- [ ] Đăng nhập `admin / 123` vào `/admin` -> thấy menu Nhóm món, Thực đơn, Bàn ăn, Báo cáo doanh thu.
- [ ] Thêm món trùng mã `LAU01` -> báo lỗi `"Mã món 'LAU01' đã tồn tại!"`.
- [ ] Thêm món giá `0` hoặc `-10000` -> báo lỗi `"Giá món phải lớn hơn 0!"`.
- [ ] Thêm 1 món hợp lệ, sửa giá, xóa món -> hoạt động trơn tru.

---

## 5. Bước 3: Yêu cầu 1 — Nhận đơn hàng tại bàn (Phục vụ)

> **Mục tiêu Bước 3:** Phục vụ chọn bàn và gửi Form gọi món (100% Python, không JS). Đảm bảo: **mỗi bàn chỉ 1 phiếu mở** và **không ghi trùng món, cộng dồn số lượng**.

### 5.1. Thêm các hàm gọi món vào `RestaurantApp/dao.py`

```python
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
    """Quy định YC 1: Mỗi bàn chỉ có 1 phiếu mở cùng lúc."""
    order = get_open_order_by_table(table_id)
    if not order:
        table = get_table_by_id(table_id)
        order = Order(table_id=table.id, waiter_id=waiter_id, status=OrderStatus.OPEN)
        table.status = TableStatus.OCCUPIED
        db.session.add(order)
        db.session.flush()
    return order


def add_item_to_table_order(table_id, waiter_id, dish_id, quantity=1, note=""):
    """Quy định YC 1: Không ghi trùng món, cộng dồn số lượng."""
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
        # Đã có món trong phiếu -> CỘNG DỒN số lượng
        detail.quantity += quantity
        if note:
            detail.note = f"{detail.note}; {note}" if detail.note else note
        # Nếu đợt cũ bếp làm xong rồi -> chuyển lại PENDING để bếp làm phần gọi thêm
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
```

### 5.2. Cập nhật Routes Phục vụ trong `RestaurantApp/index.py`

Import thêm `from RestaurantApp.utils import role_required` và thay route tạm `/waiter` bằng:

```python
@app.route("/waiter")
@role_required(UserRole.WAITER, UserRole.ADMIN)
def waiter_tables():
    return render_template("waiter/tables.html", tables=dao.load_tables())


@app.route("/waiter/table/<int:table_id>")
@role_required(UserRole.WAITER, UserRole.ADMIN)
def waiter_order_page(table_id):
    table = dao.get_table_by_id(table_id)
    if not table:
        return redirect(url_for("waiter_tables"))

    q = request.args.get("q")
    cate_id = request.args.get("cate_id")
    order = dao.get_open_order_by_table(table_id)
    return render_template(
        "waiter/order.html",
        table=table,
        order=order,
        categories=dao.load_categories(),
        dishes=dao.load_dishes(q=q, cate_id=cate_id),
    )


@app.route("/waiter/table/<int:table_id>/add", methods=["POST"])
@role_required(UserRole.WAITER, UserRole.ADMIN)
def waiter_add_item(table_id):
    dish_id = request.form.get("dish_id")
    quantity = request.form.get("quantity", 1)
    note = request.form.get("note", "")
    dao.add_item_to_table_order(
        table_id=table_id,
        waiter_id=current_user.id,
        dish_id=dish_id,
        quantity=quantity,
        note=note,
    )
    return redirect(url_for("waiter_order_page", table_id=table_id))
```

### 5.3. Tạo 2 template Bootstrap 5 cho Phục vụ

1. **`RestaurantApp/templates/waiter/tables.html`**:
```html
{% extends 'layout/base.html' %}
{% block title %}Sơ đồ bàn{% endblock %}

{% block head %}
<!-- Tự cập nhật mỗi 5 giây để nhận thông báo bếp xong (không cần JS) -->
<meta http-equiv="refresh" content="5">
{% endblock %}

{% block content %}
<h3 class="text-info text-center mb-3">SƠ ĐỒ BÀN - PHỤC VỤ</h3>

{% if unread_notis %}
    {% for n in unread_notis %}
    <div class="alert alert-success d-flex justify-content-between align-items-center">
        <span><strong>Thông báo từ Bếp:</strong> {{ n.message }} ({{ n.created_at.strftime('%H:%M:%S') }})</span>
        <form method="post" action="/notifications/{{ n.id }}/read" class="m-0">
            <button type="submit" class="btn btn-sm btn-outline-success">Đã nhận món</button>
        </form>
    </div>
    {% endfor %}
{% endif %}

<div class="row">
    {% for t in tables %}
    <div class="col-md-3 col-6 mb-3">
        <div class="card text-center {% if t.status.value == 'OCCUPIED' %}border-danger{% else %}border-success{% endif %}">
            <div class="card-body">
                <h4 class="card-title">Bàn {{ t.table_number }}</h4>
                {% if t.status.value == 'OCCUPIED' %}
                    <p><span class="badge bg-danger">Đang có khách</span></p>
                {% else %}
                    <p><span class="badge bg-success">Trống</span></p>
                {% endif %}
                <a href="/waiter/table/{{ t.id }}" class="btn btn-primary btn-sm">Gọi món / Xem phiếu</a>
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% endblock %}
```

2. **`RestaurantApp/templates/waiter/order.html`**:
```html
{% extends 'layout/base.html' %}
{% block title %}Gọi món - Bàn {{ table.table_number }}{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
    <h3 class="text-info m-0">PHIẾU GỌI MÓN - BÀN {{ table.table_number }}</h3>
    <a href="/waiter" class="btn btn-secondary btn-sm">Quay lại sơ đồ bàn</a>
</div>

<div class="row">
    <!-- Cột trái: Thực đơn -->
    <div class="col-md-7">
        <div class="mb-2">
            <a href="/waiter/table/{{ table.id }}" class="btn btn-sm btn-outline-dark">Tất cả</a>
            {% for c in categories %}
            <a href="/waiter/table/{{ table.id }}?cate_id={{ c.id }}" class="btn btn-sm btn-outline-primary">{{ c.name }}</a>
            {% endfor %}
        </div>

        <form method="get" class="d-flex mb-3">
            <input type="text" name="q" class="form-control me-2" placeholder="Tìm tên món...">
            <button class="btn btn-primary" type="submit">Tìm</button>
        </form>

        <table class="table table-bordered align-middle">
            <thead class="table-light">
                <tr>
                    <th>Mã</th>
                    <th>Tên món</th>
                    <th>Giá</th>
                    <th style="width: 260px;">Gọi món</th>
                </tr>
            </thead>
            <tbody>
                {% for d in dishes %}
                <tr>
                    <td>{{ d.code }}</td>
                    <td>{{ d.name }}</td>
                    <td>{{ "{:,.0f}".format(d.price) }} đ</td>
                    <td>
                        <form method="post" action="/waiter/table/{{ table.id }}/add" class="d-flex gap-1">
                            <input type="hidden" name="dish_id" value="{{ d.id }}">
                            <input type="number" name="quantity" value="1" min="1" class="form-control form-control-sm" style="width: 60px;">
                            <input type="text" name="note" placeholder="Ghi chú" class="form-control form-control-sm">
                            <button type="submit" class="btn btn-success btn-sm">Thêm</button>
                        </form>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <!-- Cột phải: Biểu mẫu Phiếu gọi món đúng đề bài -->
    <div class="col-md-5">
        <div class="card">
            <div class="card-header bg-dark text-white">Phiếu gọi món hiện tại</div>
            <div class="card-body p-2">
                {% if order and order.details %}
                <table class="table table-sm table-bordered mb-0">
                    <thead>
                        <tr>
                            <th>STT</th>
                            <th>Bàn số</th>
                            <th>Món ăn</th>
                            <th>Số lượng</th>
                            <th>Trạng thái</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for item in order.details %}
                        <tr>
                            <td>{{ loop.index }}</td>
                            <td>{{ table.table_number }}</td>
                            <td>
                                {{ item.dish.name }}
                                {% if item.note %}<br><small class="text-muted">({{ item.note }})</small>{% endif %}
                            </td>
                            <td>{{ item.quantity }}</td>
                            <td><span class="badge bg-info text-dark">{{ status_labels[item.status.value] }}</span></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
                {% else %}
                <p class="text-muted text-center my-3">Bàn chưa gọi món nào.</p>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 5.4. Checklist kiểm tra Bước 3
- [ ] Đăng nhập `waiter / 123`, chọn **Bàn 05**.
- [ ] Gọi 1 **Lẩu hải sản** (ghi chú `"Ít cay"`), gọi 1 **Nước suối**, rồi gọi thêm 1 **Nước suối** nữa.
- [ ] Trên Phiếu gọi món hiện đúng: dòng 1 `05 | Lẩu hải sản | 1`, dòng 2 `05 | Nước suối | 2` (cộng dồn, không bị trùng).
- [ ] Quay lại `/waiter` thấy Bàn 05 chuyển màu đỏ (`Đang có khách`), bấm vào vẫn mở đúng 1 phiếu cũ.

---

## 6. Bước 4: Yêu cầu 2 — Bếp nhận danh sách chế biến & Thông báo phục vụ

> **Mục tiêu Bước 4:** Bếp chỉ thấy đơn chưa hoàn tất, tự cập nhật mỗi 5 giây (nhờ `<meta http-equiv="refresh" content="5">`). Khi bấm **Hoàn tất**, món ẩn khỏi Bếp và bật thông báo bên màn hình Phục vụ.

### 6.1. Thêm hàm Bếp & Thông báo vào `RestaurantApp/dao.py`

```python
from RestaurantApp.models import Notification


def get_pending_kitchen_items():
    """Quy định YC 2: Bếp chỉ thấy đơn chưa hoàn tất của các phiếu đang mở."""
    items = (
        OrderDetail.query.join(Order)
        .filter(
            Order.status == OrderStatus.OPEN,
            OrderDetail.status != ItemStatus.COMPLETED,
        )
        .order_by(OrderDetail.updated_at.asc())
        .all()
    )
    return [d for d in items if d.pending_quantity > 0]


def update_kitchen_item_status(detail_id, new_status_str):
    detail = db.session.get(OrderDetail, int(detail_id))
    if not detail:
        return None

    new_status = ItemStatus[new_status_str]
    detail.status = new_status

    # Quy định YC 2: Khi bếp xác nhận xong -> tạo thông báo cho phục vụ
    if new_status == ItemStatus.COMPLETED:
        cooked = detail.pending_quantity or detail.quantity
        detail.served_quantity = detail.quantity
        msg = f"Bàn {detail.order.table.table_number} - {detail.dish.name} (x{cooked}) đã chế biến xong!"
        db.session.add(Notification(order_detail_id=detail.id, message=msg))

    db.session.commit()
    return detail


def get_unread_notifications():
    return Notification.query.filter_by(is_read=False).order_by(Notification.created_at.desc()).all()


def mark_notification_read(noti_id):
    noti = db.session.get(Notification, int(noti_id))
    if noti:
        noti.is_read = True
        db.session.commit()
```

### 6.2. Cập nhật `RestaurantApp/index.py`

1. Sửa `common_attributes()` để Phục vụ luôn nhận được thông báo chưa đọc:
```python
@app.context_processor
def common_attributes():
    notis = []
    if current_user.is_authenticated and current_user.role in (UserRole.WAITER, UserRole.ADMIN):
        notis = dao.get_unread_notifications()
    return {
        "status_labels": STATUS_LABELS,
        "unread_notis": notis,
    }
```

2. Thay route tạm `/kitchen` và thêm route xử lý Form cập nhật trạng thái + xác nhận thông báo:
```python
@app.route("/kitchen")
@role_required(UserRole.KITCHEN, UserRole.ADMIN)
def kitchen_dashboard():
    items = dao.get_pending_kitchen_items()
    return render_template("kitchen/index.html", items=items)


@app.route("/kitchen/update/<int:detail_id>", methods=["POST"])
@role_required(UserRole.KITCHEN, UserRole.ADMIN)
def kitchen_update_status(detail_id):
    new_status = request.form.get("status")
    if new_status in ("COOKING", "COMPLETED"):
        dao.update_kitchen_item_status(detail_id, new_status)
    return redirect(url_for("kitchen_dashboard"))


@app.route("/notifications/<int:noti_id>/read", methods=["POST"])
@role_required(UserRole.WAITER, UserRole.ADMIN)
def read_notification(noti_id):
    dao.mark_notification_read(noti_id)
    return redirect(request.referrer or url_for("waiter_tables"))
```

### 6.3. Tạo `RestaurantApp/templates/kitchen/index.html`

```html
{% extends 'layout/base.html' %}
{% block title %}Bếp - Danh sách chế biến{% endblock %}

{% block head %}
<!-- Tự làm mới mỗi 5 giây để nhận đơn thời gian thực (không cần JS) -->
<meta http-equiv="refresh" content="5">
{% endblock %}

{% block content %}
<h3 class="text-info text-center mb-3">DANH SÁCH MÓN CHẾ BIẾN (BẾP)</h3>

{% if items %}
<table class="table table-bordered table-striped align-middle">
    <thead class="table-dark">
        <tr>
            <th>STT</th>
            <th>Bàn số</th>
            <th>Món ăn</th>
            <th>Số lượng</th>
            <th>Trạng thái</th>
            <th>Ghi chú</th>
            <th>Thao tác</th>
        </tr>
    </thead>
    <tbody>
        {% for item in items %}
        <tr>
            <td>{{ loop.index }}</td>
            <td><strong>{{ item.order.table.table_number }}</strong></td>
            <td>{{ item.dish.name }}</td>
            <td>{{ item.pending_quantity }}</td>
            <td>
                {% if item.status.value == 'COOKING' %}
                    <span class="badge bg-warning text-dark">Đang nấu</span>
                {% else %}
                    <span class="badge bg-secondary">Chờ nấu</span>
                {% endif %}
            </td>
            <td>{{ item.note or '' }}</td>
            <td>
                <form method="post" action="/kitchen/update/{{ item.id }}" class="m-0">
                    {% if item.status.value == 'PENDING' %}
                        <input type="hidden" name="status" value="COOKING">
                        <button type="submit" class="btn btn-warning btn-sm">Bắt đầu nấu</button>
                    {% else %}
                        <input type="hidden" name="status" value="COMPLETED">
                        <button type="submit" class="btn btn-success btn-sm">Hoàn tất</button>
                    {% endif %}
                </form>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% else %}
<div class="alert alert-info text-center">Hiện không có món nào cần chế biến.</div>
{% endif %}
{% endblock %}
```

### 6.4. Checklist kiểm tra Bước 4
- [ ] Mở 2 cửa sổ trình duyệt song song: cửa sổ 1 đăng nhập `waiter`, cửa sổ 2 (ẩn danh) đăng nhập `kitchen`.
- [ ] Bên `waiter` gọi món -> đợi tối đa 5 giây (không bấm F5), bên `kitchen` tự hiện món đó kèm ghi chú.
- [ ] Bên `kitchen` bấm **Bắt đầu nấu** -> đổi sang `Đang nấu`; bấm **Hoàn tất** -> biến mất khỏi bảng Bếp.
- [ ] Bên `waiter` (trang `/waiter`) tự hiện hộp xanh lá `"Thông báo từ Bếp: Bàn 05 - Lẩu hải sản (x1) đã chế biến xong!"` -> bấm **Đã nhận món** để ẩn.

---

## 7. Bước 5: Yêu cầu 3 — Thanh toán & In hóa đơn (Thu ngân)

> **Mục tiêu Bước 5:** Tổng hợp hóa đơn đúng biểu mẫu, tính **giảm 5% nếu > 500.000 VNĐ** + **VAT 10%**, lưu `Invoice`, giải phóng bàn về `Trống`, và in hóa đơn gọn bằng Bootstrap `d-print-none`.

### 7.1. Thêm hàm tính tiền vào `RestaurantApp/utils.py`

```python
from RestaurantApp import app


def calculate_bill(details):
    subtotal = sum(d.quantity * d.unit_price for d in details)

    discount_rate = app.config["DISCOUNT_RATE"]
    discount_threshold = app.config["DISCOUNT_THRESHOLD"]
    vat_rate = app.config["VAT_RATE"]

    discount = round(subtotal * discount_rate) if subtotal > discount_threshold else 0
    vat = round((subtotal - discount) * vat_rate)
    total_amount = round(subtotal - discount + vat)

    return {
        "subtotal": subtotal,
        "discount": discount,
        "vat": vat,
        "total_amount": total_amount,
    }
```

### 7.2. Thêm hàm thanh toán vào `RestaurantApp/dao.py`

```python
from RestaurantApp.models import Invoice
from RestaurantApp import utils


def load_open_orders():
    return Order.query.filter_by(status=OrderStatus.OPEN).order_by(Order.created_at.asc()).all()


def load_recent_invoices(limit=10):
    return Invoice.query.order_by(Invoice.created_at.desc()).limit(limit).all()


def get_order_by_id(order_id):
    return db.session.get(Order, int(order_id))


def pay_order(order_id, cashier_id):
    order = get_order_by_id(order_id)
    if not order or not order.details:
        return None
    if order.status == OrderStatus.PAID:
        return order.invoice

    bill = utils.calculate_bill(order.details)
    invoice = Invoice(
        order_id=order.id,
        cashier_id=cashier_id,
        subtotal=bill["subtotal"],
        discount=bill["discount"],
        vat=bill["vat"],
        total_amount=bill["total_amount"],
    )
    order.status = OrderStatus.PAID
    order.table.status = TableStatus.AVAILABLE  # Trả bàn về trạng thái Trống

    db.session.add(invoice)
    db.session.commit()
    return invoice
```

### 7.3. Cập nhật Routes Thu ngân trong `RestaurantApp/index.py`

Import thêm `from RestaurantApp import utils` và thay route tạm `/cashier` bằng:

```python
@app.route("/cashier")
@role_required(UserRole.CASHIER, UserRole.ADMIN)
def cashier_dashboard():
    return render_template(
        "cashier/index.html",
        open_orders=dao.load_open_orders(),
        recent_invoices=dao.load_recent_invoices(10),
    )


@app.route("/cashier/order/<int:order_id>", methods=["GET", "POST"])
@role_required(UserRole.CASHIER, UserRole.ADMIN)
def cashier_checkout(order_id):
    order = dao.get_order_by_id(order_id)
    if not order:
        return redirect(url_for("cashier_dashboard"))

    if request.method == "POST":
        dao.pay_order(order.id, current_user.id)
        return redirect(url_for("cashier_checkout", order_id=order.id))

    bill = utils.calculate_bill(order.details)
    return render_template("cashier/invoice.html", order=order, bill=bill)
```

### 7.4. Tạo 2 template Bootstrap 5 cho Thu ngân

1. **`RestaurantApp/templates/cashier/index.html`**:
```html
{% extends 'layout/base.html' %}
{% block title %}Thu ngân - Thanh toán{% endblock %}
{% block content %}
<h3 class="text-info text-center mb-3">QUẦY THU NGÂN</h3>

<h5>Các bàn đang chờ thanh toán</h5>
{% if open_orders %}
<table class="table table-bordered mb-4">
    <thead class="table-light">
        <tr>
            <th>Mã phiếu</th>
            <th>Bàn số</th>
            <th>Giờ mở</th>
            <th>Phục vụ</th>
            <th>Thao tác</th>
        </tr>
    </thead>
    <tbody>
        {% for o in open_orders %}
        <tr>
            <td>#{{ o.id }}</td>
            <td><strong>Bàn {{ o.table.table_number }}</strong></td>
            <td>{{ o.created_at.strftime('%H:%M %d/%m/%Y') }}</td>
            <td>{{ o.waiter.name }}</td>
            <td><a href="/cashier/order/{{ o.id }}" class="btn btn-success btn-sm">Xem &amp; Thanh toán</a></td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% else %}
<div class="alert alert-secondary">Hiện không có bàn nào đang mở.</div>
{% endif %}

<h5>Hóa đơn đã thanh toán gần đây</h5>
<table class="table table-sm table-striped">
    <thead>
        <tr>
            <th>Mã HĐ</th>
            <th>Bàn</th>
            <th>Thời gian</th>
            <th>Tổng thanh toán</th>
            <th></th>
        </tr>
    </thead>
    <tbody>
        {% for inv in recent_invoices %}
        <tr>
            <td>#{{ inv.id }}</td>
            <td>Bàn {{ inv.order.table.table_number }}</td>
            <td>{{ inv.created_at.strftime('%H:%M %d/%m/%Y') }}</td>
            <td><strong>{{ "{:,.0f}".format(inv.total_amount) }} VNĐ</strong></td>
            <td><a href="/cashier/order/{{ inv.order_id }}" class="btn btn-outline-primary btn-sm">Xem / In</a></td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
```

2. **`RestaurantApp/templates/cashier/invoice.html`**:
```html
{% extends 'layout/base.html' %}
{% block title %}Hóa đơn thanh toán{% endblock %}
{% block content %}
<div class="card mx-auto" style="max-width: 700px;">
    <div class="card-body">
        <h3 class="text-center">HÓA ĐƠN THANH TOÁN</h3>
        <p class="text-center text-muted mb-3">
            Bàn số: <strong>{{ order.table.table_number }}</strong> |
            Ngày: {{ (order.invoice.created_at if order.invoice else order.created_at).strftime('%d/%m/%Y %H:%M') }}
        </p>

        <table class="table table-bordered">
            <thead class="table-light">
                <tr>
                    <th>Món ăn</th>
                    <th>Số lượng</th>
                    <th>Đơn giá</th>
                    <th>Thành tiền</th>
                </tr>
            </thead>
            <tbody>
                {% for d in order.details %}
                <tr>
                    <td>{{ d.dish.name }}</td>
                    <td>{{ d.quantity }}</td>
                    <td>{{ "{:,.0f}".format(d.unit_price) }}</td>
                    <td>{{ "{:,.0f}".format(d.quantity * d.unit_price) }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <div class="text-end">
            <p class="mb-1">Tổng cộng món: <strong>{{ "{:,.0f}".format(bill.subtotal) }} VNĐ</strong></p>
            <p class="mb-1">Giảm giá (5% nếu &gt; 500.000đ): <strong>- {{ "{:,.0f}".format(bill.discount) }} VNĐ</strong></p>
            <p class="mb-1">Thuế VAT (10%): <strong>+ {{ "{:,.0f}".format(bill.vat) }} VNĐ</strong></p>
            <h4 class="text-danger mt-2">Thành tiền phải trả: {{ "{:,.0f}".format(bill.total_amount) }} VNĐ</h4>
        </div>

        <div class="mt-4 d-flex justify-content-between d-print-none">
            <a href="/cashier" class="btn btn-secondary">Quay lại</a>
            <div>
                {% if order.status.value == 'OPEN' %}
                <form method="post" class="d-inline">
                    <button type="submit" class="btn btn-success">Xác nhận thanh toán</button>
                </form>
                {% else %}
                <span class="badge bg-success me-2">ĐÃ THANH TOÁN</span>
                <button type="button" class="btn btn-primary" onclick="window.print()">In hóa đơn</button>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 7.5. Checklist kiểm tra Bước 5
- [ ] **Case 1 (giống đề bài):** 1 Lẩu hải sản (250k) + 2 Nước suối (20k) -> Tạm tính `270.000`, Giảm `0`, VAT `27.000`, Phải trả `297.000 VNĐ`.
- [ ] **Case 2 (> 500.000đ):** 2 Lẩu Thái (560k) + 2 Coca (40k) -> Tạm tính `600.000`, Giảm 5% = `30.000`, VAT 10% = `57.000`, Phải trả `627.000 VNĐ`.
- [ ] Bấm **Xác nhận thanh toán** -> Bàn quay về màu xanh (`Trống`) bên Phục vụ.
- [ ] Bấm **In hóa đơn** -> menu và nút bấm tự ẩn gọn gàng (nhờ `d-print-none` của Bootstrap 5).

---

## 8. Bước 6: Yêu cầu 5 — Báo cáo doanh thu & Biểu đồ tròn (Quản lý)

> **Mục tiêu Bước 6:** Lọc doanh thu & top món bán chạy theo **ngày** hoặc **tháng**, vẽ **biểu đồ tròn** tỉ lệ món trong `/admin/stats`.

### 8.1. Thêm hàm thống kê vào `RestaurantApp/dao.py`

```python
from datetime import date
from sqlalchemy import func, extract


def get_revenue_stats(mode="day", date_str=None, month_str=None):
    today = date.today()

    inv_query = db.session.query(
        func.coalesce(func.sum(Invoice.total_amount), 0),
        func.count(Invoice.id),
    )

    dish_query = (
        db.session.query(
            Dish.code,
            Dish.name,
            func.sum(OrderDetail.quantity).label("total_qty"),
            func.sum(OrderDetail.quantity * OrderDetail.unit_price).label("total_rev"),
        )
        .join(OrderDetail, OrderDetail.dish_id == Dish.id)
        .join(Order, Order.id == OrderDetail.order_id)
        .join(Invoice, Invoice.order_id == Order.id)
    )

    if mode == "month":
        year, month = map(int, month_str.split("-")) if month_str else (today.year, today.month)
        inv_query = inv_query.filter(
            extract("year", Invoice.created_at) == year,
            extract("month", Invoice.created_at) == month,
        )
        dish_query = dish_query.filter(
            extract("year", Invoice.created_at) == year,
            extract("month", Invoice.created_at) == month,
        )
    else:
        target = date_str or today.isoformat()
        inv_query = inv_query.filter(func.date(Invoice.created_at) == target)
        dish_query = dish_query.filter(func.date(Invoice.created_at) == target)

    total_revenue, total_invoices = inv_query.first()
    top_dishes = (
        dish_query.group_by(Dish.id, Dish.code, Dish.name)
        .order_by(func.sum(OrderDetail.quantity).desc())
        .all()
    )

    return {
        "total_revenue": float(total_revenue or 0),
        "total_invoices": int(total_invoices or 0),
        "top_dishes": top_dishes,
    }
```

### 8.2. Cập nhật `MyStatView` trong `RestaurantApp/admin.py`

Thêm `from datetime import date` và `from RestaurantApp import dao`, sửa lại `MyStatView`:

```python
class MyStatView(BaseView):
    @expose("/")
    def index(self):
        mode = request.args.get("mode", "day")
        date_val = request.args.get("date_val", date.today().isoformat())
        month_val = request.args.get("month_val", date.today().strftime("%Y-%m"))

        stats = dao.get_revenue_stats(mode=mode, date_str=date_val, month_str=month_val)
        return self.render(
            "admin/stats.html",
            mode=mode,
            date_val=date_val,
            month_val=month_val,
            stats=stats,
        )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRole.ADMIN
```

### 8.3. Cập nhật `RestaurantApp/templates/admin/stats.html`

*(Dùng 2 form lọc thuần HTML không cần JS; chỉ nhúng đúng 10 dòng Chart.js CDN để vẽ biểu đồ tròn theo yêu cầu đề)*

```html
{% extends 'admin/master.html' %}
{% block body %}
<h3 class="text-info text-center my-3">BÁO CÁO DOANH THU &amp; TOP MÓN BÁN CHẠY</h3>

<div class="row mb-4">
    <div class="col-md-6">
        <form method="get" class="form-inline">
            <input type="hidden" name="mode" value="day">
            <input type="date" name="date_val" value="{{ date_val }}" class="form-control mr-2">
            <button type="submit" class="btn btn-primary">Lọc theo ngày</button>
        </form>
    </div>
    <div class="col-md-6">
        <form method="get" class="form-inline justify-content-md-end">
            <input type="hidden" name="mode" value="month">
            <input type="month" name="month_val" value="{{ month_val }}" class="form-control mr-2">
            <button type="submit" class="btn btn-success">Lọc theo tháng</button>
        </form>
    </div>
</div>

<div class="row mb-4">
    <div class="col-md-6">
        <div class="alert alert-success text-center">
            <h5>Tổng doanh thu</h5>
            <h3>{{ "{:,.0f}".format(stats.total_revenue) }} VNĐ</h3>
        </div>
    </div>
    <div class="col-md-6">
        <div class="alert alert-info text-center">
            <h5>Tổng số hóa đơn</h5>
            <h3>{{ stats.total_invoices }}</h3>
        </div>
    </div>
</div>

<div class="row">
    <div class="col-md-7">
        <h5>Top món bán chạy</h5>
        <table class="table table-bordered table-striped">
            <thead>
                <tr>
                    <th>STT</th>
                    <th>Mã món</th>
                    <th>Tên món</th>
                    <th>Số lượng bán</th>
                    <th>Doanh thu (VNĐ)</th>
                </tr>
            </thead>
            <tbody>
                {% for d in stats.top_dishes %}
                <tr>
                    <td>{{ loop.index }}</td>
                    <td>{{ d[0] }}</td>
                    <td>{{ d[1] }}</td>
                    <td>{{ d[2] }}</td>
                    <td>{{ "{:,.0f}".format(d[3]) }}</td>
                </tr>
                {% else %}
                <tr><td colspan="5" class="text-center text-muted">Chưa có dữ liệu.</td></tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <div class="col-md-5">
        <h5 class="text-center">Biểu đồ tròn tỉ lệ món</h5>
        <canvas id="dishPieChart"></canvas>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const labels = [{% for d in stats.top_dishes %}{{ d[1]|tojson }},{% endfor %}];
const data = [{% for d in stats.top_dishes %}{{ d[2] }},{% endfor %}];
if (labels.length > 0) {
    new Chart(document.getElementById("dishPieChart"), {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: ["#ff6384", "#36a2eb", "#ffce56", "#4bc0c0", "#9966ff", "#ff9f40"]
            }]
        }
    });
}
</script>
{% endblock %}
```

### 8.4. Checklist kiểm tra Bước 6
- [ ] Vào `/admin/stats`, thử bấm **Lọc theo ngày** (hôm nay) -> hiện tổng doanh thu, bảng Top món giảm dần và biểu đồ tròn.
- [ ] Thử chọn một ngày không có hóa đơn -> hiện `0 VNĐ` và `"Chưa có dữ liệu."`.
- [ ] Thử bấm **Lọc theo tháng** -> lọc đúng tổng doanh thu & top món của tháng đó.

---

## 9. Kịch bản Demo & 5 câu hỏi hay gặp khi bảo vệ

### 9.1. Luồng demo trọn 5 yêu cầu trong 5 phút
1. **Admin (`/admin`) — YC 4:** Thử nhập trùng mã `LAU01` và giá `0` để chứng minh hệ thống kiểm tra quy định; thêm 1 món mới hợp lệ.
2. **Phục vụ (`/waiter`) — YC 1:** Mở Bàn 05, gọi 1 *Lẩu hải sản* (`Ít cay`), gọi *Nước suối* 2 lần -> chứng minh cộng dồn thành SL 2 và bàn chỉ có 1 phiếu mở.
3. **Bếp (`/kitchen`) — YC 2:** Ở cửa sổ thứ 2, đơn tự xuất hiện sau 5 giây -> bấm **Bắt đầu nấu** -> **Hoàn tất** -> món biến mất khỏi Bếp và bật thông báo bên màn hình Phục vụ.
4. **Thu ngân (`/cashier`) — YC 3:** Thanh toán 1 bàn dưới 500k (VAT 10%) và 1 bàn trên 500k (giảm 5% + VAT 10%), bấm **In hóa đơn**.
5. **Quản lý (`/admin/stats`) — YC 5:** Xem tổng doanh thu, bảng Top món bán chạy, biểu đồ tròn tỉ lệ món và thử lọc theo ngày/tháng.

### 9.2. 5 câu hỏi giảng viên hay hỏi
1. **Tại sao không dùng `session['cart']` như `SaleApp`?**
   -> Vì `session` chỉ nằm riêng trên trình duyệt của 1 người; đơn tại bàn phải lưu xuống MySQL (`Order`, `OrderDetail`) để Phục vụ, Bếp và Thu ngân cùng dùng chung dữ liệu.
2. **Làm sao đảm bảo 1 bàn chỉ có 1 phiếu mở và không trùng món?**
   -> Python kiểm tra phiếu `OPEN` trong `get_or_create_open_order` và cộng dồn `quantity` trong `add_item_to_table_order`; đồng thời CSDL có `UniqueConstraint("order_id", "dish_id")` chống trùng tuyệt đối.
3. **Khách ăn xong 1 phần Lẩu rồi gọi thêm 1 phần nữa thì Bếp xử lý thế nào?**
   -> `OrderDetail` lưu `quantity = 2` (để phiếu & hóa đơn không trùng dòng) và `served_quantity = 1` (đã làm xong). Màn hình Bếp hiển thị `pending_quantity = quantity - served_quantity = 1`.
4. **Tại sao phải lưu `unit_price` trong `OrderDetail` và `total_amount` trong `Invoice`?**
   -> Để giữ nguyên giá tại thời điểm bán; sau này quản trị viên sửa giá món ăn thì hóa đơn & doanh thu cũ không bị sai lệch.
5. **Xóa món ăn đã có trong hóa đơn có bị lỗi khóa ngoại không?**
   -> Không, `delete_model` trong `MyDishView` kiểm tra trước: nếu món từng xuất hiện trong `OrderDetail` thì chuyển `active = False` (xóa mềm) để giữ toàn vẹn dữ liệu báo cáo.
