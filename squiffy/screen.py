import os
import queue
import time
from threading import Event, Thread
from squiffy.abstract import abstract_style
from squiffy.abstract import abstract_menu


def get_terminal_size(queue: queue.Queue, event: Event) -> None:
    while not event.is_set():
        queue.put(os.get_terminal_size())

        # Sleep for 1 second
        time.sleep(1)


class Screen(abstract_style.AbstractScreen):
    def __init__(self) -> None:
        screen_size = os.get_terminal_size()
        self._screen_hight: int = screen_size.lines
        self._screen_width: int = screen_size.columns

        # The screen should update the screen size in a separate thread
        self._queue = queue.Queue(maxsize=10)
        self._event = Event()
        self._thread = Thread(
            target=get_terminal_size, args=(self._queue, self._event), daemon=True
        )
        self._thread.start()

    def display(self) -> None:
        self._menu.show()
        self.async_set_screen_size()

    def get_screen_size(self) -> None:
        pass

    def async_set_screen_size(self):
        screen_size = self._queue.get()

        if (
            self._screen_hight != screen_size.lines
            or self._screen_width != screen_size.columns
        ):
            self._screen_hight = screen_size.lines
            self._screen_width = screen_size.columns

            self._menu.update_screen_size(self._screen_hight, self._screen_width)
            self._menu.show()

    def stop(self) -> None:
        self._thread.join()
        os.system("clr")

    @property
    def hight(self) -> int:
        self.get_screen_size()

        return self._screen_hight

    @property
    def width(self) -> int:
        self.get_screen_size()

        return self._screen_width

    @property
    def menu(self) -> abstract_menu.AbstractMenu:
        return self._menu

    @menu.setter
    def menu(self, menu: abstract_menu.AbstractMenu) -> None:
        self._menu = menu

    @property
    def is_running(self) -> bool:
        return self._menu.is_running
