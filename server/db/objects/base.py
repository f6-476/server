from abc import ABC, abstractclassmethod
from enum import Enum, auto
from typing import Dict, Type

class DBField(ABC):
    pass

class DBString(DBField):
    __size: int

    def __init__(self, size: int=-1):
        self.__size = size

    @property
    def size(self) -> int:
        return self.__size

class DBInteger(DBField):
    __size: int

    def __init__(self, size: int=-1):
        self.__size = size

    @property
    def size(self) -> int:
        return self.__size

class DBRelation(DBField):
    __other: Type["DBObject"]

    def __init__(self, other: Type["DBObject"]):
        self.__other = other

    @property
    def other(self) -> Type["DBObject"]:
        return self.__other

class DBObject(ABC):
    @abstractclassmethod
    def get_collection_name(self) -> str:
        return ""

    @abstractclassmethod
    def get_fields(self) -> Dict[str, DBField]:
        return []
