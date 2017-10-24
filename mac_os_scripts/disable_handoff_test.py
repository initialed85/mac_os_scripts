import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock

from mac_os_scripts.disable_handoff import HandoffDisabler
from utils import RunCommandOutput

_NO_OUTPUT = RunCommandOutput(
    stdout='',
    stderr='',
    error_level=0,
)


class HandoffDisablerTest(unittest.TestCase):
    def setUp(self):
        self._subject = HandoffDisabler(
            sudo_password='SomePassword',
        )
        self._subject.run_command = MagicMock()

    def test_enable_mcx_login_scripts(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.disable_handoff(),
            equal_to(True)
        )

    def test_run_pass(self):
        self._subject.disable_handoff = MagicMock()
        self._subject.disable_handoff.return_value = True

        assert_that(
            self._subject.run(),
            equal_to(True)
        )
