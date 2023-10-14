from abc import ABC, abstractmethod

class AbstractValidator(ABC):

    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def validate(self, data):
        return ("Not implemented")

    @abstractmethod
    def initialize_validator(self, main_schema, definitions):
        return ("Not implemented")

    @abstractmethod
    def errors(self, data):
        return ("Not implemented")