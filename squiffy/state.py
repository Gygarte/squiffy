from squiffy.abstract import abstract_state


class State(abstract_state.AbstractState):
    def __init__(self) -> None:
        self._state: dict[str, object] = dict({})

    def load(self, payload: dict[str, object]) -> None:
        self._state.update(payload)

    def save(self) -> None:
        try:
            for state_name, state_info in self._state.items():
                state_info.save()
        except AttributeError:
            pass
        else:
            return

    def get(self, state_name: str) -> object:
        return self._state.get(state_name)
