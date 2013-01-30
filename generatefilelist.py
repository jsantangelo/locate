#!/usr/bin/python

import os
import argparse
import ConfigParser

parser = argparse.ArgumentParser(description="Generates a file list.")
#parser.add_argument("--if",dest="days_old",default="0",metavar="[days old]",
#	help='generate only if current list is older than this many days')
args = parser.parse_args()

configfile = "generate.cfg"
config = ConfigParser.RawConfigParser()

searchable_dirs = []
specific_ignores = []
generic_ignores = []

#-----------------Configurables------------------
home = os.path.expanduser("~")
filelist_dir = os.path.join(home,"Documents","dev","python","test","filelist")

#This list contains all paths to be indexed (they should not overlap).
searchable_dirs.append(os.path.join(home,"Documents","dev"))

#This list contains all specific paths to be ignored.
specific_ignores.append(os.path.join(home,"Documents","dev","android","android-sdk-macosx"))

#This list contains all generic directories to ignore.
generic_ignores.append(".git")
#-----------------Configurables------------------

current_filelist = os.path.join(home,filelist_dir,"all.files")
old_filelist = os.path.join(home,filelist_dir,"all.files.old")

#Read configuration file
def parse_configuration():
	if os.path.isfile(configfile):
		config.read(configfile)
		print home
	else:
		print "No config file found!"

#Clear out old filelist
def backup_current_list():
	if os.path.isfile(old_filelist):
		os.remove(old_filelist)
		print "Removing old file..."
	if os.path.isfile(current_filelist):
		os.rename(current_filelist, old_filelist)
		print "Backing up current file list..."

#Create new filelist (empty file)
def create_new_list():
	open(current_filelist,'w').close()
	print "Creating new file list..."

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
					mylist.write(os.path.join(root,directory,filename) + '\n')

def is_specifically_ignored(directory):
	for dir in specific_ignores:
		if os.path.samefile(dir, directory):
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
	backup_current_list()
	create_new_list()
	generate_list_content()
