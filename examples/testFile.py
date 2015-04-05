#!/usr/bin/env python
# encoding: utf-8
"""
"""

import sys
import os
import math

def main():
	print "This is just a standard python file"
	print(math.sin(6))
	print "hello world"
	print(math.atan(7))
	print('I can haz email')
	
	curDir = os.getcwd()
	print(os.listdir(curDir))
	

if __name__ == '__main__':
	main()
