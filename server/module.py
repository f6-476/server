from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .app import App

class Module(ABC):
    def __init__(self, app: "App"):
        pass

    def run(self):
        pass
