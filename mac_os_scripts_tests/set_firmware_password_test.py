import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock, call

from mac_os_scripts.set_firmware_password import FirmwarePasswordSetter
from mac_os_scripts_tests.test_common import _NO_OUTPUT


class FirmwarePasswordSetterTest(unittest.TestCase):
    def setUp(self):
        self._subject = FirmwarePasswordSetter(
            sudo_password='SomePassword',
        )
        self._subject.run_command = MagicMock()

    def test_set_firmware_password(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.set_firmware_password('OtherPassword'),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='expect -d -f /usr/local/zetta/mac_os_scripts/external/set_firmware_password.expect \'OtherPassword\'',
                     quiet=True, send_lines=None, sudo_password_override=False, timeout=None)
            ])
        )

    def test_run_pass(self):
        self._subject.set_firmware_password = MagicMock()
        self._subject.set_firmware_password.return_value = True

        assert_that(
            self._subject.run('OtherPassword'),
            equal_to(True)
        )
