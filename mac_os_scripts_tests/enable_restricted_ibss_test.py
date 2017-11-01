import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock, call

from mac_os_scripts.enable_restricted_ibss import RestrictedIBSSEnabler
from mac_os_scripts_tests.test_common import _NO_OUTPUT


class RestrictedIBSSEnablerTest(unittest.TestCase):
    def setUp(self):
        self._subject = RestrictedIBSSEnabler(
            sudo_password='SomePassword',
        )
        self._subject.run_command = MagicMock()

    def test_enable_restricted_ibss(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.enable_restricted_ibss(),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(
                    command_line='/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport prefs RequireAdminIBSS=YES',
                    quiet=True, sudo_password_override=None)
            ])
        )

    def test_run_pass(self):
        self._subject.enable_restricted_ibss = MagicMock()
        self._subject.enable_restricted_ibss.return_value = True

        assert_that(
            self._subject.run(),
            equal_to(True)
        )
