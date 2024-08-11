from traceback import format_exc
from typing import Callable, Union
from squiffy.abstract import abstract_context
from squiffy import signals


class Executor:
    def __init__(
        self,
        signal: signals.Do,
        callback: Callable[
            ..., Union[signals.OK, signals.Error, signals.Abort, signals.Quit]
        ],
    ) -> None:
        self._signal = signal
        self._callback = callback

        self._context: abstract_context.AbstractContext | None = None

    def execute(self, signal: signals.Do, state) -> None:
        try:
            self._context.handle_signal(self._callback(state))
        except Exception:
            self._context.handle_signal(
                signals.Error(
                    origin=self._signal.signal,
                    log_message=f"""An error occurred while trying to execute the option.
                                                      Traceback: {format_exc()}""",
                    traceback=format_exc(),
                )
            )

    @property
    def context(self) -> abstract_context.AbstractContext:
        return self._context

    @context.setter
    def context(self, context: abstract_context.AbstractContext) -> None:
        self._context = context

    @property
    def signal(self) -> str:
        return self._signal.signal
