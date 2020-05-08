from flask import Blueprint, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user

from requests_site.models import User, db
from requests_site.plugins import oauth

blueprint = Blueprint("user", __name__, url_prefix="/user")


@blueprint.route("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("base.index"))

    redirect_uri = url_for("user.authorize", _external=True)
    return oauth.osu.authorize_redirect(redirect_uri)


@blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("base.index"))


@blueprint.route("/authorize")
def authorize():
    token = oauth.osu.authorize_access_token()
    resp = oauth.osu.get("me", token=token)
    profile = resp.json()

    uid = profile["id"]
    this_user = User.query.filter_by(osu_uid=uid).first()
    if this_user is None:
        this_user = User(osu_uid=uid)
    this_user.username = profile["username"]
    this_user.access_token = token["access_token"]
    this_user.refresh_token = token.get("refresh_token")
    this_user.expires_at = token["expires_in"]

    db.session.add(this_user)
    db.session.commit()
    login_user(this_user)

    return redirect(url_for("base.index"))
