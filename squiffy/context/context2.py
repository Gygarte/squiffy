from traceback import format_exc
from typing import Union
from . import executor
from squiffy import signals
from squiffy.abstract import abstract_application, abstract_context


class Context(abstract_context.AbstractContext):
    def __init__(self, master: abstract_application.AbstractApplication) -> None:
        self._master: abstract_application.AbstractApplication = master
        self._executors: dict[signals.Do, executor.Executor] = dict({})

    def handle_signal(
        self,
        signal: Union[
            signals.OK, signals.Do, signals.Abort, signals.Error, signals.Quit
        ],
    ) -> None:
        try:
            if isinstance(signal, signals.Do):
                self._handle_do_event(signal)

            elif isinstance(signal, signals.OK):
                self._master.handle_ok(signal)

            elif isinstance(signal, signals.Abort):
                self._master.handle_abort(signal)

            elif isinstance(signal, signals.Error):
                self._master.handle_errors(signal)

            elif isinstance(signal, signals.Quit):
                self._master.handle_quit(signal)

        except Exception:
            self._master.handle_errors(
                signals.Error(
                    origin="Context",
                    log_message="An error occured during signal handling",
                    traceback=format_exc(),
                )
            )

    def _handle_do_event(self, signal: signals.Do) -> None:
        state = self._master.provide_state()
        self._executors[signal.signal].execute(signal, state)

    @property
    def master(self) -> abstract_application.AbstractApplication:
        return self._master

    @master.setter
    def master(self, master: abstract_application.AbstractApplication) -> None:
        self._master = master

    @property
    def executors(self) -> dict[signals.Do, executor.Executor]:
        return self._executors

    @executors.setter
    def executors(self, executor: executor.Executor) -> None:
        executor.context = self
        self._executors.update({executor.signal: executor})
