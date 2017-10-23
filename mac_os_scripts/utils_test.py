import unittest
from os import remove

from hamcrest import equal_to, assert_that, calling, raises

from utils import get_logger, run_command, RunCommandOutput


class UtilsTest(unittest.TestCase):
    def test_get_logger(self):
        try:
            remove('/tmp/mac_os_scripts_Test.log')
        except:
            pass

        logger = get_logger('Test')

        logger.debug('some message')

        with open('/tmp/mac_os_scripts_Test.log', 'r') as f:
            data = f.read()

        assert_that(
            data.endswith(' DEBUG some message\n'),
            equal_to(True)
        )

    def test_run_command_pass(self):
        assert_that(
            run_command('echo "Hello, world."'),
            equal_to(RunCommandOutput(stdout='Hello, world.', stderr='', error_level=0))
        )

    def test_run_command_fail_quiet(self):
        assert_that(
            run_command('spicy porkchops'),
            equal_to((None, None, -255))
        )

    def test_run_command_fail_noisy(self):
        assert_that(
            calling(run_command).with_args('spicy porkchops', quiet=False),
            raises(OSError)
        )
