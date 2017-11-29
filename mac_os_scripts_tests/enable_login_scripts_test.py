import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock, call

from mac_os_scripts.enable_login_scripts import LoginScriptEnabler
from mac_os_scripts_tests.disable_handoff_test import _NO_OUTPUT


class LoginScriptEnablerTest(unittest.TestCase):
    def setUp(self):
        self._subject = LoginScriptEnabler(
            sudo_password='SomePassword',

        )
        self._subject.run_command = MagicMock()

    def test_enable_mcx_login_scripts(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.enable_mcx_login_scripts(),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(
                    command_line='/usr/bin/defaults write /var/root/Library/Preferences/com.apple.loginwindow EnableMCXLoginScripts TRUE',
                    quiet=True, sudo_password_override=False, timeout=None, send_lines=None)
            ])
        )

    def test_set_mcx_script_trust(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.set_mcx_script_trust(
                trust_level='FullTrust'
            ),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(
                    command_line='/usr/bin/defaults write var/root/Library/Preferences/com.apple.loginwindow MCXScriptTrust -string \'FullTrust\'',
                    quiet=True, sudo_password_override=False, timeout=None, send_lines=None)
            ])
        )

    def test_run_pass(self):
        self._subject.enable_mcx_login_scripts = MagicMock()
        self._subject.enable_mcx_login_scripts.return_value = True
        self._subject.set_mcx_script_trust = MagicMock()
        self._subject.set_mcx_script_trust.return_value = True

        assert_that(
            self._subject.run(
                trust_level='FullTrust',
            ),
            equal_to(True)
        )
