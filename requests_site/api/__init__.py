from flask import Blueprint
from flask_restx import Api

blueprint = Blueprint("api", __name__, url_prefix="/api/1")
api = Api(
    blueprint,
    title="Mod Requests API",
    version="1.0",
    description="API for mod requests.",
)
