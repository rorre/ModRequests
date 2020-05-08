from authlib.integrations.flask_client import OAuth
from flask_admin import Admin
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()
oauth = OAuth()
admin = Admin(name="Ren's Requests")
migrate = Migrate()

login_manager.login_view = "user.login"
