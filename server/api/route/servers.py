import json
from flask import Blueprint, request

from ...config import ConfigModule
from ...db import DBModule
from ...db.objects import ServerObject
from ...db.objects.base import DBPermission

def build_servers(config: ConfigModule, db: DBModule) -> Blueprint:
    servers = Blueprint("servers", __name__, url_prefix="/servers")

    @servers.route("/", methods=["GET"])
    def index_get():
        servers = db.get_all(ServerObject)

        return json.dumps([server.to_dict(config=config) for server in servers])

    @servers.route("/", methods=["POST"])
    def index_insert():
        object = ServerObject.from_dict(config=config, dict=request.json)

        return object.to_dict(config=config, permission=DBPermission.Auth)

    return servers
