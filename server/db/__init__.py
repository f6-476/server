from abc import ABC, abstractmethod
from typing import List, Type

from ..app import App
from ..module import Module
from ..config import ConfigModule
from .objects import DBObject, ServerObject

DB_OBJECTS: List[Type[DBObject]] = [ServerObject]
class DBModule(Module, ABC):
    _config: ConfigModule

    def __init__(self, app: App):
        self._config = app.load_module(ConfigModule)
        self.register_objects(DB_OBJECTS)

    @abstractmethod
    def register_objects(self, types: List[Type[DBObject]]):
        pass

    @abstractmethod
    def get_all(self, type: Type[DBObject]) -> List[DBObject]:
        return []
