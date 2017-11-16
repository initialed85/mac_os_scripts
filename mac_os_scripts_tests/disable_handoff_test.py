import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock, call

from mac_os_scripts.disable_handoff import HandoffDisabler
from mac_os_scripts_tests.test_common import _NO_OUTPUT


class HandoffDisablerTest(unittest.TestCase):
    def setUp(self):
        self._subject = HandoffDisabler(
            sudo_password=None,
        )
        self._subject.run_command = MagicMock()

    def test_disable_handoff(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.disable_handoff(),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='/usr/local/zetta/mac_os_scripts/external/disable_handoff.sh', quiet=True,
                     sudo_password_override=False, timeout=None, send_lines=None)
            ])
        )

    def test_run_pass(self):
        self._subject.disable_handoff = MagicMock()
        self._subject.disable_handoff.return_value = True

        assert_that(
            self._subject.run(),
            equal_to(True)
        )
