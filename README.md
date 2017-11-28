## MacOS scripts

This repo contains some scripts that help in the management of MacOS machines on a Windows domain.

They were put together to supplement a project that consisted of:

* Windows DCs
* a MacOS server
* Parallels Mac Management

The scripts are broken into two parts:

* run_during_build.sh - scripts that run during the computer build (as a privileged user)
* run_during_login.sh - scripts that run during logon (as the user logging on)

The two entrypoint scripts above are written in Bash and the rest of the scripts are written in Python
to make for easy unit testing (with the exception of a Bash script and a AppleScript script called by
Python). 

There are also some scripts in the "user template" folder with a README of their own- these will assist
you in creating a user template to your liking.

### How do I use it?

Frankly I don't know, I'm not a sysadmin- I just write the scripts. As best I understand it you can load files
in at build time and tell scripts to run.

What you will want to do is edit run_during_build.sh and put all the necessary passwords, network paths etc
in before you mix the script into your image building system.

Then, when you're ready to ship it, simply run "build.sh" or "build.bat" (depending on your platform) and it should
put all the necessary parts into a "deploy" folder for you.

### How do I work on it?

#####  Prerequisites (assuming you're on a Mac):

* pip (<code>brew install pip</code>)
* virtualenvwrapper (<code>pip install virtualenvwrapper</code>)

##### Create the Python virtualenv

<code>mkvirtualenv mac_os_scripts</code>

#### Activate the Python virtualenv

<code>workon mac_os_scripts</code>

##### Install the requirements

<code>pip install -r requirements-dev.txt</code>

##### Run the tests

<code>py.test -v</code>

##### Make your changes

Code-wise, the things to be aware of are:

* utils.py contains the base utils to interact with the system (run commands, read and write files etc)
    * also contain some helper functions to assist with argument parsing
* common.py contains the base CLITieIn object that implements some of those commands along with a logger

Look at any of the scripts to get an idea of how to use the argument parser and the CLITieIn and how to test stuff

##### Credits

* Credits to [Cody Krieger](https://github.com/codykrieger/) for 
[gfxCardStatus](https://github.com/codykrieger/gfxCardStatus)
* Credits to [qxnor](https://github.com/qnxor/) for [macoh](https://github.com/qnxor/macoh) which contains
  a build of [gfxCardStatus](https://github.com/qnxor/macoh/blob/master/gfxCardStatus.tgz) that allows
  commandline arguments to be specified 


##### License

The scripts I have written are licensed under under the MIT license (see LICENSE.txt); gfxCardStatus is licensed under
the New BSD license (see LICENSE_gfxCardStatus.txt)
