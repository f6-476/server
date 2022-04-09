from flask import Blueprint

from ..db import DBModule

def build_core(db: DBModule) -> Blueprint:
    core = Blueprint("core", __name__)

    @core.route("/ping")
    def ping():
        return "pong"

    return core
