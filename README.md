<<<<<<< HEAD
# cadnano 2.5  (*radnano*)
This is a development version of cadnano ported to `Qt5/PyQt5`, 
the dev branch is most up to date

## Changes
A number of organizational and style changes have occured from cadnano 2

* cadnano can be run in python without Qt installed at all
* Python 3 compatible
* no more camel-case'd variables (fixes namespace collisions)
* QUndoCommands are broken out to their own modules
* added a STL generator to generate models for 3D printing
* Maya code removed.
* Added ability to take advantage of `pyqtdeploy` tool to build standalone
versions that can be destributed as binary
* stablized code base so fewer crashes

The only additional burden for development on this code base is installing PyQt5 
to use the GUI which is not a one click situation.  Fortunately `pyqtdeploy`
should make this a problem for only people who want to hack on the code base.

## Running

to run:

    python bin/main.py

## PyQt5 Installation

the requirements PyQt5 and sip are available from Riverbank Computing Limited at: 

* [PyQt5 downloads](http://www.riverbankcomputing.com/software/pyqt/download5)
* [SIP downloads](http://www.riverbankcomputing.com/software/sip/download)

if on Windows just download the installer for your python version

if on Linux or Mac follow this path:

you can run the included `pyqt5_check.py` which will grab, build and install
`Qt5`, `sip` and `PyQt5` in your python environment.  It is cleanest using 
`virtualenv` and `virtualenvwrapper` creating a virtualenv with:

    mkvirtualenv -p /path/to/python/of/choice/bin/python myvenv
    python pyqt5_check.py

and then running the script, but you can definitely install in your system
python if you run:

    sudo python pyqt5_check.py

or you can manually:

1.  Install Qt5. download the [online installer](http://www.qt.io/download-open-source/)
2.  Build sip and PyQt5 against this Qt5

Of course there are many ways to accomplish this feat, but needless to say
OS X and Linux installs of `PyQt5` can be painful for some people.

### Anaconda

    I'm told cadnano runs well in Anaconda with PyQt5 support built in

# *nno2stl*: Conversion of cadnano .nno files to 3D STL model

The purpose of this is for 3D printing cadnano designs
=======
# README #

Currently, we are running main.py under bin.

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact
>>>>>>> master
