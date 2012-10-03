#!usr/bin/env python
# -*- coding:utf-8 -*-

'''
Created on 21 juin 2012

@author: Alexandre Neuville
'''

import wx


class MainWindow(wx.Frame):
    '''
    This class is the main window of the GUI.
    '''

    def __init__(self, iconFileName=None):
        '''
        Constructor
        '''
        wx.Frame.__init__(self, None, wx.ID_ANY, u"Gestionnaire Scripts",
                size=(600, 400))

        if iconFileName:
            self.SetIcon(wx.Icon(iconFileName, wx.BITMAP_TYPE_ICO))

        self.__scriptPanel = ScriptPanel(self)
        quitButtonPanel = QuitButtonPanel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.__scriptPanel, 1, wx.EXPAND)
        sizer.Add(quitButtonPanel, 0, wx.EXPAND)
        self.SetSizer(sizer)

        self.quit = quitButtonPanel.quit
        self.execute = self.__scriptPanel.buttonPanel.execute
        self.add = self.__scriptPanel.buttonPanel.add
        self.delete = self.__scriptPanel.buttonPanel.delete

    def addScript(self, name):
        self.__scriptPanel.addScript(name)

    def deleteScript(self, name):
        self.__scriptPanel.deleteScript(name)

    def addLine(self, line):
        self.__scriptPanel.outputPanel.addLine(line)

    def getChecked(self):
        return self.__scriptPanel.listPanel.getChecked()

    def unCheckAll(self):
        self.__scriptPanel.listPanel.unCheckAll()


class ScriptPanel(wx.Panel):
    '''
    This class implements the main panel of the main window.
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        wx.Panel.__init__(self, parent, wx.ID_ANY, style=wx.BORDER_SUNKEN)
        self.buttonPanel = ScriptButtonPanel(self)
        self.inPanel = wx.Panel(self, wx.ID_ANY)
        self.listPanel = ListScriptPanel(self.inPanel)
        self.outputPanel = OutputPanel(self.inPanel)

        inSizer = wx.BoxSizer(wx.HORIZONTAL)
        inSizer.Add(self.listPanel, 0, wx.EXPAND)
        inSizer.Add(self.outputPanel, 1, wx.EXPAND | wx.ALL, 3)
        self.inPanel.SetSizer(inSizer)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.inPanel, 1, wx.EXPAND)
        sizer.Add(self.buttonPanel, 0, wx.EXPAND | wx.ALL, 3)
        self.SetSizer(sizer)

    def addScript(self, name):
        self.listPanel.addScript(name)
        self.inPanel.GetSizer().Layout()

    def deleteScript(self, name):
        self.listPanel.deleteScript(name)
        self.inPanel.GetSizer().Layout()

    def setLabel(self, label=""):
        self.scriptButtonPanel.setLabel(label)


class OutputPanel(wx.Panel):
    """
    This class implements an output panel for the scripts.
    """

    def __init__(self, parent):
        '''
        Constructor
        '''
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self.text = wx.TextCtrl(self, wx.ID_ANY,
                style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.text.SetForegroundColour(wx.WHITE)
        self.text.SetBackgroundColour(wx.BLACK)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.text, 1, wx.EXPAND | wx.ALL, 3)
        self.SetSizer(sizer)

    def addLine(self, line):
        if len(line) == 0 or line[-1] != "\n":
            line += "\n"
        self.text.AppendText(line)
        self.text.Update()


class ListScriptPanel(wx.Panel):
    '''
    This class implements the list of scripts with checkbox
    '''

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.boxes = {}

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

    def addScript(self, name):
        box = wx.CheckBox(self, wx.ID_ANY, name)

        self.boxes.setdefault(name, box)
        self.GetSizer().Add(box, 0, wx.ALL, 2)
        self.GetSizer().Layout()

    def deleteScript(self, name):
        box = self.boxes.get(name, None)
        if not box:
            return

        del self.boxes[name]
        self.GetSizer().Remove(box)
        self.GetSizer().Layout()
        box.Destroy()

    def getChecked(self):
        names = []
        for name, box in self.boxes.items():
            if box.IsChecked():
                names.append(name)
        return names

    def unCheckAll(self):
        for box in self.boxes.values():
            box.SetValue(False)


class ScriptButtonPanel(wx.Panel):
    '''
    This panel contains the execute script button.
    '''
    LABEL = u"Scripts à exécuter: "

    def __init__(self, parent):
        '''
        Constructor
        '''
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self.execute = wx.Button(self, wx.ID_ANY, u"Exécuter")
        self.add = wx.Button(self, wx.ID_ADD, u"Ajouter")
        self.delete = wx.Button(self, wx.ID_REMOVE, u"Supprimer")
        self.label = wx.StaticText(self, wx.ID_ANY, ScriptButtonPanel.LABEL)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.add, 0)
        sizer.Add(self.delete, 0)
        sizer.Add(self.label, 0, wx.ALL | wx.ALIGN_CENTER, 3)
        sizer.AddStretchSpacer(1)
        sizer.Add(self.execute, 0)
        self.SetSizer(sizer)

    def setLabel(self, label=""):
        if not label:
            label = ""
        self.label.SetLabel(ScriptButtonPanel.LABEL + label)


class QuitButtonPanel(wx.Panel):
    '''
    This panel contains the quit button of the application.
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self.quit = wx.Button(self, wx.ID_EXIT, u"Quitter")

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddStretchSpacer(1)
        sizer.Add(self.quit, 0, wx.ALL, 3)
        self.SetSizer(sizer)


