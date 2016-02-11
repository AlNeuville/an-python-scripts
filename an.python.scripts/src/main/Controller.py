#!usr/bin/env python
# -*- coding:utf-8 -*-

'''
Created on 21 juin 2012

@author: Alexandre Neuville
'''

from Queue import PriorityQueue
from subprocess import Popen, PIPE, STDOUT, STARTUPINFO, STARTF_USESHOWWINDOW
from threading import Thread, Lock
import os

import wx

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
        self.scriptsInQueue = {}
        self.labelLock = Lock()

        self.model = Model(**parameters["model"])
        self.icon = parameters.get("icon", None)
        self.view = MainWindow(self.icon)
        self.executor = ParallelScriptExecutor(self.onSignalStart, self.onSignalEnd, self.view.addLine)
        self.executor.start()
        self.stop = StopManager(self.executor, self.stopped)

        self.view.SetMenuBar(self.__createMainMenu())
        for script in self.model.getScripts():
            self.view.addScript(script.name)

        self.model.pub.subscribe(self.onScriptAdd, "SCRIPT ADDED")
        self.model.pub.subscribe(self.onScriptDelete, "SCRIPT DELETED")

        self.autoQuitEnable = parameters.get("autoQuit", False)
        self.view.Bind(wx.EVT_CHECKBOX, self.onQuitCheck, self.view.isAutoQuit)
        self.view.isAutoQuit.SetValue(self.autoQuitEnable)

        self.view.Bind(wx.EVT_BUTTON, self.onQuit, self.view.quit)
        self.view.Bind(wx.EVT_BUTTON, self.onExecuteScript, self.view.execute)
        self.view.Bind(wx.EVT_BUTTON, self.addScript, self.view.add)
        self.view.Bind(wx.EVT_BUTTON, self.deleteScript, self.view.delete)
        self.view.Bind(wx.EVT_BUTTON, self.checkAll, self.view.addAll)

        self.view.Center(wx.CENTER_ON_SCREEN)
        self.view.Show(True)

    def __createMainMenu(self):
        menu = MainMenu()

        self.view.Bind(wx.EVT_MENU, self.onQuit, menu.qItem)
        self.view.Bind(wx.EVT_MENU, self.onAbout, menu.aItem)
        self.view.Bind(wx.EVT_MENU, self.addScript, menu.addItem)
        self.view.Bind(wx.EVT_MENU, self.deleteScript, menu.delItem)

        return menu

    def addScript(self, unusedEvent):
        ScriptWindowController(self.model, self.view)

    def deleteScript(self, unusedEvent):
        for name in self.view.getChecked():
            self.model.deleteScript(name)

    def onScriptAdd(self, script):
        self.view.addScript(script.name)

    def onScriptDelete(self, script):
        self.view.deleteScript(script)

    def onExecuteScript(self, unusedEvent):
        names = self.view.getChecked()
        if len(names) == 0:
            return

        for name in names:
            self.addScriptInWaitingQueue(name)

        for name in names:
            script = self.model.getScript(name)
            self.executor.messages.put((1, script))

        self.view.unCheckAll()

    def onQuit(self, unusedEvent):
        self.view.quit.Disable()
        self.view.execute.Disable()
        self.clearWaitingQueue()
        self.stop.start()

    def stopped(self):
        self.view.Close()

    def onAbout(self, unusedEvent):
        wx.AboutBox(AboutDialogWindow(self.icon))

    def onSignalStart(self, script):
        if script and script.name:
            self.removeScriptFromWaitingQueue(script.name)

    def onSignalEnd(self, script):
        if self.autoQuitEnable:
            self.onQuit(None)

    def onQuitCheck(self, unusedEvent):
        if self.view.isAutoQuit.IsChecked():
            self.autoQuitEnable = True
        else:
            self.autoQuitEnable = False

    def addScriptInWaitingQueue(self, name):
        self.labelLock.acquire(True)
        nbr = self.scriptsInQueue.get(name, 0)
        if nbr == 0:
            self.scriptsInQueue.setdefault(name, 1)
        else:
            self.scriptsInQueue[name] = nbr + 1
        self.updateWaitingLabel()
        self.labelLock.release()

    def removeScriptFromWaitingQueue(self, name):
        self.labelLock.acquire(True)
        nbr = self.scriptsInQueue.get(name)
        if nbr > 1:
            self.scriptsInQueue[name] = nbr - 1
        else:
            self.scriptsInQueue.pop(name, None)
        self.updateWaitingLabel()
        self.labelLock.release()

    def clearWaitingQueue(self):
        self.labelLock.acquire(True)
        self.scriptsInQueue.clear()
        self.updateWaitingLabel()
        self.labelLock.release()

    def updateWaitingLabel(self):
        label = []
        for name, nbr in self.scriptsInQueue.items():
            label.append(u", ")
            label.append(name)
            if nbr > 1:
                label.append(u" (")
                label.append(str(nbr))
                label.append(u")")
        if len(label) > 1:
            self.view.updateWaitingLabel(''.join(label[1:]))
        else:
            self.view.updateWaitingLabel("")

    def checkAll(self, unusedEvent):
        self.view.checkAll()


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
        try:
            kwargs = self.view.getKwargs()

            if args and kwargs:
                self.model.addScript(name, executable, *args, **kwargs)
            elif args:
                self.model.addScript(name, executable, *args)
            elif kwargs:
                self.model.addScript(name, executable, **kwargs)
            else:
                self.model.addScript(name, executable)
        finally:
            self.view.Destroy()

    def onCancel(self, unusedEvent):
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

    def __init__(self, signalStart=None, signalEnd=None, call=None):
        """
        Constructor
        """
        Thread.__init__(self, None, None, "scriptExecutor", (), {})
        self.messages = PriorityQueue()
        self.callable = call
        self.signalEnd = signalEnd
        self.signalStart = signalStart

    def run(self):
        while True:
            msg = self.messages.get()[1]
            if msg == "EXIT_THREAD":
                break

            execObj = None
            try:
                if self.signalStart:
                    self.signalStart(msg)

                command = msg.toExecutableString()
                if self.callable:
                    self.callable(u"Exécution: " + msg.name)
                    self.callable(u"Command: " + command)
                    self.callable(u"\n")

                execObj = None
                if os.name == "nt":
                    si = STARTUPINFO()
                    si.dwFlags |= STARTF_USESHOWWINDOW
                    execObj = Popen(command.encode("cp850"), stdout=PIPE, stderr=STDOUT, universal_newlines=True,
                                    startupinfo=si)
                else:
                    raise ControllerError("Execution not implemented for other OS than Microsoft Windows")

                if self.callable:
                    self.callable(u"Output:")
                    while execObj.poll() is None:
                        line = execObj.stdout.readline().strip()
                        if len(line) > 0:
                            self.callable(line.decode("cp850"))

                    self.callable(u"\nFin de l'exécution de " + msg.name)
            except Exception, e:
                if self.callable:
                    self.callable(str(e).decode("cp1252"))
                    if execObj and execObj.poll() is not None:
                        execObj.kill()
                else:
                    print str(e).decode("cp1252")
            finally:
                if self.callable:
                    self.callable(u"----------------------\n")
                if self.signalEnd:
                    self.signalEnd(msg)
