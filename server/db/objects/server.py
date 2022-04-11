from dataclasses import dataclass, field
from typing import Any, Dict
import uuid
import bcrypt

from ...config import ConfigModule
from .base import DBField, DBFieldVisibility, DBInteger, DBObject, DBString

@dataclass(frozen=True)
class ServerObject(DBObject):
    name: str
    host: str
    port: int
    password: str
    token: str
    count: int

    @classmethod
    def get_collection_name(cls) -> str:
        return "servers"

    @classmethod
    def hash_password(cls, config: ConfigModule, password: str) -> str:
        return bcrypt.hashpw(str(password).encode(), config.salt).decode()

    @classmethod
    def get_fields(cls, config: ConfigModule) -> Dict[str, DBField]:
        return {
            **super().get_fields(config),
            "name": DBString(),
            "host": DBString(visibility=DBFieldVisibility.User),
            "port": DBInteger(visibility=DBFieldVisibility.User),
            "password": DBString(builder=lambda password: cls.hash_password(config, password), visibility=DBFieldVisibility.Invisible),
            "token": DBString(default_factory=lambda: str(uuid.uuid4()).replace("-", ""), visibility=DBFieldVisibility.Admin),
            "count": DBInteger(default_factory=lambda: 0)
        }

    @classmethod
    def from_dict(cls, config: ConfigModule, dict: Dict[str, Any]) -> "ServerObject":
        return ServerObject(**cls.sanitize_dict(config, dict))