class MainMenu(wx.MenuBar):
    '''
    This class implements the menu of the main window.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        wx.MenuBar.__init__(self)

        fileMenu = wx.Menu()
        self.addItem = fileMenu.Append(wx.ID_NEW, u"Ajouter",
                u"Ajouter un nouveau script")
        self.delItem = fileMenu.Append(wx.ID_DELETE, u"Supprimer",
                u"Supprimer les scripts sélectionnés")
        fileMenu.AppendSeparator()
        self.qItem = fileMenu.Append(wx.ID_EXIT, u"Quitter",
                u"Quitter l'application")

        aboutMenu = wx.Menu()
        self.aItem = aboutMenu.Append(wx.ID_ABOUT, u"A propos",
                u"Au sujet de l'application")

        self.Append(fileMenu, u"&Fichier")
        self.Append(aboutMenu, u"&Aide")


class AboutDialogWindow(wx.AboutDialogInfo):
    '''
    classdocs
    '''

    def __init__(self, iconFileName=None):
        '''
        Constructor
        '''
        wx.AboutDialogInfo.__init__(self)

        self.SetName(u"Info")
        self.SetVersion(u"0.0.1")
        self.SetDescription(u"Programme de gestion et d'exécution de scripts.")
        self.AddDeveloper(u"Alexandre Neuville")
        self.SetCopyright(u"(c) 2012 Alexandre Neuville")
        if iconFileName:
            self.SetIcon(wx.Icon(iconFileName, wx.BITMAP_TYPE_ICO))


class ScriptWindow(wx.Dialog):
    '''
    classdoc
    '''

    def __init__(self, parent, script=None):
        wx.Dialog.__init__(self, parent, wx.ID_ANY,
                title=u"Propriété d'un script")

        self.scriptDescriptionPanel = ScriptDescriptionPanel(self, script)
        self.buttonPanel = OkCancelButtonPanel(self)
        self.ok = self.buttonPanel.ok
        self.cancel = self.buttonPanel.cancel

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.scriptDescriptionPanel, 0, wx.EXPAND)
        sizer.Add(self.buttonPanel, 0, wx.EXPAND)
        self.SetSizerAndFit(sizer)

    def getScriptName(self):
        return self.scriptDescriptionPanel.getName()

    def getScriptExecutable(self):
        return self.scriptDescriptionPanel.getExecutable()

    def getArgs(self):
        return self.scriptDescriptionPanel.getArgs()

    def getKwargs(self):
        return self.scriptDescriptionPanel.getKwargs()


class ScriptDescriptionPanel(wx.Panel):
    '''
    classdoc
    '''

    def __init__(self, parent, script=None):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        name = ""
        executable = ""
        args = []
        kwargs = {}
        if script:
            name = script.name
            if script.executable:
                executable = script.executable
            args = script.args
            kwargs = script.kwargs

        inPanelName = wx.Panel(self, wx.ID_ANY)
        nameLabel = wx.StaticText(inPanelName, wx.ID_ANY, u"Nom:")
        self.nameCtrl = wx.TextCtrl(inPanelName, wx.ID_ANY, name)

        inSizerName = wx.BoxSizer(wx.HORIZONTAL)
        inSizerName.Add(nameLabel, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        inSizerName.Add(self.nameCtrl, 1, wx.EXPAND | wx.LEFT, 3)
        inPanelName.SetSizer(inSizerName)

        inPanelExec = wx.Panel(self, wx.ID_ANY)
        execLabel = wx.StaticText(inPanelExec, wx.ID_ANY, u"Exécutable:")
        self.execCtrl = wx.TextCtrl(inPanelExec, wx.ID_ANY, executable)

        inSizerExec = wx.BoxSizer(wx.HORIZONTAL)
        inSizerExec.Add(execLabel, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        inSizerExec.Add(self.execCtrl, 1, wx.EXPAND | wx.LEFT, 3)
        inPanelExec.SetSizer(inSizerExec)

        inPanelArgs = wx.Panel(self, wx.ID_ANY)
        argsLabel = wx.StaticText(inPanelArgs, wx.ID_ANY, u"Arguments:")
        self.argsCtrl = wx.TextCtrl(inPanelArgs, wx.ID_ANY, ' '.join(args))

        inSizerArgs = wx.BoxSizer(wx.VERTICAL)
        inSizerArgs.Add(argsLabel, 0, wx.BOTTOM | wx.ALIGN_LEFT, 3)
        inSizerArgs.Add(self.argsCtrl, 1, wx.EXPAND)
        inPanelArgs.SetSizer(inSizerArgs)

        kStr = []
        for key, value in kwargs.items():
            kStr.append(key + u"=" + value)

        inPanelKwargs = wx.Panel(self, wx.ID_ANY)
        kwargsLabel = wx.StaticText(inPanelKwargs, wx.ID_ANY,
                u"Arguments nommés:")
        self.kwargsCtrl = wx.TextCtrl(inPanelKwargs, wx.ID_ANY, ' '.join(kStr))

        inSizerKwargs = wx.BoxSizer(wx.VERTICAL)
        inSizerKwargs.Add(kwargsLabel, 0, wx.BOTTOM | wx.ALIGN_LEFT, 3)
        inSizerKwargs.Add(self.kwargsCtrl, 1, wx.EXPAND)
        inPanelKwargs.SetSizer(inSizerKwargs)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(inPanelName, 0, wx.ALL | wx.EXPAND, 3)
        sizer.Add(inPanelExec, 0, wx.ALL | wx.EXPAND, 3)
        sizer.Add(inPanelArgs, 0, wx.ALL | wx.EXPAND, 3)
        sizer.Add(inPanelKwargs, 0, wx.ALL | wx.EXPAND, 3)
        self.SetSizer(sizer)

    def getName(self):
        return self.nameCtrl.GetValue().strip()

    def getExecutable(self):
        executable = self.execCtrl.GetValue().strip()
        if len(executable) == 0:
            executable = None
        return executable

    def getArgs(self):
        args = self.argsCtrl.GetValue().strip().split()
        if len(args) == 0:
            args = None
        return args

    def getKwargs(self):
        kwargs = self.kwargsCtrl.GetValue().strip().split()
        if len(kwargs) == 0:
            return None

        d = {}
        for e in kwargs:
            pair = e.split('=')
            if len(pair) != 2:
                raise Exception("")
            d.setdefault(pair[0], pair[1])

        return d


class OkCancelButtonPanel(wx.Panel):
    '''
    classdoc
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self.ok = wx.Button(self, wx.ID_SAVE, u"Sauver")
        self.cancel = wx.Button(self, wx.ID_CANCEL, u"Annuler")

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddStretchSpacer(1)
        sizer.Add(self.ok, 0, wx.BOTTOM | wx.TOP | wx.LEFT, 3)
        sizer.Add(self.cancel, 0, wx.ALL, 3)
        self.SetSizer(sizer)
