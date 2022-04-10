from flask import Flask

from .route import build_routes
from ..app import App
from ..module import Module
from ..db import DBModule
from ..config import ConfigModule

class ApiModule(Module):
    __config: ConfigModule
    __db: DBModule
    __flask: Flask

    def __init__(self, app: App):
        self.__config = app.load_module(ConfigModule)
        self.__db = app.load_module(DBModule)

        self.__flask = Flask(__name__)
        build_routes(self.__flask, self.__config, self.__db)

    def run(self):
        self.__flask.run(debug=self.__config.debug)
