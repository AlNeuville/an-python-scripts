#! python
# -*- coding:utf-8 -*-

"""\
This program manages a list of scripts. It can execute the scripts and show
their outputs.
"""

from argparse import ArgumentParser
from tkinter import Tk

from app.controller import MainWindowController
from app.gui import MainWindow

if __name__ == "__main__":
	parser = ArgumentParser(prog="Script Manager", description="Manage different console scripts.")
	parser.add_argument(
		'-e', '--encoding', type=str, help='Encoding of the configuration file', default='utf-8', dest='encoding')
	parser.add_argument(
		'-c', '--configuration', type=str, help='Configuration file to use', dest='configuration')
	args = parser.parse_args()

	root = Tk()
	root.title("Script Manager")
	application = MainWindow(master=root)
	controller = MainWindowController(root, application)
	application.mainloop()
