from typing import Optional
from squiffy.abstract import abstract_state
from squiffy.errors import StateContentNotSavable


# TODO: Should add a method for checking that the value in the init dict or payload is not a buildin type?
class State(abstract_state.AbstractState):
    def __init__(
        self,
        init: Optional[dict[str, object]] = None,
        save_except: list[str] | None = None,
    ) -> None:
        """
        The State could be initialized with a custom state
        (ex. from a settings file) or empty.

        Args:
            init (Optional[dict[str, object]], optional): The initial state. Defaults to None.
        """
        self._save_except = save_except

        if init is not None:
            self._state_content_precheck(init)

            self._state = init

        else:
            self._state: dict[str, object] = dict({})

    def update(self, value_dict: dict[str, object]) -> None:
        self._state.update(value_dict)

    def save(self) -> None:
        # Except form saving when the state is empty
        if len(self._state) == 0:
            return None
        for value_name, value in self._state.items():
            # Ignore the values that are excepted from saving
            if self._save_except is not None and value_name in self._save_except:
                continue
            elif hasattr(value, "save_except") and value.save_except:
                continue
            else:
                try:
                    value.save()
                except AttributeError:
                    pass

    def get(self, value_name: str) -> object:
        return self._state.get(value_name)

    def _state_content_precheck(self, init: dict) -> None:
        """
        Checks that all the values in the state content are savable.

        In order to except some object from this check - in the case when the
        save method is not necessary - the object is checked for "save_except" attribute,
        or if the name of the object is in the save_except list.


        """

        for value_name, values in init.items():
            # Chacking the save except
            if self._save_except is not None and value_name in self._save_except:
                continue

            # Checking the object for the save_except attribute
            elif hasattr(values, "save_except") and values.save_except:
                continue

            elif not hasattr(values, "save"):
                raise StateContentNotSavable(f"State content {values} is not savable.")
