from abc import ABC, abstractmethod


class Field(ABC):

    def __init__(self, value):
        self.value = value

    @abstractmethod
    def is_valid(self, value):
        pass

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if self.is_valid(value):
            self.__value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)
