from squiffy.abstract.abstract_menu import AbstractObserver
from squiffy import signals
from typing import Callable, Any, Union
from squiffy.abstract import abstract_context


class EventObserver(AbstractObserver):
    def __init__(
        self,
        event_type: signals.Signal | str,
        callback: Callable[
            ..., signals.OK | signals.Abort | signals.Error | signals.Quit
        ]
        | None = None,
        *args,
        **kwargs,
    ) -> None:
        self._event_type = event_type
        self._callback = callback
        self._context: abstract_context.AbstractContext = None
        self._args = args
        self._kwargs = kwargs

    def inform(
        self,
        event: Union[
            signals.Abort, signals.Error, signals.Quit, signals.Do, signals.OK
        ],
    ) -> Union[signals.Abort, signals.OK, signals.Error, signals.Quit]:
        """
        The observer responds with an action when the
        user selects an option in the main menu (which holds
        all possible options).

        The response of the callback function is forwarded to
        the context.

        In case of an error, abort of callback operation or quit
        the context will handle it.

        If no callback is provided, the event will be forwarded
        to the context.
        """
        if self._callback is None:
            # the signals will be forwarded towards the context
            self._context.handle_signal(event)
        else:
            if isinstance(event, signals.Do) and (event.signal == self._event_type):
                self._context.handle_signal(self._callback(*self._args, **self._kwargs))
                return
            elif (
                isinstance(event, signals.Error)
                or isinstance(event, signals.Abort)
                or isinstance(event, signals.Quit)
            ):
                self._context.handle_signal(event)
                return

    @property
    def context(self) -> Any:
        return self._context

    @context.setter
    def context(self, context: Any) -> None:
        self._context = context


class ExecutorObserver(AbstractObserver):
    """
    The executor type of observers respond to an event by evecuting
    a callback function. The callback function is expected to return
    an event which will be forwarded to the context.

    Usually the return value of the callback function is and OK Event.

    Args:
        Observer (_type_): _description_
    """

    def __init__(
        self,
        signal_type: signals.Signal,
        callback: Callable[
            ..., signals.OK | signals.Abort | signals.Error | signals.Quit
        ],
        *args,
        **kwargs,
    ) -> None:
        self._signal_type = signal_type
        self._callback = callback
        self._context: abstract_context.AbstractContext = None
        self._args = args
        self._kwargs = kwargs

    def inform(
        self,
        event: Union[
            signals.Abort, signals.Error, signals.Quit, signals.Do, signals.OK
        ],
    ) -> Union[signals.Abort, signals.OK, signals.Error, signals.Quit]:
        """
        The observer responds with an action when the
        user selects an option in the main menu (which holds
        all possible options).

        The response of the callback function is forwarded to
        the context.

        In case of an error, abort of callback operation or quit
        the context will handle it.
        """
        if isinstance(event, signals.Do) and (event.signal == self._signal_type):
            self._context.handle_signal(self._callback(*self._args, **self._kwargs))
            return
        elif (
            isinstance(event, signals.Error)
            or isinstance(event, signals.Abort)
            or isinstance(event, signals.Quit)
        ):
            self._context.handle_signal(event)
            return

    @property
    def context(self) -> Any:
        return self._context

    @context.setter
    def context(self, context: Any) -> None:
        self._context = context


class RoutingObserver(AbstractObserver):
    def __init__(self, signal: str) -> None:
        self._signal = signal
        self._context: abstract_context.AbstractContext = None

    def inform(
        self,
        signal: Union[
            signals.Abort, signals.Error, signals.Quit, signals.Do, signals.OK
        ],
    ) -> Union[signals.Abort, signals.OK, signals.Do, signals.Error, signals.Quit]:
        if isinstance(signal, signals.Do) and (signal.signal == self._signal):
            self._context.handle_signal(signal)
            return
        elif (
            isinstance(signal, signals.Error)
            or isinstance(signal, signals.Abort)
            or isinstance(signal, signals.Quit)
        ):
            self._context.handle_signal(signal)

    @property
    def context(self) -> Any:
        return self._context

    @context.setter
    def context(self, context: Any) -> None:
        self._context = context
