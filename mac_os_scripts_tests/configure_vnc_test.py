import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock, call

from mac_os_scripts.configure_vnc import VNCConfigurator
from mac_os_scripts_tests.test_common import _NO_OUTPUT


class VNCConfiguratorTest(unittest.TestCase):
    def setUp(self):
        self._subject = VNCConfigurator(
            sudo_password='SomePassword',
        )
        self._subject.run_command = MagicMock()

    def test_configure_vnc_and_set_password(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.enable_vnc_and_set_password('OtherPassword'),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(
                    command_line="/System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart -activate -configure -access -on -clientopts -setvnclegacy -vnclegacy yes -clientopts -setvncpw -vncpw 'OtherPassword' -restart -agent -privs -all", 
                    quiet=True, send_lines=None, sudo_password_override=False, timeout=None
                    )
                ])
        )

    def test_run_pass(self):
        self._subject.enable_vnc_and_set_password = MagicMock()
        self._subject.enable_vnc_and_set_password.return_value = True

        assert_that(
            self._subject.run('OtherPassword'),
            equal_to(True)
        )
