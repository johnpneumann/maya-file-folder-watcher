#!/usr/bin/env python
# encoding: utf-8
"""

config.py
Original file creation date: 2011-03-01

Easier setting of options regarding email, port, ip, output type and the file extension to look for

"""

"""

Required fields

"""

# Modify these options for sending email
FROM = 'yourname@gmail.com'
LOGIN = FROM
PASSWORD = 'password'
TO = 'someones_email@this.com'
SUBJECT = 'The result output of running your python file'

# Modify these options for sending the output to Maya
IPADDRESS = '127.0.0.1'
PORT = 7000

"""
Optional Options

These still need to be set, but modifying them is optional

"""

# Modify this if you want the suffix of the files that gets sent to Maya to be something other than _maya.py
SUFFIX = '_maya.py'

# Change the output to either 'body' or 'attachment' to receive the output either in the email or as a txt file attachment
OUTPUT_TYPE='attachment'