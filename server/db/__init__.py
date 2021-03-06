from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, TypeVar

from ..app import App
from ..module import Module
from ..config import ConfigModule
from .objects import DBObject, ServerObject

TOBJ = TypeVar("TOBJ", bound=DBObject)
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
    def get_id(self, type: Type[TOBJ], id: str) -> Optional[TOBJ]:
        return None

    @abstractmethod
    def get_all(self, type: Type[TOBJ]) -> List[TOBJ]:
        return []

    @abstractmethod
    def insert(self, object: DBObject) -> bool:
        return False

    @abstractmethod
    def update(self, type: Type[DBObject], id: str, new: Dict[str, Any]) -> bool:
        return False

    @abstractmethod
    def delete(self, type: Type[TOBJ], id: str) -> bool:
        return None
