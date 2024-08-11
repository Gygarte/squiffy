from typing import Optional
from squiffy.abstract import abstract_state


# TODO: Should add a method for checking that the value in the init dict or payload is not a buildin type?
class State(abstract_state.AbstractState):
    def __init__(self, init: Optional[dict[str, object]] = None) -> None:
        """
        The State could be initialized with a custom state
        (ex. from a settings file) or empty.

        Args:
            init (Optional[dict[str, object]], optional): The initial state. Defaults to None.
        """

        if init is not None:
            self._state = init
        else:
            self._state: dict[str, object] = dict({})

    def update(self, value_dict: dict[str, object]) -> None:
        self._state.update(value_dict)

    def save(self) -> None:
        try:
            for value_name, value in self._state.items():
                value.save()
        except AttributeError:
            pass
        else:
            return None

    def get(self, value_name: str) -> object:
        return self._state.get(value_name)
