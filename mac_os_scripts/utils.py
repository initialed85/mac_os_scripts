import argparse
import collections
import datetime
import logging
import logging.handlers
import os
import subprocess
import time
import traceback

RunCommandOutput = collections.namedtuple('RunCommandOutput', ['stdout', 'stderr', 'error_level'])


def get_username():
    username = os.environ.get('USER', False)
    if username is False:
        raise KeyError('failed to get username from $USER')

    return username


def get_logger(name, max_bytes=16384, backup_count=2, also_stdout=True):
    logger = logging.getLogger(name)
    existed = True
    if not logger.handlers:
        existed = False

        logger.setLevel(logging.DEBUG)

        username = get_username()

        handler = logging.handlers.RotatingFileHandler(
            '/tmp/mac_os_scripts_{0}{1}.log'.format(
                '{0}_'.format(username) if username is not None else '',
                name,
            ),
            maxBytes=max_bytes,
            backupCount=backup_count,
        )

        handler.setFormatter(
            logging.Formatter(
                '%(asctime)s %(levelname)s %(message)s'
            )
        )

        logger.addHandler(handler)

        if also_stdout:
            handler = logging.StreamHandler()

            handler.setFormatter(
                logging.Formatter(
                    '%(asctime)s %(levelname)s ' + str(name) + ' %(message)s'
                )
            )

            logger.addHandler(handler)

    if existed:
        logger.debug('got existing logger for {0}'.format(name))
    else:
        logger.debug('created new logger for {0}'.format(name))

    return logger


logger = get_logger('utils')


def get_hostname():
    hostname = os.environ.get('HOSTNAME', False)
    if hostname is False:
        logger.error('failed to get hostname from $HOSTNAME')
        raise KeyError('failed to get hostname from $HOSTNAME')

    return hostname


def _spawn_subprocess(command_line, shell=True):
    return subprocess.Popen(
        command_line,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
        shell=shell,
        bufsize=1,
    )


def _wait_for_terminate(p, timeout=None):
    started = datetime.datetime.now()
    while p.poll() is None:
        if timeout is not None and datetime.datetime.now() - started > datetime.timedelta(seconds=timeout):
            return False
        time.sleep(0.1)

    return True


def _force_terminate(p):
    p.kill()


def run_command(command_line, quiet=True, timeout=None, send_lines=None):
    def log(function, message):
        function('run_command(command_line={0}) {1}'.format(
            repr(command_line), message
        ))

    stdout, stderr, error_level = None, None, -255

    quiet_fail_run_command_output = RunCommandOutput(
        stdout=None,
        stderr=None,
        error_level=-255,
    )

    log(logger.debug, 'called')

    try:
        p = _spawn_subprocess(command_line)
        log(logger.debug, 'invoked _spawn_subprocess successfully')
    except Exception as e:
        log(logger.error, 'invoked _spawn_subprocess unsuccessfully; exception follows:\n{0}\n'.format(
            traceback.format_exc().strip()
        ))
        if not quiet:
            raise e
        return quiet_fail_run_command_output

    if send_lines is not None:
        for line in send_lines:
            p.stdin.write('{0}\r'.format(line.rstrip()))
            p.stdin.flush()

    if not _wait_for_terminate(p, timeout):
        _force_terminate(p)
        log(logger.error, 'invoked _wait_for_terminate unsuccessfully; force terminate after {0} seconds'.format(
            timeout
        ))
        if not quiet:
            raise Exception('invoked _wait_for_terminate unsuccessfully; force terminate after {0} seconds'.format(
                timeout
            ))
    else:
        log(logger.info, 'invoked _wait_for_terminate successfully')

    try:
        stdout, stderr = [x.strip() for x in p.communicate()]
        log(logger.debug, 'invoked communicate() successfully; stdout={0}, stderr={1}'.format(
            repr(stdout), repr(stderr)
        ))
    except Exception as e:
        log(logger.error, 'invoked communicate() unsuccessfully; exception follows:\n{0}\n'.format(
            traceback.format_exc().strip()
        ))
        if not quiet:
            raise e
        return quiet_fail_run_command_output

    try:
        p.terminate()
    except:
        pass

    try:
        p.kill()
    except:
        pass

    try:
        error_level = p.returncode
    except:
        pass

    run_command_output = RunCommandOutput(
        stdout=stdout,
        stderr=stderr,
        error_level=error_level,
    )

    log(logger.debug, 'returning {0}'.format(run_command_output))

    return run_command_output


def get_argparser():
    parser = argparse.ArgumentParser(
        description='Mac OS scripts - {0}'.format(
            os.path.split(__file__)[1],
        ),
    )

    parser.add_argument(
        '-x',
        '--sudo-password',
        type=str,
        default=None,
        help='sudo password to use for this script'
    )

    return parser


def get_args(parser):
    return parser.parse_args()


def read_file(path):
    with open(path, 'r') as f:
        data = f.read()

    return data


def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)
