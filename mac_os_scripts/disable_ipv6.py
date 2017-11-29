"""

This script is responsible for disabling IPv6 on all interfaces

Commands used:

- networksetup -listallnetworkservices
- networksetup -setv6off (interface)
- networksetup -getinfo (interface

"""

from common import CLITieIn


class IPv6Disabler(CLITieIn):
    def list_all_network_services(self):
        command = 'networksetup -listallnetworkservices'
        command_output = self.command(command)

        if command_output.error_level != 0:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return None

        return list([
            x for x in command_output.stdout.strip().split('\n') if 'An asterisk' not in x
        ])

    def set_v6_off(self, name):
        command = 'networksetup -setv6off "{0}"'.format(name)
        command_output = self.command(command)

        if command_output.error_level != 0:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return False

        return True

    def get_info(self, name):
        command = 'networksetup -getinfo "{0}"'.format(name)
        command_output = self.command(command)

        if command_output.error_level != 0:
            self._logger.error(
                '{0} failed stating {1}'.format(
                    command, command_output
                )
            )
            return None

        return {
            y[0].strip().lower(): ':'.join(y[1:]).strip() for y in [
                x.split(':') for x in command_output.stdout.split('\n')
            ] if len(y) >= 2
        }

    def run(self):
        all_network_services = self.list_all_network_services()
        if all_network_services is None:
            self._logger.error('all_network_services is None; cannot continue')
            return None

        failures = []
        for name in all_network_services:
            set_v6_off = self.set_v6_off(name)
            if set_v6_off is None:
                self._logger.error('set_v6_off failed for {0}'.format(name))
                failures += [name]
                continue

            get_info = self.get_info(name)
            if not isinstance(get_info, dict):
                self._logger.error('get_info failed for {0}'.format(get_info))
                failures += [name]
                continue

            if get_info.get('ipv6', '').strip().lower() != 'off':
                self._logger.error('get_info reports that IPv6 is still set for {0}'.format(
                    name,
                ))
                failures += [name]
                continue

        if failures != []:
            self._logger.warning('there were {0}/{1} failures ({2})'.format(
                len(failures), len(all_network_services), failures
            ))
            return False

        self._logger.debug('passed')
        return True


if __name__ == '__main__':
    from utils import get_argparser, get_args

    parser = get_argparser()

    args = get_args(parser)

    actor = IPv6Disabler(
        sudo_password=args.sudo_password,
    )

    result = actor.run()

    if not result:
        exit(1)

    exit(0)
