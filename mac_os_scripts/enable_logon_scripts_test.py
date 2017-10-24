import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock

from mac_os_scripts.enable_login_scripts import LoginScriptEnabler
from utils import RunCommandOutput

_NO_OUTPUT = RunCommandOutput(
    stdout='',
    stderr='',
    error_level=0,
)


class LoginScriptEnablerTest(unittest.TestCase):
    def setUp(self):
        self._subject = LoginScriptEnabler(
            sudo_password='SomePassword',
            trust_level='FullTrust',
        )
        self._subject.run_command = MagicMock()

    def test_enable_mcx_login_scripts(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.enable_mcx_login_scripts(),
            equal_to(True)
        )

    def test_set_mcx_script_trust(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.set_mcx_script_trust(self._subject._trust_level),
            equal_to(True)
        )

    def test_run_pass(self):
        self._subject.enable_mcx_login_scripts = MagicMock()
        self._subject.enable_mcx_login_scripts.return_value = True
        self._subject.set_mcx_script_trust = MagicMock()
        self._subject.set_mcx_script_trust.return_value = True

        assert_that(
            self._subject.run(),
            equal_to(True)
        )
