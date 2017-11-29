#!/bin/bash

# this file is applicable for each user that logs on (hence runs at log on time)

# prerequisites
#
# have copied the inner mac_os_scripts folder to /usr/local/zetta as well as the
# two bash scripts

# fully qualified domain name of the file server
FQDN='grayfs01.grayman.com.au'

# will be suffixed with \(current username)
SHARE_PREFIX='homedrives$'

# need to run scripts from here because of Python path requirements
cd /usr/local/zetta/

# disable handoff
python -m mac_os_scripts.disable_handoff

# change background image on all displays active desktops only (commented- not required)
# python -m mac_os_scripts.change_background

# disable airdrop
python -m mac_os_scripts.disable_airdrop

# enable reduced transparency
python -m mac_os_scripts.enable_reduced_transparency

# disable metadata file creation
python -m mac_os_scripts.disable_metadata_file_creation

# map user drive; note: -s flag is share prefix (not full share), it'll be suffixed with the username as a folder
python -m mac_os_scripts.map_user_drive -f "$FQDN" -s "$SHARE_PREFIX"
