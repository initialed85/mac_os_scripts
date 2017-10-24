#!/bin/bash

# this file is applicable for each user that logs on (hence runs at log on time)

# prerequisites
#
# have copied the inner mac_os_scripts folder to /usr/local/zetta as well as the
# two bash scripts

# need to run scripts from here because of Python path requirements
cd /usr/local/zetta/

# disable metadata file creation
python -m mac_os_scripts.disable_metadata_file_creation

# disable handoff
python -m mac_os_scripts.disable_handoff
