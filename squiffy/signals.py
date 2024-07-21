from abc import ABC


class Signal(ABC): ...


class OK(Signal):
    """
    A class to represent an OK event.

    The OK event is used to signal that an operation was successful
    and to return the result of the operation.

    Args:
        origin (str): The function that originated the event/ did the
        operation.
        payload (Any): The result of the function operation.


    """

    def __init__(
        self, origin: str | None = None, payload: dict[str, object] | None = None
    ) -> None:
        self.origin = origin
        self.payload = payload

    def is_payload(self) -> bool:
        return self.payload is not None


class Do(Signal):
    """
    A class to represent a Do event.

    The Do event is used to signal that an operation should be done.

    The Do event is handled by a context in which the Menu resides.
    The Menu should not implement any responses to the Do event, other
    than routing it to the appropriate context.

    Args:
        signal_type (str): The type of signal to be sent, representing the
        operation to be done.


    """

    def __init__(self, signal: str) -> None:
        self.signal = signal


class Error(Signal):
    def __init__(
        self,
        origin: str | None = None,
        log_message: str | None = None,
        traceback: str | None = None,
    ) -> None:
        self.origin = origin
        self.log_message = log_message
        self.traceback = traceback


class Abort(Signal):
    def __init__(
        self, origin: str | None = None, log_message: str | None = None
    ) -> None:
        self.origin = origin
        self.log_message = log_message


class Quit(Signal):
    def __init__(
        self, origin: str | None = None, log_message: str | None = None
    ) -> None:
        self.origin = origin
        self.log_message = log_message


class ReturnToMain(Signal): ...


class ReturnToPrevious(Signal): ...


class SwitchSubmenu(Signal):
    def __init__(self, target_id: str) -> None:
        self.target_id = target_id
