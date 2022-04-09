from flask import Blueprint

from ..db import DBModule
from ..db.objects import ServerObject

def build_servers(db: DBModule) -> Blueprint:
    servers = Blueprint("servers", __name__, url_prefix="/servers")

    @servers.route("/")
    def index():
        servers = db.get_all(ServerObject)

        server_json = []
        for server in servers:
            server_json.append({"name": server.name})

        return {"servers": server_json}

    return servers
