from abc import ABC, abstractmethod

class AbstractState(ABC):
    
    @abstractmethod
    def load(self):
        pass
    
    @abstractmethod
    def save(self):
        pass
    
    @abstractmethod
    def get(self):
        pass