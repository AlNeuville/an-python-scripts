#!usr/bin/env python
# -*- coding:utf-8 -*-

'''
Created on 21 juin 2012

@author: Alexandre Neuville
'''

import os
import wx
from Script import Script
from subprocess import Popen, PIPE, STDOUT, STARTUPINFO, STARTF_USESHOWWINDOW
from threading import Thread
from Queue import PriorityQueue
from Gui import MainWindow, MainMenu, AboutDialogWindow, ScriptWindow
from Model import Model


class ControllerError(Exception):
    pass


class Controller:
    '''
    This class implements the controller for the Script objects.
    '''

    def __init__(self, **parameters):
        '''
        Constructor
        '''
        self.model = Model(**parameters["model"])
        self.icon = parameters.get("icon", None)
        self.view = MainWindow(self.icon)
        self.executor = ParallelScriptExecutor(self.view.addLine)
        self.executor.start()
        self.stop = StopManager(self.executor, self.stopped)

        self.view.SetMenuBar(self.__createMainMenu())
        for script in self.model.getScripts():
            self.view.addScript(script.name)

        self.model.pub.subscribe(self.onScriptAdd, "SCRIPT ADDED")
        self.model.pub.subscribe(self.onScriptDelete, "SCRIPT DELETED")

        self.view.Bind(wx.EVT_BUTTON, self.onQuit, self.view.quit)
        self.view.Bind(wx.EVT_BUTTON, self.onExecuteScript, self.view.execute)
        self.view.Bind(wx.EVT_BUTTON, self.addScript, self.view.add)
        self.view.Bind(wx.EVT_BUTTON, self.deleteScript, self.view.delete)

        self.view.Center(wx.CENTER_ON_SCREEN)
        self.view.Show(True)

    def __createMainMenu(self):
        menu = MainMenu()

        self.view.Bind(wx.EVT_MENU, self.onQuit, menu.qItem)
        self.view.Bind(wx.EVT_MENU, self.onAbout, menu.aItem)
        self.view.Bind(wx.EVT_MENU, self.addScript, menu.addItem)
        self.view.Bind(wx.EVT_MENU, self.deleteScript, menu.delItem)

        return menu

    def addScript(self, e):
        ScriptWindowController(self.model, self.view)

    def deleteScript(self, e):
        for name in self.view.getChecked():
            self.model.deleteScript(name)

    def onScriptAdd(self, message):
        script = message.data
        self.view.addScript(script.name)

    def onScriptDelete(self, message):
        name = message.data
        self.view.deleteScript(name)

    def onExecuteScript(self, e):
        names = self.view.getChecked()
        for name in names:
            script = self.model.getScript(name)
            self.executor.messages.put((1, script))
        self.view.unCheckAll()

    def onQuit(self, e):
        self.view.quit.Disable()
        self.view.execute.Disable()
        self.stop.start()

    def stopped(self):
        self.view.Close()

    def onAbout(self, e):
        wx.AboutBox(AboutDialogWindow(self.icon))


class ScriptWindowController:
    '''
    Classdocs
    '''
    def __init__(self, model, parent, script=None):
        '''
        Constructor
        '''
        self.model = model
        self.view = ScriptWindow(parent, script)

        self.view.Bind(wx.EVT_BUTTON, self.onOk, self.view.ok)
        self.view.Bind(wx.EVT_BUTTON, self.onCancel, self.view.cancel)

        self.view.ShowModal()

    def onOk(self, e):
        name = self.view.getScriptName()
        if not name or len(name) == 0:
            self.onCancel(e)

        executable = self.view.getScriptExecutable()
        args = self.view.getArgs()
        kwargs = self.view.getKwargs()

        if args and kwargs:
            self.model.addScript(name, executable, *args, **kwargs)
        elif args:
            self.model.addScript(name, executable, *args)
        elif kwargs:
            self.model.addScript(name, executable, **kwargs)
        else:
            self.model.addScript(name, executable)

        self.view.Destroy()

    def onCancel(self, e):
        self.view.Destroy()


class StopManager(Thread):
    """
    Classdocs
    """
    def __init__(self, managed, call):
        """
        Constructor
        """
        Thread.__init__(self, None, None, "stopManager", (), {})
        self.callable = call
        self.managed = managed

    def run(self):
        self.managed.messages.put((0, "EXIT_THREAD"))
        self.managed.join()
        self.callable()


class ParallelScriptExecutor(Thread):
    """
    Classdocs
    """

    def __init__(self, call=None):
        """
        Constructor
        """
        Thread.__init__(self, None, None, "scriptExecutor", (), {})
        self.messages = PriorityQueue()
        self.callable = call

    def run(self):
        while True:
            msg = self.messages.get()[1]
            if msg == "EXIT_THREAD":
                break

            execObj = None
            try:
                command = msg.toExecutableString()
                if self.callable:
                    self.callable(u"Exécution: " + msg.name)
                    self.callable(u"Command: " + command)
                    self.callable(u"\n")

                execObj = None
                if os.name == "nt":
                    si = STARTUPINFO()
                    si.dwFlags |= STARTF_USESHOWWINDOW
                    execObj = Popen(command.encode("cp850"), stdout=PIPE,
                            stderr=STDOUT, universal_newlines=True,
                            startupinfo=si)
                else:
                    raise ControllerError("Execution not implemented for" + \
                            " other OS than Microsoft Windows")

                if self.callable:
                    self.callable(u"Output:")
                    while execObj.poll() == None:
                        line = execObj.stdout.readline().strip()
                        if len(line) > 0:
                            self.callable(line.decode("cp850"))

                    self.callable(u"\nFin de l'exécution de " + msg.name)
            except Exception, e:
                if self.callable:
                    self.callable(str(e).decode("cp1252"))
                    if execObj and execObj.poll() != None:
                        execObj.kill()
                else:
                    print str(e).decode("cp1252")
            finally:
                if self.callable:
                    self.callable(u"----------------------\n")
