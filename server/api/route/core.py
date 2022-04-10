from flask import Blueprint

from ...config import ConfigModule
from ...db import DBModule

def build_core(config: ConfigModule, db: DBModule) -> Blueprint:
    core = Blueprint("core", __name__)

    @core.route("/ping")
    def ping():
        return "true"

    return core
