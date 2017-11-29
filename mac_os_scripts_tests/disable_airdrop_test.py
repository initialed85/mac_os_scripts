import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock, call

from mac_os_scripts.disable_airdrop import AirDropDisabler
from mac_os_scripts_tests.test_common import _NO_OUTPUT


class AirDropDisablerTest(unittest.TestCase):
    def setUp(self):
        self._subject = AirDropDisabler(
            sudo_password='SomePassword',
        )
        self._subject.run_command = MagicMock()

    def test_disable_airdrop(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.disable_airdrop(),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='/usr/bin/defaults write com.apple.NetworkBrowser DisableAirDrop -bool YES', quiet=True,
                     sudo_password_override=False, timeout=None, send_lines=None)
            ])
        )

    def test_restart_finder(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.restart_finder(),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='/usr/bin/pkill -9 -f Finder.app', quiet=True,
                     sudo_password_override=False, timeout=None, send_lines=None)
            ])
        )

    def test_run_pass(self):
        self._subject.disable_airdrop = MagicMock()
        self._subject.disable_airdrop.return_value = True
        self._subject.restart_finder = MagicMock()
        self._subject.restart_finder.return_value = True

        assert_that(
            self._subject.run(),
            equal_to(True)
        )
