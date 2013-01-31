#!/usr/bin/python

import ConfigParser
import argparse
import os
import re

parser = argparse.ArgumentParser(description="Locates a given file/directory from a file list, as defined in generate.cfg.")
parser.add_argument("target",metavar="[name]",nargs=1,help='file/directory name to be found')
parser.add_argument("--go",dest="go_option",action="store_true",
	help='prints result if the specified [name] is a directory, and a single entry is found, otherwise \'.\'. Meant to be fed to \'cd\'.')
args = parser.parse_args()

configfile = "locate.cfg"
config = ConfigParser.RawConfigParser()
current_filelist = ""

#Check if file list exists
def file_does_exist():
	global current_filelist
	os.chdir(os.path.dirname(os.path.realpath(__file__)))
	if os.path.isfile(configfile):
		config.read(configfile)
		current_filelist = config.get("filelist", "path")
		current_filelist += "/all.files"

		if not os.path.isfile(current_filelist):
			print "You need to generate a file list first."
			return False
	else:
		print "No config file found!"
		return False
	return True

def locate(name):
	results = 0
	target = ""
	file = open(current_filelist, "r")
	for line in file:
		pattern = name
		if args.go_option:
			pattern += "$"
		if re.search(pattern, line):
			if args.go_option:
				if os.path.isdir(line.rstrip()):
					results += 1;
					target = line.rstrip()
			else:
				print line.rstrip()
	if target != "":
		if results == 1:
			print target
		else:
			print "."

if __name__ == "__main__":
	if file_does_exist():
		locate(''.join(args.target))
