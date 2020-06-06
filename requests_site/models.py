import enum
from datetime import datetime

from requests_site.plugins import db, login_manager


class User(db.Model):
    __tablename__ = "users"

    osu_uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True, nullable=False)
    access_token = db.Column(db.String, nullable=True)
    refresh_token = db.String(length=200)
    expires_at = db.Column(db.Integer)

    is_admin = db.Column(db.Boolean, index=True, nullable=False, default=False)
    is_active = True
    is_authenticated = True

    requests = db.relationship("Request", backref="requester", lazy="dynamic")

    @staticmethod
    @login_manager.user_loader
    def load_user(osu_uid):
        return User.query.filter_by(osu_uid=osu_uid).first()

    def get_id(self):
        return str(self.osu_uid)

    @property
    def current_requests(self):
        return (
            Request.query.filter(Request.requester_id == self.osu_uid)
            .filter(Request.status != Status.Completed.value)
            .filter(Request.status != Status.Rejected.value)
            .all()
        )

    def to_token(self):
        return dict(
            access_token=self.access_token,
            token_type="Bearer",
            refresh_token=self.refresh_token,
            expires_at=self.expires_at,
        )


class Status(enum.IntEnum):
    Pending = 0
    Declined = 1
    Accepted = 2
    Archived = 3
    Waiting_For_Recheck = 4
    Nominated = 5


class Request(db.Model):
    __tablename__ = "requests"

    id = db.Column(db.Integer, primary_key=True)
    status_ = db.Column(
        "status", db.Integer, nullable=False, default=Status.Pending.value
    )

    requester_id = db.Column(db.Integer, db.ForeignKey("users.osu_uid"))
    requested_at = db.Column(
        db.DateTime, index=True, nullable=False, default=datetime.utcnow
    )
    last_updated = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    song = db.Column(db.Unicode, nullable=False)
    link = db.Column(db.Unicode, nullable=True)
    mapset_id = db.Column(db.Integer, nullable=True)
    mapper = db.Column(db.Unicode, nullable=False)
    reason = db.Column(db.Text)
    archive = db.Column(db.Boolean, default=False)

    @property
    def status(self):
        return Status(self.status_)

    @status.setter
    def status(self, value):
        self.status_ = value.value
