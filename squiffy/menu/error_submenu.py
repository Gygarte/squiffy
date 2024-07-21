from prompt_toolkit import prompt
from rich.pretty import pprint
from squiffy import utils
from squiffy import signals
from squiffy.abstract.abstract_menu import AbstractErrorSubmenu, AbstractMenu


class ErrorSubmenu(AbstractErrorSubmenu):
    def __init__(self, logger=None) -> None:
        self._options: dict[str, signals.Signal] = {
            "RETURN_TO_MAIN": signals.ReturnToMain(),
            "RETURN_TO_PREVIOUS": signals.ReturnToPrevious(),
            "QUIT": signals.Quit(),
        }

        self._options_tree: dict[int, signals.Signal] = dict({})
        self._update_options_tree()

        self._master_menu: AbstractMenu | None = None

        self._logger = logger

    def show(self, error: signals.Error) -> None:
        try:
            if self._logger is not None:
                pass
            else:
                print(error.log_message)
                print(error.traceback)
                pprint(self._options_tree, expand_all=True, indent_guides=False)

                option = self._show_prompt()
                self._propagate_option(option)

        except KeyboardInterrupt:
            self._master_menu.handle_signals(signals.Quit())
        except EOFError:
            self._master_menu.handle_signals(signals.Quit())

    def _show_prompt(self) -> None:
        option = int(
            prompt(
                ">> ",
                validator=utils._is_number_within_limits(
                    lower=0, upper=len(self._options_tree)
                ),
            )
        )

        return option

    def _propagate_option(self, option: str) -> None:
        option_name = self._options_tree.get(option)
        option_event = self._options.get(option_name)
        self._master_menu.handle_signals(option_event)

    def _update_options_tree(self) -> None:
        for index, option in enumerate(self._options):
            self._options_tree.update({index: option})

    @property
    def master_menu(self) -> AbstractMenu | None:
        return self._master_menu

    @master_menu.setter
    def master_menu(self, menu: AbstractMenu) -> None:
        self._master_menu = menu
