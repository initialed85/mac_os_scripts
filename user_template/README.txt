The scripts in here are all about manipulating the user templates.

- create_user_template.sh
    - create a user template from the specified user and set it as active
- copy_user_template.sh
    - copy the current user template to English.lproj.tar.gz in the current folder
- restore_user_template.sh
    - restore to the user template before create_user_template.sh was run

So, if you're using your own machine to build a nice fresh user template, your workflow might be like this:

- copy the above 3 scripts to somewhere on your machine
- create and activate a new user template
    - sudo ./create_user_template.sh some_user
- copy the active user template into a .tar.gz file in the current folder
    - sudo ./copy_user_template.sh
- restore to the original user template (so your system isn't messed up)
    - sudo ./restore_user_template.sh
- fix the permissions so you can access it as a non-root user
    - sudo chown $USER:staff English.lproj.tar.gz

At this point you'll now have English.lproj.tar.gz sitting in your current directory, so you can either manually copy it to a Mac
you're going to image, or you can mix it in at build time using the tools available- the code would look like this in a Bash script
(assuming you've made the English.lproj.tar.gz available in /usr/local/zetta and this script is running as root).

#!/bin/bash

cd /usr/local/zetta

tar -xzf English.lproj.tar.gz

rm -fr /System/Library/User\ Template/English.lproj

sudo cp -fr English.lproj /System/Library/User\ Template/
