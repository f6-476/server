import json
from flask import Blueprint, request

from ...config import ConfigModule
from ...db import DBModule
from ...db.objects import ServerObject
from ...db.objects.base import DBObject, DBPermission

def build_servers(config: ConfigModule, db: DBModule) -> Blueprint:
    servers = Blueprint("servers", __name__, url_prefix="/servers")

    @servers.route("/", methods=["GET"])
    def index_get():
        servers = db.get_all(ServerObject)

        return json.dumps([server.to_dict(config=config) for server in servers])

    @servers.route("/", methods=["POST"])
    def index_insert():
        if not request.is_json:
            raise Exception("Invalid body.")

        dict = request.json

        dict["id"] = None
        dict["token"] = None
        dict["host"] = request.remote_addr
        dict["time"] = None

        object = ServerObject.from_dict(config=config, dict=dict)
        if not db.insert(object):
            raise Exception("Create failed.")

        if not db.get_id(ServerObject, object.id):
            raise Exception("Created failed.")

        return object.to_dict(config=config, permission=DBPermission.Admin)

    @servers.route("/<id>", methods=["GET", "POST"])
    def server_get(id: str):
        object = db.get_id(ServerObject, id)

        if object is None:
            raise Exception("Server not found.")

        permission = DBPermission.Guest
        if request.method == "POST" and request.is_json:
            data = request.json

            if "password" in data:
                hash_password = ServerObject.hash_password(config, str(data["password"]))

                # TODO: Prevent timing attack.
                if object.password == hash_password:
                    permission = DBPermission.User

        return object.to_dict(config=config, permission=permission)

    def valid_token(object: DBObject) -> bool:
        if object is None:
            return False

        authorization = request.headers["Authorization"].split(" ")
        if not (len(authorization) == 2 and authorization[0] == "Bearer"):
            return False
        token = authorization[1]

        # TODO: Prevent timing attack.
        return object.token == token

    @servers.route("/<id>", methods=["PUT"])
    def server_update(id: str):
        object = db.get_id(ServerObject, id)

        if not request.is_json:
            raise Exception("Invalid body.")

        body = request.json
        if valid_token(object):
            if db.update(ServerObject, id, body):
                return object.to_dict(config, DBPermission.Admin)

        raise Exception("Update failed.")

    @servers.route("/<id>", methods=["DELETE"])
    def server_delete(id: str):
        object = db.get_id(ServerObject, id)

        if valid_token(object):
            if db.delete(ServerObject, id):
                return object.to_dict(config, DBPermission.Admin)

        raise Exception("Delete failed.")

    return servers
