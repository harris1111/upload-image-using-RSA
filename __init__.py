from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root@localhost/crypto_project?charset=utf8mb4"


#app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://ugwvdlisgyydugol:ylYw4TwKw7IGmzRoKkOa@br1m5ieutnnxcbnrvyhk-mysql.services.clever-cloud.com:3306/br1m5ieutnnxcbnrvyhk?charset=utf8mb4"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = "AG(ASDAGIA(*&!@"
db = SQLAlchemy(app=app)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

my_login = LoginManager(app=app)
my_login.login_view = 'auth'

