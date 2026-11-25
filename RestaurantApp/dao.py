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