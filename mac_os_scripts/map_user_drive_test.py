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

    def test_map_user_drive(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.map_user_drive(
                server='file_server',
                share='some.user',
                username='some.user',
            ),
            equal_to(True)
        )

    def test_run_pass(self):
        self._subject.map_user_drive = MagicMock()
        self._subject.map_user_drive.return_value = True

        assert_that(
            self._subject.run(
                server='file_server',
                share='some.user',
                username='some.user',
            ),
            equal_to(True)
        )
