locate
======

`locate` is a file location tool written in python.

It consists of two scripts: `generatefilelist.py` and `locate.py`.

How to Use
----------

To start, you will need to configure both scripts for use on your system. By default, the name of the configuration file is `locate.cfg`, located in the same directory as the two scripts (at the top level of this repository).

The contents of the configuration file should be self-explanatory, as each section is marked out properly. At the very least, you must add a location where the file list will reside, and at least one searchable directory.

You will next need to index your desired directories. To do so, run:

	./generatefilelist.py

The `generatefilelist.py` script also takes some optional parameters. Run the script with `-h` to see available options.

Once your file list is generated, simply run:

	./locate.py whatIAmLookingFor

The `locate.py` script also takes some optional parameters. Specifically, it can return values suitable to be fed into another script or command, such as `cd`. For example, you can augment your .bashrc/.bash_profile with this:

	function go() {
		cd $(~/Documents/dev/python/locate/locate.py --go "$1")
	}

Now, running:

	go someDirectory

will automatically change your directory in your shell to the directory found, providing only one result was found, and that it was actually a directory.
