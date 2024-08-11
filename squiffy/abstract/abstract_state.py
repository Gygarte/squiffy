from abc import ABC, abstractmethod


class AbstractState(ABC):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def get(self):
        pass
