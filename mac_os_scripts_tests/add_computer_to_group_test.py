import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock, call

from mac_os_scripts.add_computer_to_group import ComputerToGroupAdder
from mac_os_scripts_tests.test_common import _NO_OUTPUT

_TMP_REGISTER_LDIF = """dn: CN=Developers,OU=Users,OU=Groups,OU=Some Place,DC=some,DC=domain,DC=com
changetype: modify
add: member
member: CN=some_hostname,OU=macOS,OU=Computers,OU=Some Place,DC=some,DC=domain,DC=com
"""


class ComputerToGroupAdderTest(unittest.TestCase):
    def setUp(self):
        self._subject = ComputerToGroupAdder(
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
                source_ou_path='CN=some_hostname,OU=macOS,OU=Computers,OU=Some Place,DC=some,DC=domain,DC=com',
                destination_ou_path='CN=Developers,OU=Users,OU=Groups,OU=Some Place,DC=some,DC=domain,DC=com',
            ),
            equal_to(True)
        )

        assert_that(
            self._subject.write_file.mock_calls,
            equal_to([
                call('/tmp/register.ldif', _TMP_REGISTER_LDIF)
            ])
        )

    def test_add_computer_to_group(self):
        self._subject.run_command.return_value = _NO_OUTPUT
        self._subject.get_hostname.return_value = 'SomeHostname'

        assert_that(
            self._subject.add_computer_to_group(
                fqdn='some.domain.com',
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
                    quiet=True, sudo_password_override=False, timeout=None, send_lines=None
                )
            ])
        )

    def test_run_pass(self):
        self._subject.build_register_ldif = MagicMock()
        self._subject.build_register_ldif.return_value = True
        self._subject.add_computer_to_group = MagicMock()
        self._subject.add_computer_to_group.return_value = True

        assert_that(
            self._subject.run(
                source_ou_path='CN=some_hostname,OU=macOS,OU=Computers,OU=Some Place,DC=some,DC=domain,DC=com',
                destination_ou_path='CN=Developers,OU=Users,OU=Groups,OU=Some Place,DC=some,DC=domain,DC=com',
                fqdn='some.domain.com',
                domain_username='some.admin',
                domain_password='P\@\$\$w0rd123\!\@\#'
            ),
            equal_to(True)
        )
