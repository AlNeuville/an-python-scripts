#!usr/bin/env python
# -*- coding:utf-8 -*-

"""
Created on 21 juin 2012

@author: Alexandre Neuville
"""

import wx


class MainWindow(wx.Frame):
    """
    This class is the main window of the GUI.
    """

    def __init__(self, iconFileName=None):
        """
        Constructor
        """
        wx.Frame.__init__(self, None, wx.ID_ANY, u"Gestionnaire Scripts", size=(600, 400))

        if iconFileName:
            self.SetIcon(wx.Icon(iconFileName, wx.BITMAP_TYPE_ICO))

        self.__scriptPanel = ScriptPanel(self)
        quit_button_panel = QuitButtonPanel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.__scriptPanel, 1, wx.EXPAND)
        sizer.Add(quit_button_panel, 0, wx.EXPAND)
        self.SetSizer(sizer)

        self.isAutoQuit = quit_button_panel.isAutoQuit
        self.quit = quit_button_panel.quit
        self.execute = self.__scriptPanel.buttonPanel.execute
        self.add = self.__scriptPanel.buttonPanel.add
        self.delete = self.__scriptPanel.buttonPanel.delete
        self.addAll = self.__scriptPanel.buttonPanel.addAll

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

    def checkAll(self):
        self.__scriptPanel.listPanel.checkAll()

    def updateWaitingLabel(self, label):
        self.__scriptPanel.setLabel(label)


class ScriptPanel(wx.Panel):
    """
    This class implements the main panel of the main window.
    """

    def __init__(self, parent):
        """
        Constructor
        """
        wx.Panel.__init__(self, parent, wx.ID_ANY, style=wx.BORDER_SUNKEN)
        self.buttonPanel = ScriptButtonPanel(self)
        self.inPanel = wx.Panel(self, wx.ID_ANY)
        self.listPanel = ListScriptPanel(self.inPanel)
        self.outputPanel = OutputPanel(self.inPanel)

        in_sizer = wx.BoxSizer(wx.HORIZONTAL)
        in_sizer.Add(self.listPanel, 0, wx.EXPAND)
        in_sizer.Add(self.outputPanel, 1, wx.EXPAND | wx.ALL, 3)
        self.inPanel.SetSizer(in_sizer)

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
        self.buttonPanel.setLabel(label)


class OutputPanel(wx.Panel):
    """
    This class implements an output panel for the scripts.
    """

    def __init__(self, parent):
        """
        Constructor
        """
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self.text = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_MULTILINE | wx.TE_READONLY)
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
    """
    This class implements the list of scripts with checkbox
    """

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

    def checkAll(self):
        for box in self.boxes.values():
            box.SetValue(True)


class ScriptButtonPanel(wx.Panel):
    """
    This panel contains the execute script button.
    """
    LABEL = u"Scripts en attente: "

    def __init__(self, parent):
        """
        Constructor
        """
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self.execute = wx.Button(self, wx.ID_ANY, u"Exécuter")
        self.add = wx.Button(self, wx.ID_ADD, u"Ajouter")
        self.delete = wx.Button(self, wx.ID_REMOVE, u"Supprimer")
        self.label = wx.StaticText(self, wx.ID_ANY, ScriptButtonPanel.LABEL)
        self.addAll = wx.Button(self, wx.ID_ANY, u"Sél. tout")

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.add, 0)
        sizer.Add(self.delete, 0)
        sizer.Add(self.addAll, 0)
        sizer.Add(self.label, 0, wx.ALL | wx.ALIGN_CENTER, 3)
        sizer.AddStretchSpacer(1)
        sizer.Add(self.execute, 0)
        self.SetSizer(sizer)

    def setLabel(self, label=""):
        if not label:
            label = ""
        self.label.SetLabel(ScriptButtonPanel.LABEL + label)


class QuitButtonPanel(wx.Panel):
    """
    This panel contains the quit button of the application.
    """

    def __init__(self, parent):
        """
        Constructor
        """
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self.isAutoQuit = wx.CheckBox(self, wx.ID_ANY, u"Quitter en fin d'exécution")

        self.quit = wx.Button(self, wx.ID_EXIT, u"Quitter")

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddStretchSpacer(1)
        sizer.Add(self.isAutoQuit, 0, wx.CENTER, 3)
        sizer.Add(self.quit, 0, wx.ALL, 3)
        self.SetSizer(sizer)


