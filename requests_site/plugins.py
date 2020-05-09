from authlib.integrations.flask_client import OAuth
from flask_admin import Admin
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Environment, Bundle

db = SQLAlchemy()
login_manager = LoginManager()
oauth = OAuth()
admin = Admin(name="Ren's Requests")
migrate = Migrate()
bundler = Environment()

js = Bundle('admin.js', 'global.js', 'index.js', 'request.js',
            filters='jsmin', output="bundle.js")
bundler.register("js_all", js)

login_manager.login_view = "user.login"
