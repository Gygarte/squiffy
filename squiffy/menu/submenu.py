import os
from prompt_toolkit import prompt
from .menu_items import Item, ItemsCollection
from squiffy.abstract.abstract_menu import AbstractSubmenu, AbstractMenu
from squiffy import signals
from squiffy import utils
from squiffy.layout.style import Style


class Submenu(AbstractSubmenu):
    # encapsulate the logic of a submenu

    def __init__(
        self,
        title: str,
        items: ItemsCollection,
        style: Style | None = None,
        header_msg: str | None = None,
        footer_msg: str | None = None,
        logo: str | None = None,
        add_return: bool = True,
        add_return_to_main: bool = True,
        add_quit: bool = True,
    ) -> None:
        self._title = title
        self._items: ItemsCollection = items
        self._logo = logo

        self._style = style
        self._header_msg = header_msg
        self._footer_msg = footer_msg

        self._add_return = add_return
        self._add_return_to_main = add_return_to_main
        self._add_quit = add_quit
        self._create_return_or_quit_options()

        self._master_menu: AbstractMenu | None = None

    def show(self) -> None:
        try:
            self._show_ui()
            option = self._show_prompt()
        except KeyboardInterrupt:
            self.handle_signals(signals.Quit())
        except EOFError:
            self.handle_signals(signals.Quit())
        else:
            self._emit_signal_from_selection(option)

    def handle_signals(self, signal: signals.Signal) -> None:
        if signal is None:
            self._master_menu.handle_errors(
                error=signals.Error(
                    origin=self._title,
                    log_message="NoneSignalRaisedError",
                    traceback=None,
                )
            )
        elif isinstance(signal, signals.Error):
            self._master_menu.handle_errors(signal)
        else:
            self._master_menu.handle_signals(signal)

    def _show_ui(self) -> None:
        # Clear the console
        # TODO: Add support for a stilyzed console

        os.system("cls")

        if self._style is not None:
            style = self._style.create(
                title=self._title,
                subtitle="",
                header_msg=self._header_msg,
                content=self._items.items,
                footer_msg=self._footer_msg,
            )

            print(style)

        else:
            print(self._title)
            if self._logo is not None:
                print(self._logo)

            self._items.show()

    def _create_return_or_quit_options(self) -> None:
        if self._add_return:
            self._items.add_item(
                Item(
                    option="RETURN_TO_PREVIOUS",
                    help="Return to previous menu",
                    signal=signals.ReturnToPrevious(),
                )
            )

        if self._add_return_to_main:
            self._items.add_item(
                Item(
                    option="RETURN_TO_MAIN",
                    help="Return to main menu",
                    signal=signals.ReturnToMain(),
                )
            )

        if self._add_quit:
            self._items.add_item(
                Item(option="QUIT", help="Quit the application", signal=signals.Quit())
            )

    def _show_prompt(self) -> None:
        option = int(
            prompt(
                ">> ",
                validator=utils._is_number_within_limits(
                    lower=0, upper=len(self._items)
                ),
            )
        )

        return option

    def _emit_signal_from_selection(self, selection: int) -> None:
        event = self._items.get_item(selection).emit()

        self.handle_signals(event)

    @property
    def master_menu(self) -> AbstractMenu | None:
        return self._master_menu

    @master_menu.setter
    def master_menu(self, menu: AbstractMenu) -> None:
        self._master_menu = menu

    @property
    def uid(self) -> str:
        return self._title
