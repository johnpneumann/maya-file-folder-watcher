#!/usr/bin/env python
# encoding: utf-8
"""
fileFolderWatcher.py
Original file creation date: 2011-02-25

Watchdog implementation to monitor a folder for changes

Concept and scripting by John P. Neumann (john@animateshmanimate.com) http://animateshmanimate.com
This work is licensed under the 3-clause BSD ("New BSD License") license.
This is one of the most permissive licenses available, next to the MIT license.
In other words: Use it, Share it, Make it better, Give credit where it's due. Done.
Licensing information is included in the download.

What is it:
	A way to remotely run python scripts within Maya (and through your local python) and retrieve the output via email.

Usage:
	Run "python fileFolderWatcher.py" in the directory you have the files that you want monitored in.
	Installation and dependency instrucations are included in the README.txt file.


Limitations:
	You must have internet access; This script must be running in the background; *You have to have a dropbox account; Maya must be running
	Dropbox doesn't always like to set file modified times correctly when syncing so because of this the files don't always get triggered correctly.
	*You don't necessarily need a Dropbox account. You just need to be able to edit a file remotely from whatever device you're using - and since I wrote this to work off my iPhone (and iPad once I can afford one) the only thing editors support is Dropbox.

Bugs:
	None known.
	
ToDo:	
	@TODO Need to clean up and make the docstrings appropriately		
	
Changelog:

0.4
* removed PyMel as a dependency
* fixed a bug with files in subdirectories not firing off correctly
* included distribute_setup.py file in the libs dir - fetches newest version and installs it
* included the ez_setup.py file in the libs dir - extracted from the newest version of setup tools (version 0.6c11)
* made separate config file
* included 2 sample example files
* added an option in the config to either send output as an attachment or in the body of the email
* took install instructions out of the Usage in this file

0.3
* added full support for windows
* changed the way some of the output was sent
* added os detection to make sure both windows and osx work
* added more intense logging
* added more comments (hard to believe I'm sure)

0.2
* switched from FileSystemEventHandler to PatternMatchingEventHandler
* added semi-proper docstrings
* added error checking
* added proper logging (removed print; added logging module)
* changed imports from single line to multi-line (pep8 recommends this)

0.1
* initial creation

"""

import os
import sys
import time
import datetime
import logging
import socket
import subprocess
import shutil
import smtplib
import config
from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

def logChecker():
	"""
	Check to see if the log file exists and if not create it
	"""
	
	# set a global variable for the log file name
	global logname
	# get the date and time
	currentDay = time.strftime("%m.%d.%Y")
	# setup names for the log directory and logfile
	logdirname = 'logs'
	logname = currentDay + '.log'

	# check if the directory exists and if not create it
	if not os.path.exists('./'+logdirname):
		os.mkdir('./'+logdirname)

	# check if the file exists and if not create it
	if not os.path.exists('./'+logdirname+'/'+logname):
		f = open('./'+logdirname+'/'+logname, 'w')
		f.close()

logChecker()
# set the log filename and setup the logging config
LOG_FILENAME = './logs/'+ logname
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

# set this once
curDir = os.getcwd()

