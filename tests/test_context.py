import unittest
import unittest.mock
from squiffy.context.context import Context
from squiffy import signals


class TestContext(unittest.TestCase):
    _mock_application = unittest.mock.Mock()
    _mock_executor = unittest.mock.Mock()
    _mock_executor.signal = "signal"

    _context = Context(_mock_application)
    _context.executors = _mock_executor

    def test_init(self):
        context = Context(self._mock_application)
        self.assertEqual(context._application, self._mock_application)
        self.assertEqual(context._executors, {})

        context.executors = self._mock_executor
        self.assertEqual(context._executors, {"signal": self._mock_executor})

    def test_handle_do_event_when_executor_not_found(self):
        # Test the case where the executor is not found - nothing should happen
        try:
            self._context._handle_do_event(signals.Do("not_signal"))
        except KeyError:
            self.fail("KeyError raised when it should not have been.")

    def test_handle_do_event_when_executor_found(self):
        # Test the case where the executor is found - executor should be called
        self._context._handle_do_event(signals.Do("signal"))
        self.assertEqual(self._context._executors["signal"].execute.call_count, 1)

    def test_handle_signal_OK(self):
        self._context.handle_signal(signals.OK())
        self.assertEqual(self._mock_application.handle_ok.call_count, 1)

    def test_handle_signal_Abort(self):
        self._context.handle_signal(signals.Abort())
        self.assertEqual(self._mock_application.handle_abort.call_count, 1)

    def test_handle_signal_Error(self):
        self._context.handle_signal(signals.Error())
        self.assertEqual(self._mock_application.handle_errors.call_count, 1)

    def test_handle_signal_Quit(self):
        self._context.handle_signal(signals.Quit())
        self.assertEqual(self._mock_application.handle_quit.call_count, 1)

    def test_handle_signal_exception(self):
        # Test the case where an exception is raised during error handling
        self._mock_application.handle_errors.side_effect = Exception()
        self._context.handle_signal(signals.OK())
        self.assertEqual(self._mock_application.handle_errors.call_count, 1)
