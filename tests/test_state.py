import unittest
from unittest.mock import Mock
from squiffy.state import State
from squiffy.errors import StateContentNotSavable


class TestValue:
    ...

    def save(self) -> str:
        return "Saved"


class TestValue2:
    save_except = False


class TestState(unittest.TestCase):
    _test_value: object = TestValue()
    _init_state = Mock()
    _second_state = Mock()
    _second_state.save_except = True

    def test_init(self):
        state = State()
        self.assertEqual(state._state, {})

    def test_init_with_state(self):
        state = State({"key": self._test_value})
        self.assertEqual(state._state, {"key": self._test_value})

    def test_update(self):
        state = State()
        state.update({"key": self._test_value})
        self.assertEqual(state._state, {"key": self._test_value})

    def test_save_empty_state(self):
        state = State()
        state.save()
        self.assertEqual(state.save(), None)

    def test_save_an_excepted_state(self) -> None:
        state = State({"key": self._second_state}, save_except=["key"])
        self.assertEqual(self._second_state.save.call_count, 0)

    def test_get(self):
        state = State({"key": self._test_value})
        self.assertEqual(state.get("key"), self._test_value)

    def test_state_content_precheck(self):
        # Test excepting based on the save_except attribute
        state = State(init={"key": self._test_value}, save_except=["key"])
        self.assertEqual(state._state, {"key": self._test_value})

        # Test excepting based on the save_except field in the object
        self._init_state.save_except = True
        state = State({"key": self._init_state})
        self.assertEqual(state._state, {"key": self._init_state})

        # Test raising StateContentNotSavable exception when the save_except is
        # provided, and set to False and the object does not have the save method

        with self.assertRaises(StateContentNotSavable):
            state = State({"key": TestValue2()})

        # Test raising StateContentNotSavable exception when the object does not
        # have the save method
        with self.assertRaises(StateContentNotSavable):
            state = State({"key": "value"})


state = State({"key": TestValue()})
print(state.save())
