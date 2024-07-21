from typing import Union
from traceback import format_exc
from .submenu import Submenu
from squiffy.abstract.abstract_menu import AbstractMenu, AbstractMenuObserversLayer
from squiffy.abstract import abstract_context
from squiffy import signals


class Menu(AbstractMenu):
    def __init__(
        self,
        submenu: list[Submenu],
        main_submenu_idx: int,
        error_submenu: Submenu | None = None,
    ) -> None:
        self._running: bool = True

        self._context: Union[
            abstract_context.AbstractContext, AbstractMenuObserversLayer, None
        ] = None

        self._submenu: list[Submenu] = submenu
        self._submenu_tree: dict[str, int] = dict({})
        self._set_submenu_master_menu()
        self._update_menu_tree()

        # in order to handle an error, the user should provide an error submenu
        # that will be displayed when an error occurs
        self._error_submenu: Submenu | None = error_submenu
        self._error_submenu.master_menu = self

        # the current submenu is the one that is currently displayed
        # is setted by the user at the creation of the menu class
        self._current_submenu: Submenu = self._submenu[main_submenu_idx]

        # the root submenu is the one that is the starting point of the
        # submenues interaction
        self._root_submenu: Submenu = self._submenu[main_submenu_idx]

        # keeps the order of the submenus
        self._submenu_order: list[Submenu, None] = [self._current_submenu]

    def show(self) -> None:
        """
        This method is the entry point of the menu.

        It is inteded to run the menu continuously as long as no context is provided.
        """

        self._show()

    def _show(self) -> None:
        # shows the items in the menu
        try:
            self._current_submenu.show()
        except Exception:
            self.handle_errors(
                signals.Error(
                    origin=self._current_submenu.uid,
                    log_message="An error occurred while trying to show the submenu",
                    traceback=format_exc(),
                )
            )

    def handle_errors(self, error: signals.Error) -> None:
        self._error_submenu.show(error)

    def handle_signals(
        self,
        signal: Union[
            signals.OK,
            signals.Do,
            signals.SwitchSubmenu,
            signals.ReturnToMain,
            signals.ReturnToPrevious,
            signals.Quit,
            signals.Abort,
            signals.Error,
        ],
    ) -> None:
        """
        Handles a signal that is triggered in a submenu and
        propagates it to the context.

        """
        #
        if isinstance(signal, signals.SwitchSubmenu):
            self._change_submenu(signal.target_id)

        elif isinstance(signal, signals.Error):
            self.handle_errors(signal)

        elif isinstance(signal, signals.Quit):
            self._quit()

        elif isinstance(signal, signals.ReturnToPrevious):
            self._return_to_previous()

        elif isinstance(signal, signals.ReturnToMain):
            self._return_to_main()

        elif isinstance(signal, signals.OK) or isinstance(signal, signals.Do):
            self._handle_ok_do_signal(signal)

        elif isinstance(signal, signals.Abort):
            pass

    def _handle_ok_do_signal(self, signal: signals.OK) -> None:
        if self._context is not None:
            if isinstance(self._context, AbstractMenuObserversLayer):
                self._context.send(signal)

            elif isinstance(self._context, abstract_context.AbstractContext):
                self._context.handle_signal(signal)
        else:
            self.handle_errors(
                signals.Error(
                    origin=self._current_submenu.uid,
                    log_message="No context was detected",
                    traceback=None,
                )
            )

    def _return_to_previous(self) -> None:
        # returns to the previous submenu
        if len(self._submenu_order) == 1:
            self._current_submenu = self._root_submenu
        else:
            # remove the current submenu form the list
            # and initialize the last submenu in the list
            self._submenu_order.pop()
            self._current_submenu = self._submenu_order[-1]

    def _return_to_main(self) -> None:
        # returns to the main submenu
        self._current_submenu = self._root_submenu

    def _quit(self) -> None:
        self._running = False

    def _update_menu_tree(self) -> None:
        for index, submenu in enumerate(self._submenu):
            self._submenu_tree.update({submenu.uid: index})

    def _change_submenu(self, target: str) -> None:
        try:
            target_idx = self._submenu_tree.get(target)
        except KeyError:
            self.handle_errors(
                signals.Error(
                    origin=self._current_submenu.uid,
                    log_message="InvalidTargetError",
                    traceback=None,
                )
            )
            return

        else:
            try:
                self._current_submenu = self._submenu[target_idx]
            except TypeError:
                self.handle_errors(
                    signals.Error(
                        origin=self._current_submenu.uid,
                        log_message="InvalidTargetError",
                        traceback=None,
                    )
                )
                return
            else:
                self._submenu_order.append(self._current_submenu)

    def _set_submenu_master_menu(self) -> None:
        for submenu in self._submenu:
            submenu.master_menu = self

    @property
    def controller(self):
        return self._context

    @controller.setter
    def controller(self, ctrl) -> None:
        self._context = ctrl

    @property
    def is_running(self) -> bool:
        return self._running
