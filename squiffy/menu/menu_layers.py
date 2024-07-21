from typing import Union
from .menu import Menu
from squiffy.abstract.abstract_menu import AbstractObserver, AbstractMenuObserversLayer
from squiffy import signals


class MenuObserversLayer(AbstractMenuObserversLayer):
    def __init__(self, menu: Menu) -> None:
        self._menu: Menu = menu
        self._menu.controller = self

        self._observers: list[AbstractObserver] = list([])

    def attach(self, observer: AbstractObserver) -> None:
        self._observers.append(observer)

    def detach(self, observer: AbstractObserver) -> None:
        self._observers.remove(observer)

    def send(
        self,
        event: Union[
            signals.OK, signals.Do, signals.Quit, signals.Abort, signals.Error
        ],
    ) -> None:
        """
        This method does the routing of various events to the
        observers.

        """

        if isinstance(event, signals.OK) or isinstance(event, signals.Do):
            for observer in self._observers:
                observer.inform(event)

        elif (
            isinstance(event, signals.Quit)
            or isinstance(event, signals.Abort)
            or isinstance(event, signals.Error)
        ):
            for observer in self._observers:
                observer.inform(event)

    def handle_errors(self, error: signals.Error) -> None:
        self._menu.handle_errors(error)

    def run(self) -> None:
        self._menu.show()

    def is_running(self) -> bool:
        return self._menu.is_running
