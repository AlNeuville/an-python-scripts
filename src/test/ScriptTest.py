#!usr/bin/env python
# -*- coding:utf-8 -*-

"""
Created on 20 juin 2012

@author: Alexandre Neuville
"""

import unittest
import json
from Script import Script, WindowsScript, JsonWindowsScriptDAO, ScriptServiceFactory


class ScriptTest(unittest.TestCase):
    @staticmethod
    def testSequenceOnlyArgs():
        script = Script("monScript", "boum.sh", "arg1", "arg2")
        assert script
        print script

    @staticmethod
    def testDictionnaryOnlyArgs():
        script = Script("monScript", "boum.sh", arg1="a", arg2="b")
        assert script
        print script

    @staticmethod
    def testCompleteArgs():
        script = Script("monScript", "boum.sh", "arg1", "arg2", arg3="a",
                        arg4="b")
        assert script
        print script

    @staticmethod
    def testEmptyScript():
        script = Script("empty")
        assert script
        print script

    @staticmethod
    def testAddArguments():
        script = Script("monScript", "boum.sh")

        script.addArg("arg1")
        script.addArg("a", "arg2")

        assert script
        print script


class WindowsScriptTest(unittest.TestCase):
    @staticmethod
    def testSequenceOnlyArgs():
        script = WindowsScript("monScript", "boum.sh", "arg1", "arg2")
        r_str = script.toExecutableString()

        assert r_str == "cmd /C boum.sh arg1 arg2", "Problem with " + r_str
        print r_str

    @staticmethod
    def testDictionnaryOnlyArgs():
        script = WindowsScript("monScript", "boum.sh", arg1="a", arg2="b")
        r_str = script.toExecutableString()

        assert r_str == "cmd /C boum.sh -arg1=a -arg2=b", "Problem with " + r_str
        print r_str

    @staticmethod
    def testCompleteArgs():
        script = WindowsScript("monScript", "boum.sh", "arg1", "arg2", arg3="a", arg4="b")
        r_str = script.toExecutableString()

        assert r_str == "cmd /C boum.sh arg1 arg2 -arg3=a -arg4=b", "Problem with " + r_str
        print r_str

    @staticmethod
    def testEmptyScript():
        script = WindowsScript("empty", "boum.sh")
        r_str = script.toExecutableString()

        assert r_str == "cmd /C boum.sh", "Script not empty"
        print r_str

    @staticmethod
    def testAddArguments():
        script = WindowsScript("monScript", "boum.sh")
        script.addArg("arg1")
        script.addArg("a", "arg2")
        r_str = script.toExecutableString()

        assert r_str == "cmd /C boum.sh arg1 -arg2=a", "Problem with " + r_str
        print r_str


class JsonDAOTest(unittest.TestCase):
    parameters = {"fileName": "resources/ScriptTest.json"}

    def setUp(self):
        dao = JsonWindowsScriptDAO(**self.parameters)
        script = Script("monScript", "boum.sh", "arg1", arg2="a")
        dao.saveScript(script)

    def testGetWindowsScript(self):
        dao = JsonWindowsScriptDAO(**self.parameters)
        script = dao.getScript("monScript")
        r_str = script.toExecutableString()

        assert r_str == "cmd /C boum.sh arg1 -arg2=a", "Problem with " + r_str
        print "Loaded script: ", script

    def testGetAllWindowsScript(self):
        dao = JsonWindowsScriptDAO(**self.parameters)
        scripts = dao.getScripts()
        for script in scripts:
            r_str = script.toExecutableString()
            assert r_str
            print "Loaded script: ", script

    def testSaveScript(self):
        script = WindowsScript("savedScript", "boum.sh", "args1", arg2="b")
        dao = JsonWindowsScriptDAO(**self.parameters)

        assert dao.saveScript(script) is True, "Script not saved"
        print "Script saved"


class ScriptServiceTest(unittest.TestCase):
    def setUp(self):
        with open("resources/ScriptServiceTestConfig.json") as f:
            parameters = json.load(f, encoding=f.encoding)
            self.factory = ScriptServiceFactory(**parameters)

    def runTest(self):
        service = self.factory.service
        assert service is not None, "service is None"
        print service

        script = service.getScript("monScript")
        assert script is not None, "script is None"
        print script

        scripts = service.getScripts()
        assert scripts
        for key, value in scripts.items():
            print key, ": ", value

        assert service.saveScript(script, "json") is True, "Script not saved"
        print "Script saved"

        assert service.saveScript(script) is True, "Script without ns not saved"
        print "Script saved"
