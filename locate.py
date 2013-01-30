#!/usr/bin/python

from generatefilelist import *

#Check if file list exists
def file_does_exist():
	if not os.path.isfile(current_filelist):
		print "You need to generate a file list first."
		return False
	return True

def locate(name):
	

if __name__ == "__main__":
	if file_does_exist():
		locate()
