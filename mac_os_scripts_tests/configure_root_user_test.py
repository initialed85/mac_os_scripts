import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock, call

from mac_os_scripts.configure_root_user import RootUserConfigurator
from mac_os_scripts_tests.test_common import _NO_OUTPUT


class RootUserConfiguratorTest(unittest.TestCase):
    def setUp(self):
        self._subject = RootUserConfigurator(
            sudo_password='SomePassword',
        )
        self._subject.run_command = MagicMock()

    def test_set_root_password(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.set_root_password(
                root_password='P\@\$\$w0rd123\!\@\#'
            ),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='dscl . -passwd /Users/root P\\@\\$\\$w0rd123\\!\\@\\#', quiet=True,
                     sudo_password_override=None, timeout=None, send_lines=None)
            ])
        )

    def test_disable_root_user(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.disable_root_user(),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='dsenableroot -d', quiet=True, sudo_password_override=None, timeout=None, send_lines=None)
            ])
        )

    def test_run_pass(self):
        self._subject.set_root_password = MagicMock()
        self._subject.set_root_password.return_value = True
        self._subject.disable_root_user = MagicMock()
        self._subject.disable_root_user.return_value = True

        assert_that(
            self._subject.run(
                root_password='P\@\$\$w0rd123\!\@\#',
            ),
            equal_to(True)
        )
