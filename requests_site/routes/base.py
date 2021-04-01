import requests
from flask import (
    Blueprint,
    current_app,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required

from requests_site.models import User
from requests_site.plugins import md

blueprint = Blueprint("base", __name__)


@blueprint.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("request.listing"))
    return render_template("login.html")


@blueprint.route("/map/<mode>/<int:mapid>")
@login_required
def get_map(mode: int, mapid: int):
    osu_token = current_app.config["OSU_TOKEN"]
    try:
        res = requests.get(
            "https://osu.ppy.sh/api/get_beatmaps?k={}&{}={}".format(
                osu_token, mode, mapid
            )
        ).json()

        if not res:
            return make_response(jsonify(err="No such beatmap found."), 400)
        if int(res[0]["approved"]) > 0:
            return make_response(
                jsonify(err="Map is not in Pending/WIP/Graveyard."), 400
            )

        return jsonify(
            song=f"{res[0]['artist']} - {res[0]['title']}",
            mapset_id=res[0]["beatmapset_id"],
            mapper=res[0]["creator"],
        )
    except Exception:
        return make_response(jsonify(err="Can't ask osu! API."), 400)


@blueprint.route("/rules/<int:uid>")
def get_rules(uid: int):
    user = User.query.filter_by(osu_uid=uid).first()
    if not user:
        return make_response(jsonify(err="No user with that user id."), 400)
    rules_html = md(user.rules)
    return render_template("md.html", md=rules_html)


@blueprint.route("/support")
def support():
    return render_template("page/support.html")


@blueprint.route("/set-nominator")
def set_nominator():
    session["nominator"] = request.args.get("nominator")
    redirect_url = request.referrer or url_for("request.listing")
    return redirect(redirect_url)


@blueprint.route("/survey")
def survey():
    session["survey_done"] = False
    return render_template("page/survey.html")


@blueprint.route("/surveyFinal")
def survey_done():
    session["survey_done"] = True
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")


@blueprint.route("/surveyStatus")
def survey_status():
    return {"status": session.get("survey_done", False)}
