from abc import ABC, abstractmethod

class AbstractApplication(ABC):
    
    @abstractmethod
    def run(self) -> None:
        pass
    
    @abstractmethod
    def add(self) -> None:
        """
        This methods adds a function to an option
        in the application layout.
        """
        
        pass
    
    @abstractmethod
    def handle_errors(self) -> None:
        pass
    
    @abstractmethod
    def handle_ok(self) -> None:
        pass
    
    @abstractmethod
    def handle_quit(self) -> None:
        pass
    
    @abstractmethod
    def handle_abort(self) -> None:
        pass
    
    @abstractmethod
    def provide_state(self):
        pass
    
    