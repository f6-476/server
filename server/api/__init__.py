from flask import Flask

from ..app import App
from ..module import Module
from ..db import DBModule
from ..config import ConfigModule
from .core import build_core
from .servers import build_servers

class ApiModule(Module):
    __config: ConfigModule
    __db: DBModule
    __flask: Flask

    def __init__(self, app: App):
        self.__config = app.load_module(ConfigModule)
        self.__db = app.load_module(DBModule)

        self.__flask = Flask(__name__)
        self.__flask.register_blueprint(build_core(self.__db))
        self.__flask.register_blueprint(build_servers(self.__db))

    def run(self):
        self.__flask.run(debug=self.__config.debug)
