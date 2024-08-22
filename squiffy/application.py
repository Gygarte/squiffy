import os
from traceback import format_exc
from typing import Callable
from .abstract import abstract_application
from .layout import layout_factory
from .state import State
from . import utils, signals
from squiffy.context import context, executor


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
                self._menu.show()
                self._running = self._menu.is_running

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
