from dataclasses import dataclass, field
import bcrypt

from ..app import App
from ..module import Module

class ConfigModule(Module):
    __debug: bool
    __salt: bytes

    def __init__(self, app: App, debug: bool=False, salt: bytes=None):
        if salt == None:
            salt = bcrypt.gensalt()

        self.__debug = debug
        self.__salt = salt

    @property
    def debug(self) -> bool:
        return self.__debug

    @property
    def salt(self) -> bytes:
        return self.__salt
