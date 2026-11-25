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


        existed = Dish.query.filter(Dish.code == model.code).first()
        if existed and (is_created or existed.id != model.id):
            raise ValidationError(f"Mã món '{model.code}' đã tồn tại!")


        if model.price is None or model.price <= 0:
            raise ValidationError("Giá món phải lớn hơn 0 VNĐ!")
        if not model.category:
            raise ValidationError("Món ăn phải thuộc nhóm món hợp lệ!")

    def delete_model(self, model):

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