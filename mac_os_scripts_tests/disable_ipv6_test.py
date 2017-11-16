import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock, call

from mac_os_scripts.disable_ipv6 import IPv6Disabler
from mac_os_scripts.utils import RunCommandOutput

_TEST_LIST_ALL_NETWORK_SERVICES_STDOUT = """An asterisk (*) denotes that a network service is disabled.
Thunderbolt Ethernet
Wi-Fi
Bluetooth PAN
Thunderbolt Bridge"""

_TEST_LIST_ALL_NETWORK_SERVICES_BEFORE = RunCommandOutput(
    stdout=_TEST_LIST_ALL_NETWORK_SERVICES_STDOUT,
    stderr='',
    error_level=0,
)

_TEST_LIST_ALL_NETWORK_SERVICES_AFTER = [
    'Thunderbolt Ethernet', 'Wi-Fi', 'Bluetooth PAN', 'Thunderbolt Bridge'
]

_TEST_SET_V6_OFF_BEFORE = RunCommandOutput(
    stdout='',
    stderr='',
    error_level=-0,
)

_TEST_GET_INFO_STDOUT = """Manual Configuration
IP address: 10.0.1.16
Subnet mask: 255.255.255.0
Router: (null)
IPv6: Off
Wi-Fi ID: b8:f6:b1:13:6f:d3"""

_TEST_GET_INFO_BEFORE = RunCommandOutput(
    stdout=_TEST_GET_INFO_STDOUT,
    stderr=None,
    error_level=0,
)

_TEST_GET_INFO_AFTER = {
    'wi-fi id': 'b8:f6:b1:13:6f:d3',
    'ip address': '10.0.1.16',
    'subnet mask': '255.255.255.0',
    'ipv6': 'Off',
    'router': '(null)'
}


class IPv6DisableTest(unittest.TestCase):
    def setUp(self):
        self._subject = IPv6Disabler(
            sudo_password='SomePassword',
        )
        self._subject.run_command = MagicMock()

    def test_list_all_network_services(self):
        self._subject.run_command.return_value = _TEST_LIST_ALL_NETWORK_SERVICES_BEFORE

        assert_that(
            self._subject.list_all_network_services(),
            equal_to(_TEST_LIST_ALL_NETWORK_SERVICES_AFTER)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='networksetup -listallnetworkservices', quiet=True, sudo_password_override=False, timeout=None, send_lines=None)
            ])
        )

    def test_set_v6_off(self):
        self._subject.run_command.return_value = _TEST_SET_V6_OFF_BEFORE

        assert_that(
            self._subject.set_v6_off('Thunderbolt Ethernet'),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='networksetup -setv6off "Thunderbolt Ethernet"', quiet=True, sudo_password_override=None, timeout=None, send_lines=None)
            ])
        )

    def test_get_info(self):
        self._subject.run_command.return_value = _TEST_GET_INFO_BEFORE

        assert_that(
            self._subject.get_info('Thunderbolt Ethernet'),
            equal_to(_TEST_GET_INFO_AFTER)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='networksetup -getinfo "Thunderbolt Ethernet"', quiet=True,
                     sudo_password_override=False, timeout=None, send_lines=None)
            ])
        )

    def test_run_pass(self):
        self._subject.list_all_network_services = MagicMock()
        self._subject.list_all_network_services.return_value = _TEST_LIST_ALL_NETWORK_SERVICES_AFTER

        self._subject.set_v6_off = MagicMock()
        self._subject.set_v6_off.return_value = True

        self._subject.get_info = MagicMock()
        self._subject.get_info.return_value = _TEST_GET_INFO_AFTER

        assert_that(
            self._subject.run(),
            equal_to(True)
        )
