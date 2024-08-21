import unittest
import unittest.mock
from squiffy import Application
from squiffy.context import executor
from squiffy import signals
from squiffy.layout import layout_factory


class TestApplication(unittest.TestCase):
    _mock_state = unittest.mock.Mock()
    _mock_layout = unittest.mock.Mock(spec_set=layout_factory.LayoutFactory)

    _application = Application(layout=_mock_layout, state=_mock_state)
    _application._menu = unittest.mock.Mock()

    def test_run_under_KeyboardInnterrupt_or_EOFError(self):
        # Test if the run function sets _running to False when KeyboardInterrupt is raised
        self._application._menu.is_running = True
        self._application._menu.show.side_effect = KeyboardInterrupt()
        self._application.run()
        self.assertFalse(self._application._running)

        self._application._menu.show.side_effect = EOFError()
        self._application.run()
        self.assertFalse(self._application._running)

    def test_saving_state_when_quit(self) -> None:
        # Test if the run function saves the state when _running is False
        self._application._menu.is_running = False
        self._application.run()
        self.assertEqual(self._application._state.save.call_count, 1)

    def test_add(self):
        # Test if the add function adds an executor to the context
        self._application.add(
            function=unittest.mock.Mock(), option_name="option", submenu_name="submenu"
        )
        self.assertEqual(len(list(self._application._context.executors.values())), 1)

        # Assert if the executor is of type Executor
        self.assertIsInstance(
            list(self._application._context.executors.values())[0], executor.Executor
        )

    def test_handle_errors(self):
        # Test if the handle_errors function calls the menu's handle_errors function
        self._application.handle_errors(signals.Error())
        self._application._menu.handle_errors.assert_called_once()

    def test_handle_ok(self):
        # Test if the handle_ok function updates the state with the payload
        self._application.handle_ok(signals.OK(payload={"key": "value"}))
        self._application._state.update.assert_called_once_with({"key": "value"})

        # Test if the handle_ok function does not update the state when the payload is empty
        self._application.handle_ok(signals.OK())
        self.assertEqual(self._application._state.update.call_count, 1)

    def test_handle_quit(self):
        pass

    def test_handle_abort(self):
        # Test if the handle_abort function does not raise an error
        try:
            self._application.handle_abort(signals.Abort())
        except Exception:
            self.fail("handle_abort method raised an error")

    def test_custom_abort_handler(self):
        # Test if the handle_abort function calls the custom abort handler
        self._application._abort_handler = unittest.mock.Mock()
        self._application.handle_abort(signals.Abort())
        self._application._abort_handler.assert_called_once()

    def test_provide_state(self):
        pass

    def test__save_state(self):
        pass
