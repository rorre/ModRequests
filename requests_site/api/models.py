from flask_restx import fields

user_model = {
    "osu_uid": fields.Integer(required=True, description="User's osu! user ID"),
    "username": fields.String(required=True, description="User's osu! username"),
    "is_bn": fields.Boolean(
        required=True, description="Whether the user is a BN in this site"
    ),
    "is_closed": fields.Boolean(description="Whether the nominator is closed"),
    "allow_multiple_reqs": fields.Boolean(
        description="Whether the nominator allows multiple concurrent requests"
    ),
    "rules": fields.String(required=True, description="Nominator's rule, in markdown"),
    "notice": fields.String(
        required=True, description="Nominator's notice, in markdown"
    ),
}

request_model = {
    "id": fields.Integer(required=True, description="The cat identifier"),
    "status": fields.Integer(required=True, description="Status enumerator"),
    "requester": fields.Nested(
        user_model, required=True, description="Owner of request"
    ),
    "target_bn": fields.Nested(
        user_model, required=True, description="The nominator being requested"
    ),
    "song": fields.String(required=True, description="The mapset's metadata"),
    "link": fields.String(required=True, description="The mapset's URL"),
    "mapset_id": fields.Integer(required=True, description="The mapset's ID in osu!"),
    "mapper": fields.String(required=True, description="The mapset's mapper"),
    "reason": fields.String(description="Reasoning of rejection"),
}

paginated_model = {
    "page": fields.Integer(description="Currently accessed page"),
    "next_page": fields.Integer(description="Next page number"),
    "items": fields.Nested(fields.List(request_model), description="Query result"),
}
