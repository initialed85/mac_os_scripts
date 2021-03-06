import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock, call

from mac_os_scripts.set_user_account_logo import LocalUserAccountLogoSetter
from mac_os_scripts_tests.test_common import _NO_OUTPUT


class LocalUserAccountLogoSetterTest(unittest.TestCase):
    def setUp(self):
        self._subject = LocalUserAccountLogoSetter(
            sudo_password='SomePassword',
        )
        self._subject.run_command = MagicMock()

    def test_delete_user_account_logo_jpeg(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.delete_user_account_logo_jpeg(
                username='SomeUser',
            ),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='/usr/bin/dscl . delete /Users/SomeUser JPEGPhoto', quiet=True, sudo_password_override=False, timeout=None,
                     send_lines=None)
            ])
        )

    def test_delete_user_account_logo(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.delete_user_account_logo(
                username='SomeUser',
            ),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='/usr/bin/dscl . delete /Users/SomeUser Picture', quiet=True, sudo_password_override=False, timeout=None,
                     send_lines=None)
            ])
        )

    def test_create_user_account_logo(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.create_user_account_logo(
                username='SomeUser',
                logo_path='/path/to/some/logo.tif',
            ),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='/usr/bin/dscl . create /Users/SomeUser Picture "/path/to/some/logo.tif"', quiet=True,
                     sudo_password_override=False, timeout=None, send_lines=None)
            ])
        )

    def test_run_pass(self):
        self._subject.delete_user_account_logo_jpeg = MagicMock()
        self._subject.delete_user_account_logo_jpeg.return_value = True
        self._subject.delete_user_account_logo = MagicMock()
        self._subject.delete_user_account_logo.return_value = True
        self._subject.create_user_account_logo = MagicMock()
        self._subject.create_user_account_logo.return_value = True

        assert_that(
            self._subject.run(
                username='SomeUser',
                logo_path='/path/to/some/logo.tif'
            ),
            equal_to(True)
        )
