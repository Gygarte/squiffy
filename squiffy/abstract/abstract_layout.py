from abc import ABC, abstractmethod


class AbstractLayoutFactory(ABC):
    
    @abstractmethod
    def create(self):
        pass
    
    