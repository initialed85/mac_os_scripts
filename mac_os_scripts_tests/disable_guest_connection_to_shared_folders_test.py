import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock, call

from mac_os_scripts.disable_guest_connection_to_shared_folders import GuestConnectionToSharedFoldersDisabler
from mac_os_scripts_tests.test_common import _NO_OUTPUT


class GuestConnectionToSharedFoldersDisablerTest(unittest.TestCase):
    def setUp(self):
        self._subject = GuestConnectionToSharedFoldersDisabler(
            sudo_password='SomePassword',
        )
        self._subject.run_command = MagicMock()

    def test_disable_guest_connection_to_shared_folders(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.disable_guest_connection_to_shared_folders(),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='/usr/bin/defaults write /Library/Preferences/SystemConfiguration/com.apple.smb.server AllowGuestAccess false',
                     quiet=True, sudo_password_override=False, timeout=None, send_lines=None)
            ])
        )

    def test_run_pass(self):
        self._subject.disable_guest_connection_to_shared_folders = MagicMock()
        self._subject.disable_guest_connection_to_shared_folders.return_value = True

        assert_that(
            self._subject.run(),
            equal_to(True)
        )
