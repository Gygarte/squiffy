from traceback import format_exc
from typing import Union
from . import executor
from squiffy import signals
from squiffy.abstract import abstract_application, abstract_context


class Context(abstract_context.AbstractContext):
    """
    The purpose of the Context class is to match signals comming from the
    menu (and subsequently from the items in each Submenu) to the callback functions
    contained in the executors.


    """

    def __init__(self, application: abstract_application.AbstractApplication) -> None:
        self._application: abstract_application.AbstractApplication = application
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
                self._application.handle_ok(signal)

            elif isinstance(signal, signals.Abort):
                self._application.handle_abort(signal)

            elif isinstance(signal, signals.Error):
                self._application.handle_errors(signal)

            elif isinstance(signal, signals.Quit):
                self._application.handle_quit(signal)

        except Exception:
            self._application.handle_errors(
                signals.Error(
                    origin="Context",
                    log_message="An error occured during signal handling",
                    traceback=format_exc(),
                )
            )

    def _handle_do_event(self, signal: signals.Do) -> None:
        state = self._application.provide_state()
        # If the selected option does not have a callback function attached to it
        # it should do nothing when selected. So the error raised by failing
        # to find the executor will be ignored.
        try:
            self._executors[signal.signal].execute(signal, state)
        except KeyError:
            pass

    @property
    def master(self) -> abstract_application.AbstractApplication:
        return self._application

    @master.setter
    def master(self, master: abstract_application.AbstractApplication) -> None:
        self._application = master

    @property
    def executors(self) -> dict[signals.Do, executor.Executor]:
        return self._executors

    @executors.setter
    def executors(self, executor: executor.Executor) -> None:
        executor.context = self
        self._executors.update({executor.signal: executor})
