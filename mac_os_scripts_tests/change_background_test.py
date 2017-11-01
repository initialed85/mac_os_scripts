import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock, call

from mac_os_scripts.change_background import BackgroundChanger
from mac_os_scripts_tests.test_common import _NO_OUTPUT


class HandoffDisablerTest(unittest.TestCase):
    def setUp(self):
        self._subject = BackgroundChanger(
            sudo_password=None,
        )
        self._subject.run_command = MagicMock()

    def test_change_background(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.change_background('/usr/local/zetta/background.jpg'),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(
                    command_line='/usr/bin/osascript /usr/local/zetta/mac_os_scripts/shell_scripts/change_background.scpt /usr/local/zetta/background.jpg',
                    quiet=True,
                    sudo_password_override=False
                )
            ])
        )

    def test_run_pass(self):
        self._subject.change_background = MagicMock()
        self._subject.change_background.return_value = True

        assert_that(
            self._subject.run('/usr/local/zetta/background.jpg'),
            equal_to(True)
        )
