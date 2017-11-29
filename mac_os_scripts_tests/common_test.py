import unittest

from hamcrest import assert_that, equal_to
from mock import patch, call

from mac_os_scripts.common import CLITieIn
from utils_test import RunCommandOutput


class CLITieInTest(unittest.TestCase):
    def setUp(self):
        self._subject = CLITieIn()

    @patch('mac_os_scripts.common.get_username')
    def test_get_username(self, get_username):
        get_username.return_value = 'SomeUsername'

        assert_that(
            self._subject.get_username(),
            equal_to('SomeUsername')
        )

        assert_that(
            get_username.mock_calls[0:1],
            equal_to([
                call()
            ])
        )

    @patch('mac_os_scripts.common.get_hostname')
    def test_get_hostname(self, get_hostname):
        get_hostname.return_value = 'SomeHostname'

        assert_that(
            self._subject.get_hostname(),
            equal_to('SomeHostname')
        )

        assert_that(
            get_hostname.mock_calls[0:1],
            equal_to([
                call()
            ])
        )

    @patch('mac_os_scripts.common.run_command')
    def test_run_command_normal(self, run_command):
        run_command.return_value = RunCommandOutput(
            stdout='some output\n',
            stderr='',
            error_level=0
        )

        self._subject.run_command('some command')

        assert_that(
            run_command.mock_calls[0:1],
            equal_to([
                call(command_line='some command', quiet=True, timeout=None, send_lines=None)
            ])
        )

    @patch('mac_os_scripts.common.run_command')
    def test_run_command_global_sudo(self, run_command):
        run_command.return_value = RunCommandOutput(
            stdout='some output\n',
            stderr='',
            error_level=0
        )

        self._subject._sudo_password = 'SomePassword'

        self._subject.run_command('some command')

        assert_that(
            run_command.mock_calls[0:1],
            equal_to([
                call(command_line='echo \'SomePassword\' | sudo -S some command',
                     quiet=True, timeout=None, send_lines=None)
            ])
        )

    @patch('mac_os_scripts.common.run_command')
    def test_run_command_override_sudo_different_password(self, run_command):
        run_command.return_value = RunCommandOutput(
            stdout='some output\n',
            stderr='',
            error_level=0
        )

        self._subject._sudo_password = 'SomePassword'

        self._subject.run_command('some command', sudo_password_override='OtherPassword')

        assert_that(
            run_command.mock_calls[0:1],
            equal_to([
                call(command_line='echo \'OtherPassword\' | sudo -S some command',
                     quiet=True, timeout=None, send_lines=None)
            ])
        )

    @patch('mac_os_scripts.common.run_command')
    def test_run_command_override_sudo_no_password(self, run_command):
        run_command.return_value = RunCommandOutput(
            stdout='some output\n',
            stderr='',
            error_level=0
        )

        self._subject._sudo_password = 'SomePassword'

        self._subject.run_command(
            'some command',
            sudo_password_override=False,
            timeout=None,
            send_lines=None)

        assert_that(
            run_command.mock_calls[0:1],
            equal_to([
                call(command_line='some command', quiet=True, timeout=None, send_lines=None)
            ])
        )

    @patch('mac_os_scripts.common.read_file')
    def test_read_file(self, read_file):
        read_file.return_value = 'some data'

        self._subject.read_file('/some/path')

        assert_that(
            [x for x in read_file.mock_calls if '__' not in repr(x)],
            equal_to([
                call('/some/path')
            ])
        )

    @patch('mac_os_scripts.common.write_file')
    def test_write_file(self, write_file):
        self._subject.write_file('/some/path', 'some data')

        assert_that(
            write_file.mock_calls,
            equal_to([
                call('/some/path', 'some data')
            ])
        )
