import abc


class ITypeRecognizer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def type(self, value) -> type:
        pass

    @abc.abstractmethod
    def default_type(self) -> type:
        pass

    @abc.abstractmethod
    def convert(self, value):
        pass
