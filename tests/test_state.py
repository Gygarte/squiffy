import unittest
from squiffy.state import State


class TestValue:
    ...

    def save(self) -> str:
        return "Saved"


class TestState(unittest.TestCase):
    _test_value: object = TestValue()

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

    def test_get(self):
        state = State({"key": self._test_value})
        self.assertEqual(state.get("key"), self._test_value)


state = State({"key": TestValue()})
print(state.save())
