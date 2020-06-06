from datetime import datetime

from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
    abort,
)
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from sqlalchemy import and_
from wtforms.fields import IntegerField, SubmitField, TextField
from wtforms.fields.html5 import URLField
from wtforms.validators import Required

from requests_site.decorator import admin_only
from requests_site.models import Request, Status, db
from requests_site.webhook import send_hook

blueprint = Blueprint("request", __name__, url_prefix="/request")


class NewRequestForm(FlaskForm):
    link = URLField("Mapset URL", validators=[Required()])
    song = TextField("Artist - Title", validators=[Required()])
    mapset_id = IntegerField("Mapset ID", validators=[Required()])
    mapper = TextField("Mapper", validators=[Required()])
    submit = SubmitField("Submit", validators=[Required()])


@blueprint.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = NewRequestForm()
    if form.validate_on_submit():
        existing_requester = Request.query.filter(
            and_(
                Request.requester_id == current_user.osu_uid,
                Request.status_ == Status.Pending.value,
            )
        ).all()
        if existing_requester:
            flash("You already have a request opened.")
            return render_template("base/req.html", form=form, scripts=["request.js"])

        existing_request = Request.query.filter(
            and_(
                Request.mapset_id == form.mapset_id.data,
                Request.status_.in_([Status.Pending.value, Status.Accepted.value]),
            )
        ).all()
        if existing_request:
            flash("There is a pending request for that beatmap already.")
            return render_template("base/req.html", form=form, scripts=["request.js"])

        request = Request(
            status_=Status.Pending.value,
            song=form.song.data,
            link=form.link.data,
            mapset_id=form.mapset_id.data,
            mapper=form.mapper.data,
        )
        current_user.requests.append(request)
        db.session.add(request)
        db.session.commit()
        send_hook("add_request", request)
        flash("Done adding request.")
        return redirect(url_for("base.index"))
    return render_template("base/req.html", form=form, scripts=["request.js"])


@blueprint.route("/<int:set_id>", methods=["POST"])
@admin_only
def update(set_id):
    mapset = Request.query.filter_by(id=set_id).first_or_404()
    try:
        data = request.json
        for key in data:
            setattr(mapset, key, data[key])
        mapset.last_updated = datetime.utcnow()
        db.session.add(mapset)
        db.session.commit()
        send_hook("update_request", mapset)
        return jsonify(msg="OK")
    except Exception:
        return jsonify(err="An error occured.")


@blueprint.route("/<int:set_id>/delete")
@login_required
def delete(set_id):
    mapset = Request.query.filter_by(id=set_id).first_or_404()
    if mapset.requester_id != current_user.osu_uid:
        return abort(403)
    db.session.delete(mapset)
    db.session.commit()
    send_hook("delete_request", mapset)
    flash("Deleted.")
    return redirect(url_for("base.index"))


@blueprint.route("/search/<query>")
def search(query):
    json = {"results": []}
    requests = Request.query.filter(Request.song.like(f"%{query}%")).all()
    for req in requests:
        new = {}
        new["title"] = req.song
        new["description"] = f"Mapped by {req.mapper} | {req.status.name}"
        json["results"].append(new)
    return jsonify(json)


@blueprint.route("/list")
def listing():
    page = request.args.get("page", 1, type=int)
    reqs = (
        Request.query.filter(Request.status_ == 0)
        .order_by(Request.requested_at.desc())
        .paginate(page, 10, False)
    )
    next_url = url_for("request.listing", page=reqs.next_num) if reqs.has_next else None
    prev_url = url_for("request.listing", page=reqs.prev_num) if reqs.has_prev else None

    return render_template(
        "base/index.html",
        reqs=reqs.items,
        title="Requests list",
        scripts=["admin.js", "index.js"],
        next_url=next_url,
        prev_url=prev_url,
        show_last_update=False,
    )


@blueprint.route("/list/mine")
@login_required
def mine():
    page = request.args.get("page", 1, type=int)
    reqs = (
        Request.query.filter(Request.requester == current_user)
        .order_by(Request.requested_at.desc())
        .paginate(page, 10, False)
    )
    next_url = url_for("request.listing", page=reqs.next_num) if reqs.has_next else None
    prev_url = url_for("request.listing", page=reqs.prev_num) if reqs.has_prev else None

    return render_template(
        "base/index-table.html",
        reqs=reqs.items,
        title="My requests",
        subtitle="Where all of your (past) requests resides.",
        scripts=["admin.js", "index.js"],
        next_url=next_url,
        prev_url=prev_url,
        with_reason=True
    )


@blueprint.route("/list/archive")
def archive():
    page = request.args.get("page", 1, type=int)
    reqs = (
        Request.query.filter(Request.status_ == 3)
        .order_by(Request.requested_at.desc())
        .paginate(page, 10, False)
    )
    next_url = url_for("request.listing", page=reqs.next_num) if reqs.has_next else None
    prev_url = url_for("request.listing", page=reqs.prev_num) if reqs.has_prev else None

    return render_template(
        "base/index.html",
        reqs=reqs.items,
        title="Archived requests",
        subtitle="All of the requests that is already done.",
        scripts=["admin.js", "index.js"],
        next_url=next_url,
        prev_url=prev_url,
        show_last_update=True,
    )


@blueprint.route("/list/accepted")
def accepted():
    page = request.args.get("page", 1, type=int)
    reqs = (
        Request.query.filter(Request.status_ == 2)
        .order_by(Request.requested_at.desc())
        .paginate(page, 10, False)
    )
    next_url = url_for("request.listing", page=reqs.next_num) if reqs.has_next else None
    prev_url = url_for("request.listing", page=reqs.prev_num) if reqs.has_prev else None

    return render_template(
        "base/index.html",
        reqs=reqs.items,
        title="Accepted requests",
        subtitle="Those who gets accepted. Once they're done, they will end up in Archive.",
        scripts=["admin.js", "index.js"],
        next_url=next_url,
        prev_url=prev_url,
        show_last_update=True,
    )
