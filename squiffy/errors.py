class CallbackNotAttachedError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class NoneSignalRaisedError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
