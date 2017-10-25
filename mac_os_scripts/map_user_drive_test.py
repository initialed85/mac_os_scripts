import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock

from mac_os_scripts.map_user_drive import UserDriveMapper
from utils import RunCommandOutput

_NO_OUTPUT = RunCommandOutput(
    stdout='',
    stderr='',
    error_level=0,
)


class UserDriveMapperTest(unittest.TestCase):
    def setUp(self):
        self._subject = UserDriveMapper(
            sudo_password='SomePassword',
        )
        self._subject.run_command = MagicMock()

    def test_create_user_drive_folder(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.create_user_drive_folder('some_user'),
            equal_to(True)
        )

    def test_change_user_drive_folder_permission(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.change_user_drive_folder_permission('some_user'),
            equal_to(True)
        )

    def test_map_user_drive(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.map_user_drive(
                username='some.user',
                password='SomePassword',
                server='file_server',
                share='some.user',
                domain='SomeDomain',
            ),
            equal_to(True)
        )

    def test_run_pass(self):
        self._subject.create_user_drive_folder = MagicMock()
        self._subject.create_user_drive_folder.return_value = True
        self._subject.change_user_drive_folder_permission = MagicMock()
        self._subject.change_user_drive_folder_permission.return_value = True
        self._subject.map_user_drive = MagicMock()
        self._subject.map_user_drive.return_value = True

        assert_that(
            self._subject.run(
                username='some.user',
                password='SomePassword',
                server='file_server',
                share='some.user',
                domain='SomeDomain',
            ),
            equal_to(True)
        )
