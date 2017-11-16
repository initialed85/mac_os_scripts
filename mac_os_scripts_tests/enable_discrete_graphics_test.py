import unittest

from hamcrest import assert_that, equal_to
from mock import MagicMock, call

from mac_os_scripts.enable_discrete_graphics import DiscreteGraphicsEnabler
from mac_os_scripts.utils import RunCommandOutput


class DiscreteGraphicsEnablerTest(unittest.TestCase):
    def setUp(self):
        self._subject = DiscreteGraphicsEnabler(
            sudo_password=None,
        )
        self._subject.run_command = MagicMock()

    def test_enable_discrete_graphics(self):
        self._subject.run_command.return_value = RunCommandOutput(
            stdout='', stderr='', error_level=-9
        )

        assert_that(
            self._subject.enable_discrete_graphics(),
            equal_to(True)
        )

        assert_that(
            self._subject.run_command.mock_calls,
            equal_to([
                call(command_line='/usr/local/zetta/mac_os_scripts/external/gfxCardStatus.app/Contents/MacOS/gfxCardStatus --discrete',
                     quiet=True, sudo_password_override=False, timeout=5, send_lines=None)
            ])
        )

    def test_run_pass(self):
        self._subject.enable_discrete_graphics = MagicMock()
        self._subject.enable_discrete_graphics.return_value = True

        assert_that(
            self._subject.run(),
            equal_to(True)
        )
