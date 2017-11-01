import unittest
from os import remove

from hamcrest import equal_to, assert_that
from mock import patch

from mac_os_scripts.utils import get_username, get_hostname, get_logger, run_command, RunCommandOutput, read_file, \
    write_file


class UtilsTest(unittest.TestCase):
    @patch('mac_os_scripts.utils.os.environ')
    def test_get_username(self, environ):
        environ.get.return_value = 'SomeUser'

        assert_that(
            get_username(),
            equal_to('SomeUser')
        )

    @patch('mac_os_scripts.utils.os.environ')
    def test_get_hostname(self, environ):
        environ.get.return_value = 'SomeHostname'

        assert_that(
            get_hostname(),
            equal_to('SomeHostname')
        )

    @patch('mac_os_scripts.utils.get_username')
    def test_get_logger(self, get_username):
        username = 'SomeUser'

        get_username.return_value = username

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

    def test_read_file(self):
        with open('test_file.txt', 'w') as f:
            f.write('some data')

        assert_that(
            read_file('test_file.txt'),
            equal_to('some data')
        )

        remove('test_file.txt')

    def test_write_file(self):
        write_file('test_file.txt', 'some data')

        with open('test_file.txt', 'r') as f:
            assert_that(
                f.read(),
                equal_to('some data')
            )

        remove('test_file.txt')
