import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock, call

from mac_os_scripts.enable_security_logging import SecurityLoggingEnabler
from mac_os_scripts.utils import RunCommandOutput

_TEST_ENABLE_SECURITY_LOGGING = RunCommandOutput(
    stdout='/System/Library/LaunchDaemons/com.apple.auditd.plist: service already loaded',
    stderr='',
    error_level=0,
)


class SecurityLoggingEnablerTest(unittest.TestCase):
    def setUp(self):
        self._subject = SecurityLoggingEnabler(
            sudo_password='SomePassword',
        )
        self._subject.run_command = MagicMock()

    def test_enable_security_logging(self):
        self._subject.run_command.return_value = _TEST_ENABLE_SECURITY_LOGGING

        assert_that(
            self._subject.enable_security_logging(),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='launchctl load -w /System/Library/LaunchDaemons/com.apple.auditd.plist', quiet=True,
                     sudo_password_override=None, timeout=None, send_lines=None)
            ])
        )

    def test_run_pass(self):
        self._subject.enable_security_logging = MagicMock()
        self._subject.enable_security_logging.return_value = True

        assert_that(
            self._subject.run(),
            equal_to(True)
        )
