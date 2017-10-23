import os
import sys
import logging
from collections import namedtuple
from pynt import task
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time
import pexpect

root = logging.getLogger()
root.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

SOURCE_FOLDERS = [
    'mac_os_scripts'
]


@task()
def flake():
    print 'flake8 check'
    result = execute_sh('flake8 src')
    if result.exitstatus != 0:
        print_result_text('Flake errors detected, see above', ShColor.FAIL)
    else:
        print_result_text('Flake check passed', ShColor.OKGREEN)


@task()
def test(test_identifier=None):
    """Runs our unit tests"""
    # UNIT_TESTING environment variable changes some decorators
    # to be pass throughs
    os.environ['UNIT_TESTING'] = 'unit testing'
    # jumping through a few hoops to getting coloured text printed out
    if test_identifier is None:
        # Discover tests in all of the source folders
        src_args = []
        for folder in SOURCE_FOLDERS:
            src_args.append('-s {0}'.format(folder))
        test_str = ' '.join(src_args)
    else:
        print 'Running with test identifier : ' + test_identifier
        test_str = test_identifier

    result = execute_sh('py.test {0} --junitxml=test_results/junit_results.xml'.format(test_str))
    # Report to the outside world that the tests have failed
    exit(result.exitstatus)


def create_observer(handler, path):
    observer = Observer()
    observer.schedule(handler, path, recursive=True)
    return observer


@task()
def watchtest(test_identifier=None, smart_watch=False):
    '''Watching files for changes and runs tests'''

    class WatchTestsEventHandler(PatternMatchingEventHandler):
        patterns = ["*.py"]

        def run_tests(self, event):
            # delete the pyc file
            file_to_remove = './' + event.src_path + 'c'
            try:
                os.remove(file_to_remove)
                print 'Deleted pyc file ' + file_to_remove
            except OSError:
                # it's ok if the file does not exist
                print 'No pyc file to delete (looked for {0})'.format(file_to_remove)

            if not smart_watch:
                adjusted_test_identifier = test_identifier if test_identifier is not None else ''
            else:
                event_test_path = '/'.join(event.src_path.split('/')[0:-1])

                if event.src_path.endswith('_test.py'):
                    event_test_path = event.src_path
                else:
                    current_folder_test_path = event.src_path.replace('.py', '_test.py')
                    if os.path.exists(current_folder_test_path):
                        if os.path.isfile(current_folder_test_path):
                            event_test_path = current_folder_test_path

                print 'Detected change in {0}, re-running {1}'.format(event.src_path, event_test_path)
                adjusted_test_identifier = event_test_path

            try:
                execute_sh("pynt 'test[{0}]'".format(adjusted_test_identifier))
            except:
                root.exception('Error running tests')

        def on_modified(self, event):
            self.run_tests(event)

        def on_created(self, event):
            self.run_tests(event)

    handler = WatchTestsEventHandler()
    observers = []
    for folder in SOURCE_FOLDERS:
        observers.append(create_observer(handler, folder))

    for ob in observers:
        ob.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for ob in observers:
            ob.stop()
            ob.join()


@task()
def smartwatchtest():
    watchtest(
        test_identifier=None,
        smart_watch=True
    )


# Utility stuff ----------------------------


class ShColor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


ShellResult = namedtuple('ShellResult', 'output exitstatus signalstatus')


class ExecuteShellError(Exception):
    pass


def execute_sh(cmd,
               abort_on_error=False,
               print_output=True):
    '''Execute a shell command'''
    child = pexpect.spawn(cmd)
    child.expect(pexpect.EOF, timeout=120)
    if child.isalive():
        child.wait()
    output = child.before
    if print_output:
        print output
    if abort_on_error:
        if child.exitstatus != 0:
            raise ExecuteShellError('Error excuting command: {0}'.format(cmd))
    return ShellResult(output=output,
                       exitstatus=child.exitstatus,
                       signalstatus=child.signalstatus)


def print_result_text(text, color):
    print '{3}{0}============= {1} ============={2}'.format(color, text, ShColor.ENDC, ShColor.BOLD)
