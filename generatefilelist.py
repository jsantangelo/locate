#!/usr/bin/python

import os
import time
import argparse
import ConfigParser

parser = argparse.ArgumentParser(description="Generates a file list.")
parser.add_argument("-d",dest="days_old",default="0",metavar="[days old]",
	help='generate only if current list is older than this many days')
# parser.add_argument("-h",dest="hours_old",default="0",metavar="[hours old]",
# 	help='generate only if current list is older than this many hours')
args = parser.parse_args()

configfile = "locate.cfg"
config = ConfigParser.RawConfigParser()

filelist_dir = ""
current_filelist = ""
old_filelist = ""

searchable_dirs = []
specific_ignores = []
generic_ignores = []

#Read configuration file
def parse_configuration():
	global filelist_dir
	global searchable_dirs
	global specific_ignores
	global generic_ignores
	global current_filelist
	global old_filelist
	if os.path.isfile(configfile):
		config.read(configfile)

		filelist_dir = config.get("filelist", "path")
		paths = config.items("searchables")
		for key,path in paths:
			searchable_dirs.append(path)

		paths = config.items("specificignores")
		for key,path in paths:
			specific_ignores.append(path)

		paths = config.items("genericignores")
		for key,path in paths:
			generic_ignores.append(path)

		current_filelist = os.path.join(filelist_dir,"all.files")
		old_filelist = os.path.join(filelist_dir,"all.files.old")
	else:
		print "No config file found!"

#Clear out old filelist
def backup_current_list():
	now = time.time()
	seconds_ago = 0
	if os.path.isfile(current_filelist):
		if (args.days_old != 0):
			seconds_ago = now - 60*60*24*int(args.days_old)
			if (os.path.getmtime(current_filelist) < seconds_ago):
				if os.path.isfile(old_filelist):
					print "Removing old file..."
					os.remove(old_filelist)
				print "Backing up current file list..."
				os.rename(current_filelist, old_filelist)
				return True
	print "Not generating new file because the file list is newer than " + args.days_old + " days."
	return False

#Create new filelist (empty file)
def create_new_list():
	print "Creating new file list..."
	with file(current_filelist,'a'):
		os.utime(current_filelist, None)

#Generate new file list contents
def generate_list_content():
	with open(current_filelist,'w') as mylist:	
		for rootdir in searchable_dirs:
			for root, subdirs, files in os.walk(rootdir):
				for directory in subdirs:
					if is_specifically_ignored(os.path.join(root,directory)) or is_generic_ignored(directory):
						subdirs.remove(directory)
					else:
						mylist.write(os.path.join(root,directory) + '\n')
				for filename in files:
					if not is_specifically_ignored(os.path.join(root,filename)) or not is_generic_ignored(filename):
						mylist.write(os.path.join(root,filename) + '\n')

def is_specifically_ignored(node_in_question):
	for node in specific_ignores:
		if os.path.samefile(node, node_in_question):
			return True
	return False

def is_generic_ignored(directory):
	for dir in generic_ignores:
		if directory == dir:
			return True
	return False

#This is the "main" function; it will only execute if the script itself is run,
#not if it is imported
if __name__ == "__main__":
	parse_configuration()
	if backup_current_list():
		if create_new_list():
			generate_list_content()
