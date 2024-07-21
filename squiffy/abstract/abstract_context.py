from typing import Union
from abc import ABC, abstractmethod

from squiffy import signals


class AbstractContext(ABC):
    @abstractmethod
    def handle_signal(
        self,
        signal: Union[
            signals.OK, signals.Do, signals.Abort, signals.Error, signals.Quit
        ],
    ) -> None: ...
    @abstractmethod
    def master(self) -> None:
        pass
