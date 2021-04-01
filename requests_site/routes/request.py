from datetime import datetime
from typing import Any, Dict

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from sqlalchemy import and_, or_
from sqlalchemy.orm import load_only
from wtforms.fields import (
    IntegerField,
    SelectField,
    SubmitField,
    TextAreaField,
    TextField,
)
from wtforms.fields.html5 import URLField
from wtforms.validators import Required

from requests_site.decorator import bn_only
from requests_site.models import Request, Status, User, db
from requests_site.webhook import send_hook

blueprint = Blueprint("request", __name__, url_prefix="/request")


class MockSQLResult:
    items = []


class NewRequestForm(FlaskForm):
    link = URLField("Mapset URL", validators=[Required()])
    song = TextField("Artist - Title", validators=[Required()])
    mapset_id = IntegerField("Mapset ID", validators=[Required()])
    mapper = TextField("Mapper", validators=[Required()])
    note = TextAreaField("Note")
    submit = SubmitField("Submit", validators=[Required()])
    target_bn = SelectField("Nominator")


@blueprint.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = NewRequestForm()
    form.target_bn.choices = [("", "Nominator")]

    u: User
    for u in User.query.filter_by(is_bn=True):
        extra = " (CLOSED)" if u.is_closed else ""
        form.target_bn.choices.append([str(u.osu_uid), u.username + extra])

    if form.validate_on_submit():
        if not form.target_bn.data:
            flash("Invalid nominator.")
            return render_template("page/req.html", form=form, scripts=["request.js"])

        form.target_bn.data = int(form.target_bn.data)
        target_bn: User = User.query.filter_by(osu_uid=form.target_bn.data).first()
        if target_bn.is_closed:
            flash(f"{target_bn.username} is currently closed.")
            return render_template("page/req.html", form=form, scripts=["request.js"])

        # Look if the target BN allows multiple requests or not.
        # If not, then check if there is an existing request by the user.
        if not target_bn.allow_multiple_reqs:
            existing_request = Request.query.filter(
                and_(
                    Request.requester_id == current_user.osu_uid,
                    Request.status_ == Status.Pending.value,
                    Request.target_bn_id == form.target_bn.data,
                )
            ).all()
            if existing_request:
                flash("You already have a request opened.")
                return render_template(
                    "page/req.html", form=form, scripts=["request.js"]
                )

        # Disallow duplicate map as it will cause spam.
        # Only checking the one that is pending though.
        existing_map = Request.query.filter(
            and_(
                Request.mapset_id == form.mapset_id.data,
                Request.status_.in_([Status.Pending.value, Status.Accepted.value]),
                Request.target_bn_id == form.target_bn.data,
            )
        ).all()
        if existing_map:
            flash("There is a pending request for that beatmap already.")
            return render_template("page/req.html", form=form, scripts=["request.js"])

        request = Request(
            status_=Status.Pending.value,
            song=form.song.data,
            link=form.link.data,
            mapset_id=form.mapset_id.data,
            mapper=form.mapper.data,
            note=form.note.data,
            target_bn=target_bn,
        )
        current_user.requests.append(request)
        db.session.add(request)
        db.session.commit()
        send_hook("add_request", request)
        flash("Done adding request.")
        return redirect(url_for("request.listing", nominator=target_bn.osu_uid))
    return render_template("page/req.html", form=form, scripts=["request.js"])


@blueprint.route("/<int:set_id>", methods=["POST"])
@bn_only
def update(set_id: int):
    mapset: Request = Request.query.filter_by(id=set_id).first_or_404()
    if mapset.target_bn_id != current_user.osu_uid:
        return make_response(jsonify(err="You can't control other BN's request."), 400)

    try:
        data: Dict[str, Any] = request.json
        for key in data:
            setattr(mapset, key, data[key])
        mapset.last_updated = datetime.utcnow()
        db.session.add(mapset)
        db.session.commit()
        send_hook("update_request", mapset)
        return jsonify(msg="OK")
    except Exception:
        return make_response(jsonify(err="An error occured."), 500)


@blueprint.route("/<int:set_id>/delete")
@login_required
def delete(set_id: int):
    mapset: Request = Request.query.filter_by(id=set_id).first_or_404()
    if mapset.requester_id != current_user.osu_uid:
        return abort(403)
    send_hook("delete_request", mapset)
    db.session.delete(mapset)
    db.session.commit()
    flash("Deleted.")
    return redirect(url_for("base.index"))


