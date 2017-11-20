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
