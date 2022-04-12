from abc import ABC, abstractclassmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Callable, Dict, Optional, Type, Any
import uuid

from ...config import ConfigModule 

class DBFieldVisibility(Enum):
    Visible=auto()
    User=auto()
    Admin=auto()
    Invisible=auto()

class DBPermission(Enum):
    Guest=auto()
    User=auto()
    Admin=auto()
    DB=auto()

    def can_view_visibility(self, field: DBFieldVisibility) -> bool:
        if self == DBPermission.Guest:
            return field in [DBFieldVisibility.Visible]
        elif self == DBPermission.User:
            return field in [DBFieldVisibility.Visible, DBFieldVisibility.User]
        elif self == DBPermission.Admin:
            return not field == DBFieldVisibility.Invisible
        elif self == DBPermission.DB:
            return True
        else:
            return False

@dataclass(frozen=True)
class DBField(ABC):
    primary: bool=field(default=False)
    unique: bool=field(default=False)
    visibility: DBFieldVisibility=field(default=DBFieldVisibility.Visible)
    builder: Optional[Callable[[Any], Any]]=field(default=None)
    default_factory: Optional[Callable[[], Any]]=field(default=None)

@dataclass(frozen=True)
class DBString(DBField):
    size: int=field(default=-1)

@dataclass(frozen=True)
class DBInteger(DBField):
    size: int=field(default=-1)

@dataclass(frozen=True)
class DBRelation(DBField):
    other: Type["DBObject"]=field(default=None)

@dataclass(frozen=True)
class DBObject(ABC):
    id: str

    @classmethod
    def random_id(cls) -> str:
        return str(uuid.uuid4()).replace("-", "")

    @abstractclassmethod
    def get_collection_name(cls) -> str:
        return ""

    @abstractclassmethod
    def get_fields(cls, config: ConfigModule) -> Dict[str, DBField]:
        return {
            "id": DBString(default_factory=lambda: cls.random_id(), primary=True)
        }

    @abstractclassmethod
    def from_dict(cls, config: ConfigModule, dict: Dict[str, Any]) -> "DBObject":
        return None

    def to_dict(self, config: ConfigModule, permission: DBPermission=DBPermission.Guest) -> Dict[str, Any]:
        fields = self.get_fields(config)

        field_dict = {}
        for field_name, field in fields.items():
            if permission.can_view_visibility(field.visibility):
                field_dict[field_name] = getattr(self, field_name)

        return field_dict

    @classmethod
    def sanitize_dict_unsafe(cls, config: ConfigModule, dict: Dict[str, Any]) -> Dict[str, Any]:
        fields = cls.get_fields(config)

        field_dict = {}
        for field_name, field in fields.items():
            if not field_name in dict:
                continue

            entry = dict[field_name]

            if not field.builder is None:
                entry = field.builder(entry)
            elif isinstance(field, DBString):
                entry = str(entry)
            elif isinstance(field, DBInteger):
                entry = int(entry)
            else:
                raise Exception("TODO")

            field_dict[field_name] = entry

        return field_dict

    @classmethod
    def sanitize_dict(cls, config: ConfigModule, dict: Dict[str, Any]) -> Dict[str, Any]:
        fields = cls.get_fields(config)

        field_dict = {}
        for field_name, field in fields.items():
            if field_name in dict and not dict[field_name] is None:
                entry = dict[field_name]
            elif not field.default_factory is None:
                entry = field.default_factory()
            else:
                entry = None

            if not field.builder is None:
                entry = field.builder(entry)
            elif isinstance(field, DBString):
                try:
                    entry = str(entry)
                except:
                    raise Exception(f"{field_name} is \"{entry}\". Expected a str.")
            elif isinstance(field, DBInteger):
                try:
                    entry = int(entry)
                except:
                    raise Exception(f"{field_name} is \"{entry}\". Expected an int.")
            else:
                raise Exception("TODO")

            field_dict[field_name] = entry

        return field_dict