def fetch_db(filter_op, order_op):
    page = request.args.get("page", 1, type=int)
    reqs = Request.query.filter(filter_op).order_by(order_op)
    total = reqs.count()
    reqs_paginated = reqs.paginate(page, 10, False)

    return reqs_paginated, total, reqs


@blueprint.route("/list")
def listing():
    nominator_id = session.get("nominator", current_app.config["DEFAULT_NOMINATOR"])
    filter_op = and_(Request.status_ == 0, Request.target_bn_id == nominator_id)
    order_op = Request.requested_at.desc()
    reqs, total, _ = fetch_db(filter_op, order_op)

    return render_template(
        "page/index.html",
        pagination=reqs,
        reqs=reqs.items,
        title="Requests list",
        scripts=["admin.js", "index.js"],
        show_last_update=False,
        selected=nominator_id,
        count=total,
    )


@blueprint.route("/list/mine")
@login_required
def mine():
    filter_op = Request.requester == current_user
    order_op = Request.requested_at.desc()
    reqs = fetch_db(filter_op, order_op)[0]

    return render_template(
        "page/index-modal.html",
        pagination=reqs,
        reqs=reqs.items,
        title="My requests",
        subtitle="Where all of your (past) requests resides.",
        scripts=["admin.js", "index.js"],
    )


@blueprint.route("/list/archive")
def archive():
    nominator_id = session.get("nominator", current_app.config["DEFAULT_NOMINATOR"])
    filter_op = and_(Request.status_ == 3, Request.target_bn_id == nominator_id)
    order_op = Request.requested_at.desc()
    reqs = fetch_db(filter_op, order_op)[0]

    return render_template(
        "page/index-modal.html",
        pagination=reqs,
        reqs=reqs.items,
        title="Archived requests",
        subtitle="All of the requests that is already done and not for nominations.",
        scripts=["admin.js", "index.js"],
        selected=nominator_id,
    )


@blueprint.route("/list/rejected")
def rejected():
    nominator_id = session.get("nominator", current_app.config["DEFAULT_NOMINATOR"])
    nominator = User.query.options(load_only("show_rejected")).get_or_404(nominator_id)
    show_rejected = nominator.show_rejected
    if show_rejected:
        filter_op = and_(Request.status_ == 1, Request.target_bn_id == nominator_id)
        order_op = Request.last_updated.desc()
        reqs = fetch_db(filter_op, order_op)[0]
    else:
        reqs = MockSQLResult()

    return render_template(
        "page/index-modal.html",
        pagination=reqs,
        reqs=reqs.items,
        title="Rejected requests",
        subtitle="Declined requests are shown here. Only if the nominator enables it, though.",
        scripts=["admin.js", "index.js"],
        selected=nominator_id,
    )


@blueprint.route("/list/accepted")
def accepted():
    nominator_id = session.get("nominator", current_app.config["DEFAULT_NOMINATOR"])
    filter_op = and_(Request.status_ == 2, Request.target_bn_id == nominator_id)
    order_op = Request.last_updated.desc()
    reqs, total, _ = fetch_db(filter_op, order_op)

    return render_template(
        "page/index.html",
        pagination=reqs,
        reqs=reqs.items,
        title="Accepted requests",
        subtitle="Those who gets accepted. Once they're done, they will end up in Archive.",
        scripts=["admin.js", "index.js"],
        show_last_update=True,
        selected=nominator_id,
        count=total,
    )


@blueprint.route("/list/nominations")
def nominations():
    nominator_id = session.get("nominator", current_app.config["DEFAULT_NOMINATOR"])
    filter_op = and_(
        or_(Request.status_ == 4, Request.status_ == 5),
        Request.target_bn_id == nominator_id,
    )
    order_op = Request.last_updated.desc()
    reqs = fetch_db(filter_op, order_op)[0]

    return render_template(
        "page/index-table.html",
        pagination=reqs,
        reqs=reqs.items,
        title="Nominations",
        subtitle="Beatmaps that got me interested in pushing will be logged here.",
        scripts=["admin.js", "index.js"],
        with_reason=False,
        selected=nominator_id,
    )
