import login
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'restaurant-btl-detai10-secret-key'
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:kyvu2609@localhost/restaurantdb?charset=utf8mb4"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

app.config["VAT_RATE"] = 0.10
app.config["DISCOUNT_THRESHOLD"] = 500000
app.config["DISCOUNT_RATE"] = 0.05

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login_my_user'
