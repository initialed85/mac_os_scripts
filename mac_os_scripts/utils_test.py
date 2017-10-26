import unittest
from os import remove, environ

from hamcrest import equal_to, assert_that

from utils import get_logger, run_command, RunCommandOutput


class UtilsTest(unittest.TestCase):
    def test_get_logger(self):
        try:
            username = environ.get('USER')
        except:
            username = None

        path = '/tmp/mac_os_scripts_{0}{1}.log'.format(
            '{0}_'.format(username) if username is not None else '',
            'Test',
        )

        try:
            remove(path)
        except:
            pass

        logger = get_logger('Test')

        logger.debug('some message')

        with open(path, 'r') as f:
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
            equal_to(
                RunCommandOutput(stdout='', stderr='/bin/sh: spicy: command not found', error_level=127)
            )
        )
