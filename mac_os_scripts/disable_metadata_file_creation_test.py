import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock

from mac_os_scripts.disable_metadata_file_creation import MetadataFileCreationDisabler
from utils import RunCommandOutput

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
        self._subject = MetadataFileCreationDisabler()
        self._subject.run_command = MagicMock()

    def test_set_ds_dont_write_network_stores(self):
        self._subject.run_command.return_value = _TEST_SET_DS_DONT_WRITE_NETWORK_STORES

        assert_that(
            self._subject.set_ds_dont_write_network_stores(),
            equal_to(True)
        )

    def test_get_ds_dont_write_network_stores(self):
        self._subject.run_command.return_value = _TEST_GET_DS_DONT_WRITE_NETWORK_STORES

        assert_that(
            self._subject.get_ds_dont_write_network_stores(),
            equal_to(True)
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
