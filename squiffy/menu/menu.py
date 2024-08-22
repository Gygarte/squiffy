import os
import sys
import queue
import time
import asyncio
from threading import Thread, Event
from pynput import keyboard
from typing import Union
from traceback import format_exc
from .submenu import Submenu
from squiffy.abstract.abstract_menu import AbstractMenu, AbstractMenuObserversLayer
from squiffy.abstract import abstract_context
from squiffy import signals
from squiffy.layout.constants import FRAME_RATE
from prompt_toolkit import PromptSession


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

        # Create threads periodically measure screen size
        if self._current_submenu.style.autoscale:
            self._create_helper_thread()
            self._autoscale = True
        else:
            self._autoscale = False

        # State variables. The _init variable permint the screen to be initialized when the
        # application starts. The _refresh variable is used to refresh the screen when the user
        # changes the screen dimensions.
        self._init: bool = True
        self._refresh: bool = False
        self._loop = None

    def show(self) -> None:
        # shows the items in the menu
        try:
            if self._autoscale:
                self._async_show_ui()
            else:
                self._current_submenu.show()

        except Exception:
            self.handle_errors(
                signals.Error(
                    origin=self._current_submenu.uid,
                    log_message="An error occurred while trying to show the submenu",
                    traceback=format_exc(),
                )
            )

    def _async_show_ui(self):
        if not self._size_queue.empty():
            size = self._size_queue.get()
            self._current_submenu.update_screen_size(
                hight=size.lines, width=size.columns
            )
            self._refresh = True
            # The event is reset when accepting user input is not possible due to
            # redrawing the menu.
            self._event.clear()

        if self._init or self._refresh:
            self._refresh = False
            self._init = False
            # We clear all the content that could get to the screen
            self._clear_screen()
            # The resized submenu is redrawn to the screen
            self._current_submenu.show()
        if self._loop is None:
            try:
                loop = asyncio.get_running_loop()
                option = loop.run_until_complete(self._show_prompt)
            except RuntimeError:
                loop = asyncio.new_event_loop()
                option = loop.run_until_complete(self._show_prompt())
        if option is not None:
            self._current_submenu._emit_signal_from_selection(int(option))

    async def _show_prompt(self):
        session = PromptSession()
        option = await session.prompt_async("Make a selection:")
        return option

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
                self._refresh = True

    def _set_submenu_master_menu(self) -> None:
        for submenu in self._submenu:
            submenu.master_menu = self

    def set_submenu_size(self, hight: int, width: int) -> None:
        self._current_submenu.update_screen_size(hight, width)

    @staticmethod
    def _get_terminal_size(queue: queue.Queue, event: Event) -> None:
        initial_size = os.get_terminal_size()
        while True:
            current_size = os.get_terminal_size()
            if current_size.lines != initial_size.lines or (
                current_size.columns != initial_size.columns
            ):
                queue.put(current_size)
                initial_size = current_size

            time.sleep(FRAME_RATE)

    @staticmethod
    def _show_input_prompt() -> None:
        sys.stdout.write("Select an option:")
        sys.stdout.flush()

    def _get_user_input(self) -> None:
        # Display the user input
        if not self._input_queue.empty():
            key = self._input_queue.get()

            try:
                if key.char.isdigit():
                    self._user_input = int(key.char)
                    sys.stdout.write(key.char)
                    sys.stdout.flush()
            except AttributeError:
                pass

            if key == keyboard.Key.enter:
                self._current_submenu._emit_signal_from_selection(self._user_input)
                self._user_input = None
            elif key == keyboard.Key.backspace:
                sys.stdout.write("\b \b")
                sys.stdout.flush()

    def _create_helper_thread(self) -> None:
        self._event = Event()
        self._size_queue = queue.Queue(maxsize=1)

        self._size_thread = Thread(
            target=self._get_terminal_size,
            args=(self._size_queue, self._event),
            daemon=True,
        )

        self._size_thread.start()

    @staticmethod
    def _clear_screen() -> None:
        sys.stdout.flush()
        os.system("cls")

    @property
    def controller(self):
        return self._context

    @controller.setter
    def controller(self, ctrl) -> None:
        self._context = ctrl

    @property
    def is_running(self) -> bool:
        return self._running
