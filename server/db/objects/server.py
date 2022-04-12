from dataclasses import dataclass
from typing import Any, Dict
import uuid
import bcrypt
import socket
import time

from ...config import ConfigModule
from .base import DBField, DBFieldVisibility, DBInteger, DBObject, DBString

@dataclass(frozen=True)
class ServerObject(DBObject):
    time: int
    name: str
    host: str
    port: int
    count: int
    password: str
    token: str

    def ping(self) -> bool:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(3.0)

        for _ in range(3):
            sock.sendto(b"\x00" * 10, (self.host, self.port))

            try:
                msg, _ = sock.recvfrom(1024)
                return len(msg) == 18
            except:
                return False

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
            "time": DBInteger(default_factory=lambda: int(time.time())),
            "name": DBString(),
            "host": DBString(unique=True, visibility=DBFieldVisibility.User),
            "port": DBInteger(visibility=DBFieldVisibility.User),
            "count": DBInteger(default_factory=lambda: 0),
            "password": DBString(builder=lambda password: cls.hash_password(config, password), visibility=DBFieldVisibility.Invisible),
            "token": DBString(default_factory=lambda: str(uuid.uuid4()).replace("-", ""), visibility=DBFieldVisibility.Admin),
        }

    @classmethod
    def from_dict(cls, config: ConfigModule, dict: Dict[str, Any]) -> "ServerObject":
        return ServerObject(**cls.sanitize_dict(config, dict))
