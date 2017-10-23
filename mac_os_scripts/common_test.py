import unittest

from hamcrest import assert_that, equal_to
from mock import patch, call

from mac_os_scripts.common import CLITieIn


class CLITieInTest(unittest.TestCase):
    def setUp(self):
        self._subject = CLITieIn()

    @patch('mac_os_scripts.common.run_command')
    def test_run_command_normal(self, run_command):
        self._subject.run_command('some command')

        assert_that(
            run_command.mock_calls[0:1],
            equal_to([
                call(command_line='some command', quiet=True)
            ])
        )

    @patch('mac_os_scripts.common.run_command')
    def test_run_command_global_sudo(self, run_command):
        self._subject._sudo_password = 'SomePassword'

        self._subject.run_command('some command')

        assert_that(
            run_command.mock_calls[0:1],
            equal_to([
                call(command_line='echo "SomePassword" | sudo -S some command', quiet=True)
            ])
        )

    @patch('mac_os_scripts.common.run_command')
    def test_run_command_override_sudo_different_password(self, run_command):
        self._subject._sudo_password = 'SomePassword'

        self._subject.run_command('some command', sudo_password_override='OtherPassword')

        assert_that(
            run_command.mock_calls[0:1],
            equal_to([
                call(command_line='echo "OtherPassword" | sudo -S some command', quiet=True)
            ])
        )

    @patch('mac_os_scripts.common.run_command')
    def test_run_command_override_sudo_no_password(self, run_command):
        self._subject._sudo_password = 'SomePassword'

        self._subject.run_command('some command', sudo_password_override=False)

        assert_that(
            run_command.mock_calls[0:1],
            equal_to([
                call(command_line='some command', quiet=True)
            ])
        )
