#!/bin/bash

# assuming you've copied the contents of the mac_os_scripts folder to /usr/local/mac_os_scripts
cd /usr/local/

# disable metadata file creation
python -m mac_os_scripts.disable_metadata_file_creation
