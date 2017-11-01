import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock, call

from mac_os_scripts.register_computer_account import ComputerAccountRegisterer
from mac_os_scripts_tests.test_common import _NO_OUTPUT

_TMP_REGISTER_LDIF = """dn: CN=computer_group,OU=group1,OU=group2,DC=some,DC=domain,DC=com
changetype: modify
add: member
member: CN=computer_name,OU=group1,OU=group2,DC=some,DC=domain,DC=com
"""


class ComputerAccountRegistererTest(unittest.TestCase):
    def setUp(self):
        self._subject = ComputerAccountRegisterer(
            sudo_password='Password1',
        )
        self._subject.run_command = MagicMock()
        self._subject.read_file = MagicMock()
        self._subject.write_file = MagicMock()
        self._subject.get_hostname = MagicMock()

    def test_build_register_ldif(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.build_register_ldif(
                computer_group='computer_group',
                ou_path='group1.group2',
                dc_path='some.domain.com',
                computer_name='computer_name',
            ),
            equal_to(True)
        )

        assert_that(
            self._subject.write_file.mock_calls,
            equal_to([
                call('/tmp/register.ldif', _TMP_REGISTER_LDIF)
            ])
        )

    def test_register_computer_account(self):
        self._subject.run_command.return_value = _NO_OUTPUT
        self._subject.get_hostname.return_value = 'SomeHostname'

        assert_that(
            self._subject.register_computer_account(
                dc_path='some.domain.com',
                domain_username='some.admin',
                domain_password='P\@\$\$w0rd123\!\@\#'
            ),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(
                    command_line='ldapmodify -H ldap://some.domain.com -f /tmp/register.ldif -D some.admin -w P\\@\\$\\$w0rd123\\!\\@\\# -x -c -v',
                    quiet=True, sudo_password_override=None
                )
            ])
        )

    def test_run_pass(self):
        self._subject.build_register_ldif = MagicMock()
        self._subject.build_register_ldif.return_value = True
        self._subject.register_computer_account = MagicMock()
        self._subject.register_computer_account.return_value = True

        assert_that(
            self._subject.run(
                computer_group='computer_group',
                ou_path='group1.group2',
                dc_path='some.domain.com',
                computer_name='SomeHostname',
                domain_username='some.admin',
                domain_password='P\@\$\$w0rd123\!\@\#'
            ),
            equal_to(True)
        )
