import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock, call

from mac_os_scripts.configure_auditing_flags import AuditingFlagsConfigurator
from mac_os_scripts.utils import RunCommandOutput

_NO_OUTPUT = RunCommandOutput(
    stdout='',
    stderr='',
    error_level=0,
)

_ETC_SECURITY_AUDIT_CONTROL_BEFORE = """#
# $P4: //depot/projects/trustedbsd/openbsm/etc/audit_control#8 $
#
dir:/var/audit
flags:lo,aa
minfree:5
naflags:lo,aa
policy:cnt,argv
filesz:2M
expire-after:10M
superuser-set-sflags-mask:has_authenticated,has_console_access
superuser-clear-sflags-mask:has_authenticated,has_console_access
member-set-sflags-mask:
member-clear-sflags-mask:has_authenticated
"""

_ETC_SECURITY_AUDIT_CONTROL_AFTER = """#
# $P4: //depot/projects/trustedbsd/openbsm/etc/audit_control#8 $
#
dir:/var/audit
flags:lo,ad,fd,fm,-all
minfree:5
naflags:lo,aa
policy:cnt,argv
filesz:2M
expire-after:10M
superuser-set-sflags-mask:has_authenticated,has_console_access
superuser-clear-sflags-mask:has_authenticated,has_console_access
member-set-sflags-mask:
member-clear-sflags-mask:has_authenticated
"""


class AuditingFlagsConfiguratorTest(unittest.TestCase):
    def setUp(self):
        self._subject = AuditingFlagsConfigurator(
            sudo_password='Password1',
        )
        self._subject.run_command = MagicMock()
        self._subject.read_file = MagicMock()
        self._subject.write_file = MagicMock()

    def test_modify_security_auditing_flags(self):
        self._subject.read_file.return_value = _ETC_SECURITY_AUDIT_CONTROL_BEFORE

        assert_that(
            self._subject.modify_security_auditing_flags(),
            equal_to(True)
        )

        assert_that(
            self._subject.read_file.mock_calls,
            equal_to([
                call('/etc/security/audit_control')
            ])
        )

        assert_that(
            self._subject.write_file.mock_calls,
            equal_to([
                call('/etc/security/audit_control', _ETC_SECURITY_AUDIT_CONTROL_AFTER)
            ])
        )

    def test_run_pass(self):
        self._subject.modify_firewall_config = MagicMock()
        self._subject.modify_firewall_config.return_value = True

        assert_that(
            self._subject.run(),
            equal_to(True)
        )
