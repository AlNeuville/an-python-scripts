#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Created on 20 juin 2012

@author: Alexandre Neuville
"""

import json
import sys


class Error(Exception):
    """
    General error class for the Script module.
    """
    pass


class ParameterError(Error):
    """
    Configuration error (missing parameter, unknown parameter, etc).
    """
    pass


class UnknownNameSpaceError(Error):
    """
    An unknown DAO is found or no DAO is found.
    """
    pass


class Script:
    """
    This class contains a general script.
    """

    def __init__(self, name, executable=None, *args, **kwargs):
        """
        Constructor

        @param name: executable name of the script
        @param *args: sequence with the script unnamed arguments
        @param **kwargs: dictionnary with the script named arguments
        """
        self.args = args
        self.name = name
        self.kwargs = kwargs
        self.executable = executable

        if not self.args:
            self.args = []
        if not self.kwargs:
            self.kwargs = {}

    def addArg(self, arg, name=None):
        """
        This method add an arguments in the script call. This argument can be
        named or unnamed.

        @param arg: argument
        @param name: name of the argument
        """

        if name:
            self.kwargs.setdefault(name, arg)
        else:
            self.args.append(arg)

    def __repr__(self):
        ret_str = ["Script: {name: ", self.name, ", executable: "]
        if self.executable:
            ret_str.append(self.executable)
        else:
            ret_str.append('<None>')
        ret_str.append(", args: ")
        ret_str.append(str(self.args))
        ret_str.append(", kwargs: ")
        ret_str.append(str(self.kwargs))
        ret_str.append("}")
        return ''.join(ret_str)

    def __str__(self):
        return self.__repr__()


class WindowsScript(Script):
    """
    This class contains a Windows script.
    """

    def __init__(self, name, *args, **kwargs):
        """
        Constructor

        @see: the documentation of the parent class constructor
        """
        Script.__init__(self, name, *args, **kwargs)

    def toExecutableString(self):
        """
        This method return the general executable command that can be sent to
        Windows.

        @return: the executable string
        """
        str_list = [u"cmd", u"/C"]
        if self.executable:
            str_list.append(self.executable)
        else:
            str_list.append(self.name)

        for arg in self.args:
            str_list.append(arg)

        keys = sorted(self.kwargs.keys())
        for k in keys:
            str_list.append('-' + k + '=' + self.kwargs[k])

        return ' '.join(str_list)


class JsonWindowsScriptDAO:
    """
    This DAO interacts with a JSON file to extract or save messages.
    """

    def __init__(self, **parameters):
        """
        Constructor

        @param **parameters: dictionnary of parameters. 'fileName' is
        mandatory.
        @raise ParameterError: if 'fileName' is not found in the parameters
        dictionnary
        """

        if not parameters or "fileName" not in parameters:
            raise ParameterError("Parameter 'fileName' not found")
        self.fileName = parameters["fileName"]
        self.encoding = "utf8"
        if "encoding" in parameters:
            self.encoding = parameters["encoding"]

        with open(self.fileName) as f:
            self.messages = json.load(f, encoding=self.encoding)

    def getScript(self, name):
        """
        This method returns the named script in the json file.

        @param name: script name
        @return: named script or None if not found
        """

        if not name:
            return None

        script = self.messages.get(name, None)
        if not script:
            return None

        executable = script.get("executable", None)
        args = script.get("args", [])
        kwargs = script.get("kwargs", {})

        return WindowsScript(name, executable, *args, **kwargs)

    def getScripts(self):
        """
        This method returns a sequence of all the messages known by the dao.

        @return: a sequence of messages or an empty sequence.
        """

        scripts = []
        for key in self.messages.keys():
            args = self.messages[key].get("args", [])
            kwargs = self.messages[key].get("kwargs", {})
            executable = self.messages[key].get("executable", None)
            script = WindowsScript(key, executable, *args, **kwargs)
            scripts.append(script)

        return scripts

    def saveScript(self, script):
        """
        This method saves a script in the json file.

        @param script: script that must be saved
        @return: False if an error occurs or if script is 'None'.
        """

        if not script:
            return False

        args = {}
        if script.executable:
            args.setdefault("executable", script.executable)
        if script.kwargs:
            args.setdefault("kwargs", script.kwargs)
        if script.args:
            args.setdefault("args", script.args)
        self.messages.setdefault(script.name, args)

        with open(self.fileName, "w") as f:
            json.dump(self.messages, f, indent=4, encoding=self.encoding)

        return True

    def deleteScript(self, script):
        """
        This method removes a script in the json file.

        @param script: the script that must be removed
        """
        if not script or script.name not in self.messages:
            return

        del self.messages[script.name]
        with open(self.fileName, "w") as f:
            json.dump(self.messages, f, indent=4, encoding=self.encoding)


class ScriptService:
    """
    This class implements a Script service
    """

    def __init__(self, **parameters):
        """
        Constructor
        """

        if not parameters or "daos" not in parameters:
            raise ParameterError("Parameter 'daos' not found")

        self.nsdaos = {}
        self.daos = []
        for dao in parameters["daos"]:
            if "className" not in dao:
                raise ParameterError(
                    "Parameter 'className' not found in dao configuration")

            dao_name = dao["className"]
            nspc = dao.get("namespace", None)

            names = dao_name.split('.')
            obj = getattr(sys.modules[__name__], names[-1])(**dao)
            if nspc:
                self.nsdaos.setdefault(nspc, obj)
            self.daos.append(obj)

    def getScript(self, name, nspc=None):
        """
        This method returns the named script in the specified namespace or
        in all the known daos. It returns None if no script is found.

        @param name: name of the script
        @param nspc: namespace
        """
        if nspc:
            return self.nsdaos[nspc].getScript(name)

        for dao in self.daos:
            script = dao.getScript(name)
            if script:
                return script

        return None

    def getScripts(self):
        """
        This method returns all the messages found in the daos.

        @return: a dictionary with all the known messages.
        """

        scripts = {}
        for dao in self.daos:
            for script in dao.getScripts():
                scripts.setdefault(script.name, script)

        return scripts

    def saveScript(self, script, nspc=None):
        """
        This method saves the given script into the given namespace.

        @param script: the script that must be saved
        @param nspc: namespace
        @return: False if an error occurs, True otherwise
        @raise UnknownNameSpaceError: if more than one namespace are configured
        and no namespace is specified
        """
        if not nspc and len(self.daos) == 1:
            return self.daos[0].saveScript(script)
        elif not nspc:
            raise UnknownNameSpaceError("Namespace not specified")

        return self.nsdaos[nspc].saveScript(script)

    def deleteScript(self, script, nspc=None):
        """
        This method removes a script.

        @param script: the script that must be removed
        @param nspc: the namespace where find the script
        """
        if nspc:
            self.nsdaos[nspc].deleteScript(script)
        else:
            for dao in self.daos:
                dao.deleteScript(script)

    def __repr__(self):
        str_list = ["Service: ", str(self.__class__), ": {daos: ", str(self.daos), "}"]
        return ''.join(str_list)

    def __str__(self):
        return self.__repr__()


class ScriptServiceFactory:
    """
    This class is the factory that builds ScriptService instance.
    """

    def __init__(self, **parameters):
        if not parameters or "className" not in parameters:
            raise ParameterError("Parameter 'className' not found")

        names = parameters["className"].split('.')
        self.__service = getattr(sys.modules[__name__],
                                 names[-1])(**parameters)

    @property
    def service(self):
        """
        The __service property (getter)
        """
        return self.__service
