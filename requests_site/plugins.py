import re

from authlib.integrations.flask_client import OAuth
from flask_admin import Admin
from flask_assets import Bundle, Environment
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from jinja2 import Markup, escape, evalcontextfilter
from sqlalchemy import MetaData

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
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
