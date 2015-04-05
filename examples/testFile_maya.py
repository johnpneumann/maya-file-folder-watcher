#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import math
import maya.cmds as cmds

def main():
	print "We're Running a script INSIDE MAYA!"
	print(math.sin(6))
	x = cmds.polySphere(radius=2.5)
	print x
	print cmds.polySphere(x[0], query=True, radius=True)
	cmds.polyCube()
	cmds.polyTorus()
	cmds.polySphere(radius=6.0)
	x = cmds.polySphere(radius=8.0)
	print x
	x = cmds.polySphere(radius=30.0)
	print x
	x = cmds.polySphere(radius=70.0)
	print x
	x = cmds.polySphere(radius=100.0)
	print x
	x = cmds.polySphere(radius=50.0)
	print x

if __name__ == '__main__':
	main()



