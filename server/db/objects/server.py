from typing import Dict

from .base import DBField, DBObject, DBString

class ServerObject(DBObject):
    __name: str

    def __init__(self, name: str):
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    @classmethod
    def get_collection_name(cls) -> str:
        return "servers"

    @classmethod
    def get_fields(cls) -> Dict[str, DBField]:
        return {
            "name": DBString()
        }
