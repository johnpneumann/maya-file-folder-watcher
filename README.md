# Maya File Folder Watcher
A semi-terrible idea by a young man with no experience!

A way to remotely run python scripts and retrieve the output via email.

---

This was an idea that had it's time and place and should probably die.
Literally just a clone from CreativeCrash as I move everything from there here.


*********
0.4 is live and it's highly encouraged to update. This release brings some bugfixes and some new features.
*********

I get ideas all the time. Usually I get them when I don't have a way to test them out. I also use an iPhone (although this also works with Android, iPads, netbooks, whatever as long as you can edit a file and save it to the folder you have the script running in - dropbox, an s3/webdav accout synced to a local folder, etc). There is no good python debugger on it so I can't get interactive feedback. That sucks. So I wrote this little script that hooks into the Watchdog library so that I can update files on my dropbox account and have the output of the files emailed to me. Not only will it email me the output from standard Python, but it also hooks into Maya and emails you the output from the commands you run in Maya! It also runs cross platform code so that you can run it on Windows, Mac or Linux - as a note I don't have a Linux box with Maya on it, so if someone wants to test it for me I'd really appreciate it. If anyone finds a problem shoot me an email.

Upcoming features in 0.5

- ability to send Mel to Maya

If you have ANY suggestions on how to make this better or more useful, PLEASE email me. I'll do my best to implement any suggestion and give you credit for the suggestion (or code if you're so inclined).
What is it:

A way to remotely run python scripts and retrieve the output via email.

Usage:

You'll need to install Watchdog, which is a Python library.
It can be found here: http://packages.python.org/watchdog/index.html

If you have pip you can use pip to install it: pip install watchdog
http://pypi.python.org/pypi/pip#downloads

If you have setup tools installed you can use easy\_install to install it: easy\_install watchdog
http://pypi.python.org/pypi/setuptools#files

You can also compile from source, but I'm not going to go into how to do that
    (if you don't know how to compile from source, then use one of the other methods)

Install instructions for setup tools (easy\_install) are included in the watchdog\_setup.txt file


After watchdog is installed:

- Put fileFolderWatcher.py, config.py, pythonExec.py and \_\_init\_\_.py into the folder you want monitored for changes.
- Edit config.py to fit your setup - FROM must be a gmail address.
- Then run "python fileFolderWatcher.py".
- Start working on the files in that directory and watch the magic. :)
- That's it.

Limitations:

- You must have internet access.
- This script must be running in the background.
- You have to have a dropbox account.*caveat noted below
- Maya must be running.
- Dropbox doesn't always like to set file modified times correctly when syncing. Because of this the files don't always get triggered correctly.
- If you want to change the email type from attachment to body or vice-versa you have to either restart your console or delete the config.pyc file


*caveat - You don't necessarily need a Dropbox account. You just need to be able to edit a file remotely from whatever device you're using - and since I wrote this to work off my iPhone (and iPad once I can afford one) the only thing editors support is Dropbox.


License Notes:

    Original concept and scripting for pythonExec.py by Eric Pavey (aka WarpCat)
    (warpcat@sbcglobal.net) http://www.akeric.com/
    Eric's original concept url:
    http://mayamel.tiddlyspot.com/#[[How%20can%20I%20have%20Wing%20send%20Python%20or%20mel%20code%20to%20Maya%3F]]

    Eric has said that he currently has no licensing for his scripts, but has given me permission
    to use the concepts presented in the url mentioned given that I give credit to him. As such
    if anyone modifies this script or redistributes it, you MUST credit Eric Pavey (aka WarpCat)
    if you don't rewrite the pythonExec.py script.


Bugs:
     None known

ToDo:
    Need to clean up and make our docstrings appropriately


Changelog:

0.4

- removed PyMel as a dependency
- fixed a bug with files in subdirectories not firing off correctly
- included distribute_setup.py file in the libs dir - fetches newest version of distribute and installs it
- included the ez_setup.py file in the libs dir - extracted from the newest version of setup tools (version 0.6c11)
- made separate config file
- included 2 sample example files
- added an option in the config to either send output as an attachment or in the body of the email
- put install instructions in a separate file

0.3

- added full support for windows
- changed the way some of the output was sent
- added os detection to make sure both windows and osx work
- added more intense logging
- added more comments (hard to believe I'm sure)
- included the \_\_init\_\_.py file that was missing from the last one

0.2

- switched from FileSystemEventHandler to PatternMatchingEventHandler
- added semi-proper docstrings
- added error checking
- added proper logging (removed print; added logging module)
- changed imports from single line to multi-line (pep8 recommends this)

0.1

- initial creation

