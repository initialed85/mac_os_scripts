## mac_os_scripts

Some scripts for automating domain stuff for MacOS machines

#### Prerequisites for development

* brew
* pip
    * brew install pip
* virtualenvwrapper 
    * pip install virtualenvwrapper
    
#### Setup for dev

* mkvirtualenv mac_os_scripts
* pip install -r requirements-dev.txt

#### Run the tests

* To run the tests once
    * pynt test
* To have the tests watch for code changes
    * pynt watchtest

#### To build a deployable package folder

* ./build.sh