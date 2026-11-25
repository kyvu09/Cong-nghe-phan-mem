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

@app.route("/waiter")
def waiter_tables():
    return "Trang Phục vụ - <a href='/logout'>Đăng xuất</a>"


@app.route("/kitchen")
def kitchen_dashboard():
    return "Trang Bếp - <a href='/logout'>Đăng xuất</a>"


@app.route("/cashier")
def cashier_dashboard():
    return "Trang Thu ngân - <a href='/logout'>Đăng xuất</a>"

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