class MainMenu(wx.MenuBar):
    """
    This class implements the menu of the main window.
    """

    def __init__(self):
        """
        Constructor
        """
        wx.MenuBar.__init__(self)

        file_menu = wx.Menu()
        self.addItem = file_menu.Append(wx.ID_NEW, u"Ajouter", u"Ajouter un nouveau script")
        self.delItem = file_menu.Append(wx.ID_DELETE, u"Supprimer", u"Supprimer les scripts sélectionnés")
        file_menu.AppendSeparator()
        self.qItem = file_menu.Append(wx.ID_EXIT, u"Quitter", u"Quitter l'application")

        about_menu = wx.Menu()
        self.aItem = about_menu.Append(wx.ID_ABOUT, u"A propos", u"Au sujet de l'application")

        self.Append(file_menu, u"&Fichier")
        self.Append(about_menu, u"&Aide")


class AboutDialogWindow(wx.AboutDialogInfo):
    """
    classdocs
    """

    def __init__(self, iconFileName=None):
        """
        Constructor
        """
        wx.AboutDialogInfo.__init__(self)

        self.SetName(u"Info")
        self.SetVersion(u"0.0.1")
        self.SetDescription(u"Programme de gestion et d'exécution de scripts.")
        self.AddDeveloper(u"Alexandre Neuville")
        self.SetCopyright(u"(c) 2012 Alexandre Neuville")
        if iconFileName:
            self.SetIcon(wx.Icon(iconFileName, wx.BITMAP_TYPE_ICO))


class ScriptWindow(wx.Dialog):
    """
    classdoc
    """

    def __init__(self, parent, script=None):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, title=u"Propriété d'un script")

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
    """
    classdoc
    """

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

        in_panel_name = wx.Panel(self, wx.ID_ANY)
        name_label = wx.StaticText(in_panel_name, wx.ID_ANY, u"Nom:")
        self.nameCtrl = wx.TextCtrl(in_panel_name, wx.ID_ANY, name)

        in_sizer_name = wx.BoxSizer(wx.HORIZONTAL)
        in_sizer_name.Add(name_label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        in_sizer_name.Add(self.nameCtrl, 1, wx.EXPAND | wx.LEFT, 3)
        in_panel_name.SetSizer(in_sizer_name)

        in_panel_exec = wx.Panel(self, wx.ID_ANY)
        exec_label = wx.StaticText(in_panel_exec, wx.ID_ANY, u"Exécutable:")
        self.execCtrl = wx.TextCtrl(in_panel_exec, wx.ID_ANY, executable)

        in_sizer_exec = wx.BoxSizer(wx.HORIZONTAL)
        in_sizer_exec.Add(exec_label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)
        in_sizer_exec.Add(self.execCtrl, 1, wx.EXPAND | wx.LEFT, 3)
        in_panel_exec.SetSizer(in_sizer_exec)

        in_panel_args = wx.Panel(self, wx.ID_ANY)
        args_label = wx.StaticText(in_panel_args, wx.ID_ANY, u"Arguments:")
        self.argsCtrl = wx.TextCtrl(in_panel_args, wx.ID_ANY, ' '.join(args))

        in_sizer_args = wx.BoxSizer(wx.VERTICAL)
        in_sizer_args.Add(args_label, 0, wx.BOTTOM | wx.ALIGN_LEFT, 3)
        in_sizer_args.Add(self.argsCtrl, 1, wx.EXPAND)
        in_panel_args.SetSizer(in_sizer_args)

        k_str = []
        for key, value in kwargs.items():
            k_str.append(key + u"=" + value)

        in_panel_kwargs = wx.Panel(self, wx.ID_ANY)
        kwargs_label = wx.StaticText(in_panel_kwargs, wx.ID_ANY, u"Arguments nommés:")
        self.kwargsCtrl = wx.TextCtrl(in_panel_kwargs, wx.ID_ANY, ' '.join(k_str))

        in_sizer_kwargs = wx.BoxSizer(wx.VERTICAL)
        in_sizer_kwargs.Add(kwargs_label, 0, wx.BOTTOM | wx.ALIGN_LEFT, 3)
        in_sizer_kwargs.Add(self.kwargsCtrl, 1, wx.EXPAND)
        in_panel_kwargs.SetSizer(in_sizer_kwargs)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(in_panel_name, 0, wx.ALL | wx.EXPAND, 3)
        sizer.Add(in_panel_exec, 0, wx.ALL | wx.EXPAND, 3)
        sizer.Add(in_panel_args, 0, wx.ALL | wx.EXPAND, 3)
        sizer.Add(in_panel_kwargs, 0, wx.ALL | wx.EXPAND, 3)
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
    """
    classdoc
    """

    def __init__(self, parent):
        """
        Constructor
        """
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self.ok = wx.Button(self, wx.ID_SAVE, u"Sauver")
        self.cancel = wx.Button(self, wx.ID_CANCEL, u"Annuler")

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddStretchSpacer(1)
        sizer.Add(self.ok, 0, wx.BOTTOM | wx.TOP | wx.LEFT, 3)
        sizer.Add(self.cancel, 0, wx.ALL, 3)
        self.SetSizer(sizer)
