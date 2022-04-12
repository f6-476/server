from flask import Flask

from ...config import ConfigModule
from ...db import DBModule
from .core import build_core
from .servers import build_servers

def build_routes(app: Flask, config: ConfigModule, db: DBModule):
    @app.errorhandler(Exception)
    def error_handler(error: Exception):
        return {"message": str(error)}, 500

    app.register_blueprint(build_core(config, db))
    app.register_blueprint(build_servers(config, db))
