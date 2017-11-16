"""

This script is responsible for changing the desktop background.

Commands used:

-  /usr/bin/osascript /usr/local/zetta/mac_os_scripts/external/change_background.scpt (path)

Scripts referenced:

- osascript change_background.scpt
on run argv

  tell application "System Events"

    set monitors to a reference to every desktop
    set numMonitors to count (monitors)

    repeat with monitorIndex from 1 to numMonitors by 1
      set picture of item monitorIndex of the monitors to "" & item 1 of argv & "" -- display 1
      set picture of item monitorIndex of the monitors to "" & item 1 of argv & "" -- display 2
      set picture of item monitorIndex of the monitors to "" & item 1 of argv & "" -- display 3
      set picture of item monitorIndex of the monitors to "" & item 1 of argv & "" -- display 4
      set picture of item monitorIndex of the monitors to "" & item 1 of argv & "" -- display 5
      set picture of item monitorIndex of the monitors to "" & item 1 of argv & "" -- display 6
      set picture of item monitorIndex of the monitors to "" & item 1 of argv & "" -- display 7
      set picture of item monitorIndex of the monitors to "" & item 1 of argv & "" -- display 8
    end repeat

  end tell

end run

"""

from common import CLITieIn


class BackgroundSetter(CLITieIn):
    def change_background(self, background_path):
        command = 'osascript /usr/local/zetta/mac_os_scripts/external/change_background.scpt {0}'.format(
            background_path
        )
        command_output = self.command(command)

        if command_output.error_level != 0:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return False

        return True

    def run(self, background_path):
        if not self.change_background(background_path):
            self._logger.error('failed change_background with background_path={0}; cannot continue'.format(
                background_path
            ))
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    parser.add_argument(
        '-b',
        '--background-path',
        type=str,
        required=True,
        help='path for background file to use'
    )

    args = get_args(parser)

    actor = BackgroundSetter(
        sudo_password=args.sudo_password,
    )

    actor.run(
        background_path=args.background_path
    )
