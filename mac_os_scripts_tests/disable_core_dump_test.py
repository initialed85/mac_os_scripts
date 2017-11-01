import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock, call

from mac_os_scripts.disable_core_dump import CoreDumpDisabler
from mac_os_scripts_tests.test_common import _NO_OUTPUT


class CoreDumpDisablerTest(unittest.TestCase):
    def setUp(self):
        self._subject = CoreDumpDisabler(
            sudo_password='SomePassword',
        )
        self._subject.run_command = MagicMock()

    def test_disable_core_dump(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.disable_core_dump(),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='sysctl kern.coredump=0', quiet=True, sudo_password_override=None)
            ])
        )

    def test_run_pass(self):
        self._subject.disable_core_dump = MagicMock()
        self._subject.disable_core_dump.return_value = True

        assert_that(
            self._subject.run(),
            equal_to(True)
        )
