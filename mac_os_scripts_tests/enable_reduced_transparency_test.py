import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock, call

from mac_os_scripts.enable_reduced_transparency import ReducedTransparencyEnabler
from mac_os_scripts_tests.test_common import _NO_OUTPUT


class ReducedTransparencyEnablerTest(unittest.TestCase):
    def setUp(self):
        self._subject = ReducedTransparencyEnabler(
            sudo_password=None,
        )
        self._subject.run_command = MagicMock()

    def test_enable_reduced_transparency(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.enable_reduced_transparency(),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='defaults write com.apple.universalaccess reduceTransparency -bool true', quiet=True,
                     sudo_password_override=False, timeout=None, send_lines=None)
            ])
        )

    def test_restart_dock(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.restart_dock(),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='pkill -9 -f Dock.app', quiet=True, sudo_password_override=False, timeout=None, send_lines=None)
            ])
        )

    def test_run_pass(self):
        self._subject.enable_reduced_transparency = MagicMock()
        self._subject.enable_reduced_transparency.return_value = True
        self._subject.restart_dock = MagicMock()
        self._subject.restart_dock.return_value = True

        assert_that(
            self._subject.run(),
            equal_to(True)
        )
