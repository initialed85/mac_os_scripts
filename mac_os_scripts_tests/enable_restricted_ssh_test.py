import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock, call

from mac_os_scripts.enable_restricted_ssh import RestrictedSSHEnabler
from mac_os_scripts_tests.test_common import _NO_OUTPUT

_ETC_PF_CONF_BEFORE = """#
# Default PF configuration file.
#
# This file contains the main ruleset, which gets automatically loaded
# at startup.  PF will not be automatically enabled, however.  Instead,
# each component which utilizes PF is responsible for enabling and disabling
# PF via -E and -X as documented in pfctl(8).  That will ensure that PF
# is disabled only when the last enable reference is released.
#
# Care must be taken to ensure that the main ruleset does not get flushed,
# as the nested anchors rely on the anchor point defined here. In addition,
# to the anchors loaded by this file, some system services would dynamically
# insert anchors into the main ruleset. These anchors will be added only when
# the system service is used and would removed on termination of the service.
#
# See pf.conf(5) for syntax.
#

#
# com.apple anchor point
#
scrub-anchor "com.apple/*"
nat-anchor "com.apple/*"
rdr-anchor "com.apple/*"
dummynet-anchor "com.apple/*"

anchor "com.apple/*"
load anchor "com.apple" from "/etc/pf.anchors/com.apple

# !!!! added by Zetta (WARNING: place any other rules above this line)

# some old garbage to be removed
"""

_ETC_PF_CONF_AFTER = """#
# Default PF configuration file.
#
# This file contains the main ruleset, which gets automatically loaded
# at startup.  PF will not be automatically enabled, however.  Instead,
# each component which utilizes PF is responsible for enabling and disabling
# PF via -E and -X as documented in pfctl(8).  That will ensure that PF
# is disabled only when the last enable reference is released.
#
# Care must be taken to ensure that the main ruleset does not get flushed,
# as the nested anchors rely on the anchor point defined here. In addition,
# to the anchors loaded by this file, some system services would dynamically
# insert anchors into the main ruleset. These anchors will be added only when
# the system service is used and would removed on termination of the service.
#
# See pf.conf(5) for syntax.
#

#
# com.apple anchor point
#
scrub-anchor "com.apple/*"
nat-anchor "com.apple/*"
rdr-anchor "com.apple/*"
dummynet-anchor "com.apple/*"

anchor "com.apple/*"
load anchor "com.apple" from "/etc/pf.anchors/com.apple

# !!!! added by Zetta (WARNING: place any other rules above this line)

# permit SSH for certain hosts
pass in quick inet proto tcp from 192.168.1.1 to any port 22
pass in quick inet proto tcp from 192.168.1.2 to any port 22

# drop SSH for all other hosts
block drop in quick inet proto tcp from any to any port 22
"""


class RestrictedSSHEnablerTest(unittest.TestCase):
    def setUp(self):
        self._subject = RestrictedSSHEnabler(
            sudo_password='Password1',
        )
        self._subject.run_command = MagicMock()
        self._subject.read_file = MagicMock()
        self._subject.write_file = MagicMock()

    def test_set_remote_login_on(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.set_remote_login_on(),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(
                    command_line='/usr/sbin/systemsetup -setremotelogin on', quiet=True, sudo_password_override=False, timeout=None, send_lines=None
                )
            ])
        )

    def test_modify_firewall_config(self):
        self._subject.read_file.return_value = _ETC_PF_CONF_BEFORE

        assert_that(
            self._subject.modify_firewall_config(
                '192.168.1.1,192.168.1.2'
            ),
            equal_to(True)
        )

        assert_that(
            self._subject.read_file.mock_calls,
            equal_to([
                call('/etc/pf.conf')
            ])
        )

        assert_that(
            self._subject.write_file.mock_calls,
            equal_to([
                call('/etc/pf.conf', _ETC_PF_CONF_AFTER)
            ])
        )

    def test_restart_firewall(self):
        self._subject.run_command.return_value = _NO_OUTPUT

        assert_that(
            self._subject.restart_firewall(),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='/sbin/pfctl -d', quiet=True, sudo_password_override=False, timeout=None, send_lines=None),
                call(command_line='/sbin/pfctl -F all', quiet=True, sudo_password_override=False, timeout=None, send_lines=None),
                call(command_line='/sbin/pfctl -f /etc/pf.conf -e', quiet=True, sudo_password_override=False, timeout=None, send_lines=None)
            ])
        )

    def test_run_pass(self):
        self._subject.set_remote_login_on = MagicMock()
        self._subject.set_remote_login_on.return_value = True
        self._subject.modify_firewall_config = MagicMock()
        self._subject.modify_firewall_config.return_value = True
        self._subject.restart_firewall = MagicMock()
        self._subject.restart_firewall.return_value = True

        assert_that(
            self._subject.run(
                allowed_hosts='192.168.1.1,192.168.1.2'
            ),
            equal_to(True)
        )
