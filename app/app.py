#!usr/bin/env python
# -*- coding:utf-8 -*-

"""\
This program manages a list of scripts. It can execute the scripts and show
their outputs.
"""

from argparse import ArgumentParser
from sys import exit
from tkinter import Tk

from controller import MainWindowController
from gui import MainWindow

VERSION = u"0.1.0"

if __name__ == "__main__":

	parser = ArgumentParser(prog="Script Manager", description="Manage different console scripts.")
	parser.add_argument(
		'-e', '--encoding', type=str, help='Encoding of the configuration file', default='utf-8', dest='encoding')
	parser.add_argument('-v', '--version', help='Print the version', action='store_true')
	parser.add_argument(
		'-c', '--configuration', type=str, help='Configuration file to use', dest='configuration')
	args = parser.parse_args()

	if args.version:
		print("Version is", VERSION)
		exit(0)

	root = Tk()
	root.title("Script Manager")
	application = MainWindow(master=root)
	controller = MainWindowController(root, application)
	application.mainloop()
