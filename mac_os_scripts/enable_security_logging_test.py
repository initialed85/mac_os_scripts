import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock

from mac_os_scripts.enable_security_logging import SecurityLoggingEnabler
from utils import RunCommandOutput

_TEST_ENABLE_SECURITY_LOGGING = RunCommandOutput(
    stdout='/System/Library/LaunchDaemons/com.apple.auditd.plist: service already loaded',
    stderr='',
    error_level=0,
)


class SecurityLoggingEnablerTest(unittest.TestCase):
    def setUp(self):
        self._subject = SecurityLoggingEnabler()
        self._subject.run_command = MagicMock()

    def test_enable_security_logging(self):
        self._subject.run_command.return_value = _TEST_ENABLE_SECURITY_LOGGING

        assert_that(
            self._subject.enable_security_logging(),
            equal_to(True)
        )

    def test_run_pass(self):
        self._subject.test_enable_security_logging = MagicMock()
        self._subject.test_enable_security_logging.return_value = True

        assert_that(
            self._subject.run(),
            equal_to(True)
        )