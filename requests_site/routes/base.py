import requests
from flask import (
    Blueprint,
    current_app,
    jsonify,
    make_response,
    render_template,
    redirect,
    url_for,
)
from flask_login import current_user, login_required

blueprint = Blueprint("base", __name__)


@blueprint.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("request.listing"))
    return render_template("login.html")


@blueprint.route("/<mode>/<mapid>")
@login_required
def get_map(mode, mapid):
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
