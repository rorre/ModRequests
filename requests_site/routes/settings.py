from flask import Blueprint, flash, render_template
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms.fields import BooleanField

from requests_site.decorator import bn_only
from requests_site.plugins import db

blueprint = Blueprint("settings", __name__)


class SettingsForm(FlaskForm):
    is_closed = BooleanField("Closed")
    allow_multiple_reqs = BooleanField("Allow Multiple Reqs")


@blueprint.route("/")
@bn_only
def index():
    form = SettingsForm()
    if form.validate_on_submit():
        current_user.is_closed = form.is_closed.value
        current_user.allow_multiple_reqs = form.allow_multiple_reqs.value
        db.session.add(current_user)
        db.session.commit()
        flash("Done applying settings.")
    return render_template("base/req.html", form=form)
