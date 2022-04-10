from dataclasses import dataclass, field
from typing import Any, Dict

import bcrypt

from ...config import ConfigModule
from .base import DBField, DBFieldVisibility, DBObject, DBString

@dataclass(frozen=True)
class ServerObject(DBObject):
    name: str
    password: str
    address: str
    port: int

    @classmethod
    def get_collection_name(cls) -> str:
        return "servers"

    @classmethod
    def get_fields(cls, config: ConfigModule) -> Dict[str, DBField]:
        return {
            **super().get_fields(config),
            "name": DBString(),
            "address": DBString(visibility=DBFieldVisibility.Auth),
            "port": DBString(visibility=DBFieldVisibility.Auth),
            "password": DBString(visibility=DBFieldVisibility.Invisible, transform=lambda password: bcrypt.hashpw(str(password).encode(), config.salt).decode())
        }

    @classmethod
    def from_dict(cls, config: ConfigModule, dict: Dict[str, Any]) -> "ServerObject":
        return ServerObject(**cls.sanitize_dict(config, dict))
