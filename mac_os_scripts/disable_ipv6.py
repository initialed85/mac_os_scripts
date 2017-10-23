from common import CLITieIn


class IPv6Disabler(CLITieIn):
    def list_all_network_services(self):
        command = 'networksetup -listallnetworkservices'
        command_output = self.command(command)

        if command_output.stdout is None:
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
        command_output = self.sudo_command(command)

        if command_output.stdout is None:
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

        if command_output.stdout is None:
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

        return True


if __name__ == '__main__':
    from sys import argv

    try:
        sudo_password = argv[1]
    except:
        sudo_password = None

    actor = IPv6Disabler(
        sudo_password=sudo_password,
    )

    actor.run()