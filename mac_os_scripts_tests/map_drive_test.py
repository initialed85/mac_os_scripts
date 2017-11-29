import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock, call

from mac_os_scripts.map_drive import DriveMapper
from mac_os_scripts.utils import RunCommandOutput
from mac_os_scripts_tests.test_common import _NO_OUTPUT

_PING_PASS = RunCommandOutput(
    stdout="""PING 192.168.0.1 (192.168.0.1): 56 data bytes
Request timeout for icmp_seq 0
Request timeout for icmp_seq 1
Request timeout for icmp_seq 2

--- 192.168.0.1 ping statistics ---
4 packets transmitted, 0 packets received, 100.0% packet loss""",
    stderr='',
    error_level=0,
)

_PING_FAIL = RunCommandOutput(
    stdout="""PING 6.6.6.6 (6.6.6.6): 56 data bytes
Request timeout for icmp_seq 0
Request timeout for icmp_seq 1
Request timeout for icmp_seq 2clear

--- 6.6.6.6 ping statistics ---
4 packets transmitted, 0 packets received, 100.0% packet loss""",
    stderr='',
    error_level=2,
)


class UserDriveMapperTest(unittest.TestCase):
    def setUp(self):
        self._subject = DriveMapper(
            sudo_password='SomePassword',
        )
        self._subject.run_command = MagicMock()

    def test_ping_hostname_pass(self):
        self._subject.run_command.return_value = _PING_PASS

        assert_that(
            self._subject.ping_hostname('8.8.8.8'),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='/sbin/ping -c 4 -W 1000 -t 5 8.8.8.8', quiet=True,
                     sudo_password_override=False, timeout=None, send_lines=None)
            ])
        )

    def test_ping_hostname_fail(self):
        self._subject.run_command.return_value = _PING_FAIL

        assert_that(
            self._subject.ping_hostname('6.6.6.6'),
            equal_to(False)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='/sbin/ping -c 4 -W 1000 -t 5 6.6.6.6', quiet=True,
                     sudo_password_override=False, timeout=None, send_lines=None)
            ])
        )

    def test_map_drive(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.map_drive(
                hostname='file_server',
                share='user_folders/some.user',
            ),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='/usr/bin/open "smb://file_server/user_folders/some.user"', quiet=True,
                     sudo_password_override=False, timeout=None, send_lines=None)
            ])
        )

    def test_run_pass(self):
        self._subject.ping_hostname = MagicMock()
        self._subject.ping_hostname.return_value = True
        self._subject.map_drive = MagicMock()
        self._subject.map_drive.return_value = True

        assert_that(
            self._subject.run(
                hostname='file_server',
                share='user_folders/some.user',
            ),
            equal_to(True)
        )
