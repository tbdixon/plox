import abc


class LoxCallable(abc.ABC):
    @abc.abstractmethod
    def call(self, *args):
        pass

    @abc.abstractmethod
    def arity(self) -> int:
        pass
