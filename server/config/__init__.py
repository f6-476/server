import bcrypt

from ..app import App
from ..module import Module

class ConfigModule(Module):
    __debug: bool
    __salt: bytes
    __host: str
    __port: int

    def __init__(self, app: App, debug: bool=False, salt: bytes=None, host: str="0.0.0.0", port=13337):
        if salt == None:
            salt = bcrypt.gensalt()

        self.__debug = debug
        self.__salt = salt
        self.__host = host
        self.__port = port

    @property
    def debug(self) -> bool:
        return self.__debug

    @property
    def salt(self) -> bytes:
        return self.__salt

    @property
    def host(self) -> str:
        return self.__host

    @property
    def port(self) -> str:
        return self.__port
