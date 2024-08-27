class CallbackNotAttachedError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class NoneSignalRaisedError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class StateContentNotSavable(Exception):
    """
    An exception raised when the content of the state is not savable,
    due to not containing an 'save' method.

    """

    def __init__(self, message: str):
        super().__init__(message)
