from abc import ABC, abstractmethod


class AbstractStyleFactory(ABC):
    @abstractmethod
    def create(self) -> str:
        pass


class AbstractScreen(ABC):
    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def get_screen_size(self):
        pass

    @abstractmethod
    def async_get_sceen_size(self):
        pass


class AbstractStyle(ABC):
    @abstractmethod
    def create(self) -> str:
        pass


class AbstractStyleHeader(ABC):
    pass


class AbstractStyleFooter(ABC):
    pass


class AbstractStyleContent(ABC):
    pass


class AbstractStyleHelp(ABC):
    pass


class AbstractStyleDisplay(ABC):
    pass


class AbstractStyleTable(ABC):
    pass


class AbstractPadding(ABC):
    @abstractmethod
    def top(self):
        pass

    @abstractmethod
    def bottom(self):
        pass

    @abstractmethod
    def left(self):
        pass

    @abstractmethod
    def right(self):
        pass
