"""
pythonExec.py
Original file creation date: 2011-02-27

Original concept and scripting by Eric Pavey (aka WarpCat) (warpcat@sbcglobal.net) http://www.akeric.com/
Original concept url: http://mayamel.tiddlyspot.com/#[[How%20can%20I%20have%20Wing%20send%20Python%20or%20mel%20code%20to%20Maya%3F]]
Adaptation and additional scripting by John P. Neumann (john@animateshmanimate.com) http://animateshmanimate.com
This work is licensed under the 3-clause BSD ("New BSD License") license.
This is one of the most permissive licenses available, next to the MIT license.
In other words: Use it, Share it, Make it better, Give credit where it's due. Done.
Licensing information is included in the download.

Changelog:
	See fileFolderWatcher.py for changelog info
"""

import __main__
import os
import time
import datetime
import logging
import smtplib
import config
from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText

def main():
	"""Execute the file that was saved as a txt file earlier and output it in Maya."""

	# start the logging functions
	
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
		
	# set the log filename and setup the logging config
	LOG_FILENAME = './logs/'+ logname
	logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
	
	# get micro-time for logging
	getTime = datetime.datetime.now()
	formatTime = getTime.strftime("%b %d %Y %H:%M:%S:%f")
	
	# get the current directory
	truePath = os.getcwd()
	curDir = truePath.replace('\\','/')
	# start processing the file
	tempFile = (curDir+'/pythonProcessFile.txt')
	if os.access(tempFile, os.F_OK):
		# write to the log file
		logging.info('File was successfully found : '+formatTime)
		# Open the file up and read the data
		f = open(tempFile, 'r')
		text = f.read()
		f.close
		# Prepend a history output to the file and add a history output to the end
		f = open(tempFile, 'w')
		f.write('cmds.scriptEditorInfo(historyFilename="'+curDir+'/tempOutputHistory.txt", writeHistory=True)\n')
		f.write(text)
		f.write('cmds.scriptEditorInfo(writeHistory=False)\n')
		f.close()
		# write to the log file
		logging.info('File was successfully written to: '+formatTime)
		# Open and print the file in Maya.
		f = open(tempFile, 'r')
		lines = f.readlines()
		for line in lines:
			print line
		f.close()
		print '\n',
		# Execute the file contents in Maya.
		f = open(tempFile, 'r')
		exec(f, __main__.__dict__, __main__.__dict__)
		f.close()
		logging.info('File was successfully run : '+formatTime)
		
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
			attachment = msg1.add_header('Content-Disposition', 'attachment', filename='outputFromMaya.txt')
			msg.attach(msg1)
			fp.close()
			
			logging.info('Email attachment successfully parsed : '+formatTime)
		else:			
			# read the output and put the message together.
			fp = open(curDir+'/tempOutputHistory.txt', 'r')
			msg = MIMEText(fp.read())
			fp.close()
			msg['Subject'] = config.SUBJECT
			msg['From'] = config.FROM
			msg['To'] = config.TO
			
			logging.info('Email body successfully parsed : '+formatTime)
		
		# Now email the user.
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.set_debuglevel(1)
		server.ehlo()
		server.starttls()
		server.login(config.LOGIN, config.PASSWORD)
		server.sendmail(config.FROM, config.TO, msg.as_string())
		server.quit()
		
		logging.info('Output was successfully emailed : '+formatTime)
		
		# now we need to delete the files we created
		os.remove(curDir+'/tempOutputHistory.txt')
		logging.info('tempOutputHistory.txt was successfully removed : '+formatTime)
		os.remove(curDir+'/pythonProcessFile.txt')
		logging.info('pythonProcessFile.txt was successfully removed : '+formatTime)
	else:
		print 'No temp file exists.'
		logging.error('File was not found : '+formatTime)