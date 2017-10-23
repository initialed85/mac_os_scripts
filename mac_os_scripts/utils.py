import collections
import logging
import logging.handlers
import shlex
import subprocess
import traceback

RunCommandOutput = collections.namedtuple('RunCommandOutput', ['stdout', 'stderr', 'error_level'])


def get_logger(name, max_bytes=16384, backup_count=2):
    """
    this function gets (or creates) a logger for the requested name

    :param name: name of logger to create or get (if it already exists)
    :param max_bytes: size a log file can get to before it rotates
    :param backup_count: number of rotations of a file before deletion (e.g. x.log, x.log.1, x.log.2)
    :return: logger object
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        handler = logging.handlers.RotatingFileHandler(
            '/tmp/mac_os_scripts_{0}.log'.format(name),
            maxBytes=max_bytes,
            backupCount=backup_count,
        )

        handler.setFormatter(
            logging.Formatter(
                '%(asctime)s %(levelname)s %(message)s'
            )
        )

        logger.addHandler(handler)

    return logger


logger = get_logger('utils')


def run_command(command_line, quiet=True):
    """
    this function tries to execute the specified command line

    :param command_line: command line to execute
    :param quiet: default True; fail quietly (no Exceptions)
    :return: RunCommandOutput object (.stdout, .stderr, .error_level)
    """

    def log(function, message):
        function('run_command(command_line={0}) {1}'.format(
            repr(command_line), message
        ))

    stdout, stderr, error_level = None, None, -255

    log(logger.debug, 'called')

    try:
        p = subprocess.Popen(
            shlex.split(command_line),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
        )
        log(logger.debug, 'invoked Popen() successfully')
    except Exception as e:
        log(logger.error, 'invoked Popen() unsuccessfully; exception follows:\n{0}\n'.format(
            traceback.format_exc().strip()
        ))
        if not quiet:
            raise e

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
