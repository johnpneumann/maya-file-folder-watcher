Licensing can be found in the License.txt file.

This is an addendum to the License.txt file - give credit where it's due. :)
Original concept and scripting for pythonExec.py by Eric Pavey (aka WarpCat) 
(warpcat@sbcglobal.net) http://www.akeric.com/
Eric's original concept url: 
http://mayamel.tiddlyspot.com/#[[How%20can%20I%20have%20Wing%20send%20Python%20or%20mel%20code%20to%20Maya%3F]]

Eric has said that he currently has no licensing for his scripts, but has given me permission
to use the concepts presented in the url mentioned given that I give credit to him. As such
if anyone modifies this script or redistributes it, you MUST credit Eric Pavey (aka WarpCat)
if you don't rewrite the pythonExec.py script.

What is it:

A way to remotely run python scripts and retrieve the output via email.

Usage:

You'll need to install Watchdog, which is a Python library. 
It can be found here: http://packages.python.org/watchdog/index.html

If you have pip you can use pip to install it: pip install watchdog
http://pypi.python.org/pypi/pip#downloads

If you have setup tools installed you can use easy_install to install it: easy_install watchdog
http://pypi.python.org/pypi/setuptools#files

You can also compile from source, but I'm not going to go into how to do that 
	(if you don't know how to compile from source, then use one of the other methods)
	
Install instructions for setup tools (easy_install) are included in the watchdog_setup.txt file


After watchdog is installed - 
	Put fileFolderWatcher.py, config.py, pythonExec.py and __init__.py into the folder you want monitored for changes.
	Edit config.py to fit your setup - FROM must be a gmail address.
	Then run "python fileFolderWatcher.py".
	Start working on the files in that directory and watch the magic. :)
	That's it.
	

Limitations:

	You must have internet access.
	This script must be running in the background.
	You have to have a dropbox account.*
	Maya must be running.
	Dropbox doesn't always like to set file modified times correctly when syncing. Because of this the files don't always get triggered correctly.
	*You don't necessarily need a Dropbox account. You just need to be able to edit a file remotely from whatever device you're using - and since I wrote this to work off my iPhone (and iPad once I can afford one) the only thing editors support is Dropbox.
	If you want to change the email type from attachment to body or vice-versa you have to either restart your console or delete the config.pyc file

Bugs:
	None known

ToDo:
	Need to clean up and make our docstrings appropriately
	
	
Changelog:

0.4
* removed PyMel as a dependency
* fixed a bug with files in subdirectories not firing off correctly
* included distribute_setup.py file in the libs dir - fetches newest version of distribute and installs it
* included the ez_setup.py file in the libs dir - extracted from the newest version of setup tools (version 0.6c11)
* made separate config file
* included 2 sample example files
* added an option in the config to either send output as an attachment or in the body of the email
* put install instructions in a separate file

0.3
* added full support for windows
* changed the way some of the output was sent
* added os detection to make sure both windows and osx work
* added more intense logging
* added more comments (hard to believe I'm sure)
* included the __init__.py file that was missing from the last one

0.2
* switched from FileSystemEventHandler to PatternMatchingEventHandler
* added semi-proper docstrings
* added error checking
* added proper logging (removed print; added logging module)
* changed imports from single line to multi-line (pep8 recommends this)

0.1
* initial creation