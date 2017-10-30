import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock, call

from mac_os_scripts.disable_metadata_file_creation import MetadataFileCreationDisabler
from mac_os_scripts.utils import RunCommandOutput

_TEST_SET_DS_DONT_WRITE_NETWORK_STORES = RunCommandOutput(
    stdout='',
    stderr='',
    error_level=0,
)

_TEST_GET_DS_DONT_WRITE_NETWORK_STORES = RunCommandOutput(
    stdout='1',
    stderr='',
    error_level=0,
)


class MetadataFileCreationDisablerTest(unittest.TestCase):
    def setUp(self):
        self._subject = MetadataFileCreationDisabler(
            sudo_password='SomePassword',
        )
        self._subject.run_command = MagicMock()

    def test_set_ds_dont_write_network_stores(self):
        self._subject.run_command.return_value = _TEST_SET_DS_DONT_WRITE_NETWORK_STORES

        assert_that(
            self._subject.set_ds_dont_write_network_stores(),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='defaults write com.apple.desktopservices DSDontWriteNetworkStores -bool true',
                     quiet=True, sudo_password_override=False)
            ])
        )

    def test_get_ds_dont_write_network_stores(self):
        self._subject.run_command.return_value = _TEST_GET_DS_DONT_WRITE_NETWORK_STORES

        assert_that(
            self._subject.get_ds_dont_write_network_stores(),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='defaults read com.apple.desktopservices DSDontWriteNetworkStores', quiet=True,
                     sudo_password_override=False)
            ])
        )

    def test_run_pass(self):
        self._subject.set_ds_dont_write_network_stores = MagicMock()
        self._subject.set_ds_dont_write_network_stores.return_value = True
        self._subject.get_ds_dont_write_network_stores = MagicMock()
        self._subject.get_ds_dont_write_network_stores.return_value = True

        assert_that(
            self._subject.run(),
            equal_to(True)
        )
