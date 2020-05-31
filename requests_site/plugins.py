import re

from authlib.integrations.flask_client import OAuth
from flask_admin import Admin
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Environment, Bundle
from jinja2 import evalcontextfilter, Markup, escape

db = SQLAlchemy()
login_manager = LoginManager()
oauth = OAuth()
admin = Admin(name="Ren's Requests")
migrate = Migrate()
bundler = Environment()

js = Bundle(
    "admin.js",
    "global.js",
    "index.js",
    "request.js",
    filters="jsmin",
    output="bundle.js",
)
bundler.register("js_all", js)

login_manager.login_view = "user.login"

_paragraph_re = re.compile(r"(?:\r\n|\r|\n){2,}")


@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u"\n\n".join(
        u"<p>%s</p>" % p.replace("\n", "<br>\n")
        for p in _paragraph_re.split(escape(value))
    )
    if eval_ctx.autoescape:
        result = Markup(result)
    return result
