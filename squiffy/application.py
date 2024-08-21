import os
import time
import queue
from threading import Thread, Event
from traceback import format_exc
from typing import Callable
from .abstract import abstract_application
from .layout import layout_factory
from .state import State
from . import utils, signals
from squiffy.context import context, executor
from squiffy.layout.constants import FRAME_RATE


class Application(abstract_application.AbstractApplication):
    def __init__(
        self,
        layout: str | layout_factory.LayoutFactory = "layout.json",
        state: State | None = None,
        abort_handler: Callable | None = None,
    ) -> None:
        # Layout setting
        if isinstance(layout, layout_factory.LayoutFactory):
            self._layout = layout
        elif isinstance(layout, str) and layout not in "layout.json":
            self._layout = layout_factory.LayoutFactory
        else:
            self._layout = layout_factory.LayoutFactory(layout)

        # Menu setting
        self._menu = self._layout.create()
        self._context = context.Context(application=self)
        self._menu._context = self._context

        # States and internal variables
        self._running: bool = True
        self._init = True
        self._refresh = False

        self._event = Event()
        self._size_queue = queue.Queue(maxsize=1)
        self._input_queue = queue.Queue(maxsize=1)

        self._size_thread = Thread(
            target=self._get_terminal_size,
            args=(self._size_queue, self._event),
            daemon=True,
        )
        self._input_thread = Thread(
            target=self._get_user_input,
            args=(self._input_queue, self._event),
            daemon=True,
        )
        self._size_thread.start()
        self._input_thread.start()

        if state is None:
            self._state = State()
        else:
            self._state: State = state

        # Other mechanism
        if abort_handler is not None:
            self._abort_handler = abort_handler

    def run(self) -> None:
        while self._running:
            try:
                if not self._size_queue.empty():
                    size = self._size_queue.get()
                    self._menu.set_submenu_size(hight=size.lines, width=size.columns)
                    self._refresh = True

                    # The event is reset when accepting user input is not possible due to
                    # redrawing the menu.
                    self._event.clear()

                if self._init or self._refresh:
                    self._menu.show()
                    self._running = self._menu.is_running
                    self._init = False
                    self._refresh = False

                    # The event is set when accepting input from user is possible.
                    self._event.set()
                    # The event is cleared so that the user input thread will stop after taking an input from the user.
                    # This prevents the thread to continue spanning the input action and block the execution of other functions.
                    # The delay is intended to give the thread the opportunity to execute the function at leat oance, until it
                    # get stuck in the input action await behaivour.
                    # At least that is the idea.
                    # TODO: implement the logic for error handling in the input thread.
                    time.sleep(0.1)
                    self._event.clear()

                # Check if the user has provided input
                if not self._input_queue.empty():
                    self._menu._current_submenu._emit_signal_from_selection(
                        self._input_queue.get()
                    )
                    self._refresh = True

                if self._running is False:
                    self._save_state()

            except KeyboardInterrupt or EOFError:
                self.handle_quit()

    def add(self, function: Callable, option_name: str, submenu_name: str) -> None:
        # Create rounting observers and Executors for the signal signature and the function
        signal_signature: str = utils.generate_signal_name(submenu_name, option_name)
        exe = executor.Executor(signals.Do(signal_signature), function)

        self._context.executors = exe

    def handle_errors(self, error: signals.Error) -> None:
        # self._save_state()
        self._menu.handle_errors(error)

    def handle_ok(self, signal: signals.OK) -> None:
        if signal.is_payload():
            self._state.update(signal.payload)

    def handle_quit(self) -> None:
        os.system("cls")
        self._running = False
        self._save_state()

    def handle_abort(self, signal: signals.Abort) -> None:
        if isinstance(signal, signals.Abort):
            if hasattr(self, "_abort_handler"):
                self._abort_handler(signal)
        else:
            raise ValueError("Signal is not an instance of signals.Abort")

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
    def _get_user_input(queue: queue.Queue, event: Event) -> None:
        while True:
            if event.is_set():
                option: int = int(input("Select an option: "))
                queue.put(option)

    def provide_state(self):
        return self._state

    def _save_state(self) -> None | signals.Error:
        try:
            self._state.save()
        except Exception:
            self.handle_errors(
                signals.Error(
                    origin="Application",
                    log_message="An error occured during state saving",
                    traceback=format_exc(),
                )
            )
