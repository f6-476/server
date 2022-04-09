from typing import TYPE_CHECKING, List, Type, TypeVar

if TYPE_CHECKING:
    from .module import Module

T = TypeVar("T")
class App:
    __modules: List["Module"]

    def __init__(self):
        self.__modules = []

    def run(self):
        for module in self.__modules:
            module.run()

    def load_module(self, type: Type[T]) -> T:
        for module in self.__modules:
            if isinstance(module, type):
                return module

        raise Exception(f"Module {type} not loaded.")

    def register_module(self, type: Type["Module"], **kwargs):
        kwargs["app"] = self
        module = type(**kwargs)
        self.__modules.append(module)
