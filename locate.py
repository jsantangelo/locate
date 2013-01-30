#!/usr/bin/python

import ConfigParser
import argparse
import os
import re

parser = argparse.ArgumentParser(description="Locates a given file/directory from a file list, as defined in generate.cfg.")
parser.add_argument("target",metavar="[name]",nargs=1,help='file/directory name to be found')
args = parser.parse_args()

configfile = "locate.cfg"
config = ConfigParser.RawConfigParser()
current_filelist = ""

#Check if file list exists
def file_does_exist():
	global current_filelist

	config.read(configfile)
	current_filelist = config.get("filelist", "path")
	current_filelist += "/all.files"

	if not os.path.isfile(current_filelist):
		print "You need to generate a file list first."
		return False
	return True

def locate(name):
	file = open(current_filelist, "r")
	for line in file:
		if re.search(name, line):
			print line.rstrip()

if __name__ == "__main__":
	if file_does_exist():
		locate(''.join(args.target))
