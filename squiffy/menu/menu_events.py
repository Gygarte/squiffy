from squiffy import signals


class SwitchSubmenu(signals.Signal):
    def __init__(self, target: str) -> None:
        self.target = target

    def __repr__(self) -> str:
        return f"GoTo({self.target})"


class ReturnToPrevious(signals.Signal): ...


class ReturnToMain(signals.Signal): ...
