#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Created on 26 juin 2012

@author: u205992
"""

from wx.lib.pubsub.pub import getDefaultPublisher

from Script import ScriptServiceFactory, WindowsScript


class Model:

    """
    This class implements the model of the script manager program.
    """

    def __init__(self, **parameters):
        """
        Constructor
        """

        factory = ScriptServiceFactory(**parameters)
        self.service = factory.service
        self.messages = self.service.getScripts()
        self.pub = getDefaultPublisher()

    def addScript(self, name, executable=None, *args, **kwargs):
        """
        Add a new script in the dictonary of all messages.

        @param name: name of the script
        @param executable: path and name of the script executable
        @param args: arguments of the script (sequence form)
        @param kwargs: arguments of the script (dictonary form)
        """

        script = WindowsScript(name, executable, *args, **kwargs)
        self.service.saveScript(script)
        self.messages.setdefault(name, script)
        self.pub.sendMessage("SCRIPT ADDED", script=script)

    def deleteScript(self, name):
        """
        This method deletes a script.

        @param name: name of the script
        """
        script = self.messages.get(name, None)
        if not script:
            return

        self.service.deleteScript(script)
        del self.messages[name]
        self.pub.sendMessage("SCRIPT DELETED", script=name)

    def getScript(self, name):
        """
        Returns the named script.

        @param name: name of the script
        @return: a script or None if any
        """

        return self.messages.get(name, None)

    def getScripts(self):
        return self.messages.values()
