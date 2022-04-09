from ..app import App
from ..module import Module

class ConfigModule(Module):
    __debug: bool

    def __init__(self, app: App, debug: bool=False):
        self.__debug = debug
    
    @property
    def debug(self) -> bool:
        return self.__debug
