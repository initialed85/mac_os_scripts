import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock, call

from mac_os_scripts.configure_ntp import NTPConfigurator
from mac_os_scripts_tests.test_common import _NO_OUTPUT


class NTPConfiguratorTest(unittest.TestCase):
    def setUp(self):
        self._subject = NTPConfigurator(
            sudo_password='SomePassword',
        )
        self._subject.run_command = MagicMock()

    def test_enable_ntp(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.enable_ntp(),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='/usr/sbin/systemsetup -setusingnetworktime on', quiet=True, sudo_password_override=False, timeout=None,
                     send_lines=None)
            ])
        )

    def test_set_ntp_server(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.set_ntp_server(
                server='time1.google.com'
            ),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='/usr/sbin/systemsetup -setnetworktimeserver time1.google.com', quiet=True,
                     sudo_password_override=False, timeout=None, send_lines=None)
            ])
        )

    def test_run_pass(self):
        self._subject.enable_ntp = MagicMock()
        self._subject.enable_ntp.return_value = True
        self._subject.set_ntp_server = MagicMock()
        self._subject.set_ntp_server.return_value = True

        assert_that(
            self._subject.run(
                server='time1.google.com'
            ),
            equal_to(True)
        )
