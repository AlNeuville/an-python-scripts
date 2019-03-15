#!usr/bin/env python
# -*- coding:utf-8 -*-

"""\
Created on 21 juin 2012
@author: Alexandre Neuville
@version: 0.1.0

This program manages a list of scripts. It can execute the scripts and show
their outputs.
Options:
    -h, --help:    Display this help message.
    -f, --cfg:     The configuration file.
    -v, --version: Display the session number.\
"""

from getopt import getopt
from json import load
from sys import argv, exit

from wx import App

from controller import Controller


VERSION = u"0.1.0"


if __name__ == "__main__":

    configFileName = None
    encoding = "utf-8"
    options = getopt(argv[1:], "hf:", ["help", "cfg="])
    for option, value in options[0]:
        if option == "-h" or option == "--help":
            print(__doc__)
            exit(0)
        elif option == "-v" or option == "--version":
            print(VERSION)
            exit(0)
        elif option == "-f" or option == "--cfg":
            configFileName = value
        elif option == "-e" or option == "--encoding":
            encoding = value

    with open(configFileName, encoding) as f:
        parameters = load(f)
    if not parameters:
        print("Configuration not read")
        exit(1)

    app = App(False)
    app.SetVendorName("Alexandre Neuville")
    controller = Controller(**parameters)
    app.MainLoop()
