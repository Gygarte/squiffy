import os
from squiffy.abstract import abstract_style
from squiffy.abstract import abstract_menu


class Screen(abstract_style.AbstractScreen):
    def __init__(self) -> None:
        self._screen_hight: int | None = None
        self._screen_width: int | None = None

        # self._content:abstract_menu.AbstractMenu = None

    def display(self) -> None:
        pass

    def get_screen_size(self) -> None:
        screen_size = os.get_terminal_size()
        self._screen_hight = screen_size.lines
        self._screen_width = screen_size.columns

    def async_get_sceen_size(self):
        pass

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
        return self._content

    @menu.setter
    def menu(self, content: abstract_menu.AbstractMenu) -> None:
        self._content = content