class MyEventHandler(PatternMatchingEventHandler):
	"""
	This handles the events that occur during file
	creation and modification. The only arguments
	being passed in are the files to be processed
	and ignored
	"""
	
	def currentTime(self):
		"""
		Returns the current time
		"""
		getTime = datetime.datetime.now()
		formatTime = getTime.strftime("%b %d %Y %H:%M:%S:%f")
		return formatTime
		
	def catch_all_handler(self, event):
		""" 
		The catch_all_handler writes the file affected
		and the event that occurred to a log file.
		"""
		# write the event to the log - the file affected and the event type
		logging.info(' File '+event.event_type+': ' + event.src_path + ' : ' + self.currentTime())


	def on_created(self, event):
		"""
		This handles file creation events and sends
		the file either to the console or to maya
		"""
		fullPath = event.src_path
		# check fs to see platform for proper path handling
		if sys.platform == 'win32':
			singleFile = fullPath.split('\\')[-1]
		else:
			singleFile = fullPath.split('/')[-1]
		# notify the user which file was created
		print singleFile + ' was created'
		# see if the file should be sent to maya or not
		suffix = config.SUFFIX
		if not singleFile.endswith(suffix):
			# write the output to the logfile
			self.catch_all_handler(event)
			# get the current directory and set the output file
			tempHistOutput = curDir+'/tempOutputHistory.txt'
				# check which os we're running on since neither of these commands work on both platforms for some damn reason
			if sys.platform == 'win32':
				# execute the python program
				output, error = subprocess.Popen([sys.executable, fullPath], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
			else:
				# execute the python program
				output, error = subprocess.Popen('python ' + fullPath, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
			# writing the output to file
			f = open(tempHistOutput, 'w')
			f.write(output)
			f.close()
			logging.info('File was successfully run : '+self.currentTime())
			self.email_to_user(singleFile)	
		else:
			# write the output to the logfile
			self.catch_all_handler(event)
			# send it to maya
			self.send_to_maya(fullPath, singleFile)


	def on_modified(self, event):
		"""
		This handles modified file events and sends
		the file either to the console or to maya
		"""
		fullPath = event.src_path
		# check fs to see platform for proper path handling
		if sys.platform == 'win32':
			singleFile = fullPath.split('\\')[-1]
		else:
			singleFile = fullPath.split('/')[-1]
		# notify the user which file was modified
		print singleFile + ' was modified'
		# see if the file should be sent to maya or not
		suffix = config.SUFFIX
		if not singleFile.endswith(suffix):
			# write the output to the logfile
			self.catch_all_handler(event)
			# get the current directory and set the output file
			tempHistOutput = curDir+'/tempOutputHistory.txt'
			# check which os we're running on since neither of these commands work on both platforms for some damn reason
			if sys.platform == 'win32':
				# execute the python program
				output, error = subprocess.Popen([sys.executable, fullPath], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
			else:
				# execute the python program
				output, error = subprocess.Popen('python ' + fullPath, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
			# writing the output to file
			f = open(tempHistOutput, 'w')
			f.write(output)
			f.close()
			logging.info('File was successfully run : '+self.currentTime())
			self.email_to_user(singleFile)	
		else:
			# write the output to the logfile
			self.catch_all_handler(event)
			# send it to maya
			self.send_to_maya(fullPath, singleFile)

		
	def send_to_maya(self, fullPath, singleFile):
		"""
		If the file ends in _maya.py check to see if 	
		maya is running and send the file to maya
		"""
		# first check whether maya is open or not before doing any real work
		maya = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			maya.connect((config.IPADDRESS, config.PORT))
			logging.info(' Connection to Maya was successful @ ' + self.currentTime())
			# if it's open we'll copy the file to a known filename
			shutil.copy(fullPath, curDir+'/pythonProcessFile.txt')
			logging.info('File was successfully copied : ' + self.currentTime())
			# and now we call our second library to run the maya commands
			convertPath = curDir.replace('\\','/')
			maya.send('python("import os; import sys; import maya.cmds as cmds; os.chdir(\''+convertPath+'\'); sys.path.append(\''+convertPath+'\'); import pythonExec; pythonExec.main()")')
			logging.info('File was successfully sent : ' + self.currentTime())
		except:
			maya.close()
			logging.error(' No connection made. Is Maya running? Have you opened port '+str(config.PORT)+' for Maya. ' + self.currentTime())
			raise socket.error('No connection made. Is Maya running? Have you opened port '+str(config.PORT)+' for Maya.')
		maya.close()
		
	def email_to_user(self, singleFile):
		"""
		Email the output to the user
		
		Determine whether or not the user has set the required options 
		
		or not and if the output should be sent as plaintext or an attachment
		
		"""
		
		if config.OUTPUT_TYPE == 'attachment':
			#put the message together.
			msg = MIMEMultipart()
			msg['Subject'] = config.SUBJECT
			msg['From'] = config.FROM
			msg['To'] = config.TO
			
			# put the attachment together
			attach_file = curDir+'/tempOutputHistory.txt'
			fp = open(attach_file, 'rb')
			msg1 = MIMEText(fp.read())
			attachment = msg1.add_header('Content-Disposition', 'attachment', filename='outputFrom_'+singleFile+'.txt')
			msg.attach(msg1)
			fp.close()
			
			logging.info('Email attachment successfully parsed : '+self.currentTime())
		else:
			# read the output and put the message together.
			fp = open(curDir+'/tempOutputHistory.txt', 'r')
			msg = MIMEText(fp.read())
			fp.close()
			msg['Subject'] = config.SUBJECT
			msg['From'] = config.FROM
			msg['To'] = config.TO
			
			logging.info('Email body successfully parsed : '+self.currentTime())

		# Now email the user.
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.set_debuglevel(1)
		server.ehlo()
		server.starttls()
		server.login(config.LOGIN, config.PASSWORD)
		server.sendmail(config.FROM, config.TO, msg.as_string())
		server.quit()

		logging.info('Output was successfully emailed : '+self.currentTime())

		# now we need to delete the files we created
		os.remove(curDir+'/tempOutputHistory.txt')
		logging.info('tempOutputHistory.txt was successfully removed : '+self.currentTime())
		
def main():
	"""
	Initiate the file/folder watcher and pass events to our MyEventHandler class
	"""
	event_handler = MyEventHandler(patterns=['*.py'], ignore_patterns=['*.log', '*.txt', '*.pyc'], ignore_directories=False)
	observer = Observer()
	observer.schedule(event_handler,  path='.', recursive=True)
	observer.start()
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()

if __name__ == '__main__':
	main()