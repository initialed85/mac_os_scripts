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

### How do I use it?

Frankly I don't know, I'm not a sysadmin- I just write the scripts. As best I understand it you can load files
in at build time and tell scripts to run.

What you will want to do is edit run_during_build.sh and put all the necessary passwords, network paths etc
in before you mix the script into your image building system.

### How do I work on it?

#### Prerequisites (assuming you're on a Mac):

* pip (brew install pip)
* virtualenvwrapper (pip install virtualenvwrapper)

##### Create the Python virtualenv

<code>mkvirtualenv virtualenvwrapper</code> 

##### Install the requirements

<code>pip install -r requirements-dev.txt</code>

##### Run the tests

<code>py.test -v</code>

##### Make your changes