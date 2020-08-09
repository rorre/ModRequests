from flask import Blueprint, flash, render_template
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms.fields import BooleanField, TextAreaField, SubmitField

from requests_site.decorator import bn_only
from requests_site.plugins import db

blueprint = Blueprint("settings", __name__, url_prefix="/settings")


class SettingsForm(FlaskForm):
    is_closed = BooleanField("Closed")
    allow_multiple_reqs = BooleanField("Allow multiple reqs")
    show_rejected = BooleanField("Show rejected maps")
    rules = TextAreaField("Rules")
    notice = TextAreaField("Notice")
    show_notice = BooleanField("Show notice")
    submit = SubmitField("Save")


@blueprint.route("/", methods=["GET", "POST"])
@bn_only
def index():
    form = SettingsForm()
    form.is_closed.default = current_user.is_closed
    form.allow_multiple_reqs.default = current_user.allow_multiple_reqs
    form.rules.default = current_user.rules
    form.show_rejected.default = current_user.show_rejected
    form.notice.default = current_user.notice
    form.show_notice.default = current_user.show_notice

    if form.validate_on_submit():
        current_user.is_closed = form.is_closed.data
        current_user.allow_multiple_reqs = form.allow_multiple_reqs.data
        current_user.rules = form.rules.data
        current_user.show_rejected = form.show_rejected.data
        current_user.notice = form.notice.data
        current_user.show_notice = form.show_notice.data

        db.session.commit()
        flash("Done applying settings.")
    else:
        form.process()
    return render_template("base/settings.html", form=form)
