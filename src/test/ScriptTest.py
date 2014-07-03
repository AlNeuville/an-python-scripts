#!usr/bin/env python
# -*- coding:utf-8 -*-

'''
Created on 20 juin 2012

@author: Alexandre Neuville
'''


import unittest
import json
from Main.Script import Script, WindowsScript, JsonWindowsScriptDAO, \
                        ScriptServiceFactory


class ScriptTest(unittest.TestCase):
    def testSequenceOnlyArgs(self):
        script = Script("monScript", "boum.sh", "arg1", "arg2")
        assert script
        print script

    def testDictionnaryOnlyArgs(self):
        script = Script("monScript", "boum.sh", arg1="a", arg2="b")
        assert script
        print script

    def testCompleteArgs(self):
        script = Script("monScript", "boum.sh", "arg1", "arg2", arg3="a",
                arg4="b")
        assert script
        print script

    def testEmptyScript(self):
        script = Script("empty")
        assert script
        print script

    def testAddArguments(self):
        script = Script("monScript", "boum.sh")

        script.addArg("arg1")
        script.addArg("a", "arg2")

        assert script
        print script


class WindowsScriptTest(unittest.TestCase):
    def testSequenceOnlyArgs(self):
        script = WindowsScript("monScript", "boum.sh", "arg1", "arg2")
        rStr = script.toExecutableString()

        assert rStr == "boum.sh arg1 arg2", "Problem with " + rStr
        print rStr

    def testDictionnaryOnlyArgs(self):
        script = WindowsScript("monScript", "boum.sh", arg1="a", arg2="b")
        rStr = script.toExecutableString()

        assert rStr == "boum.sh -arg1=a -arg2=b", "Problem with " + rStr
        print rStr

    def testCompleteArgs(self):
        script = WindowsScript("monScript", "boum.sh", "arg1", "arg2",
                arg3="a", arg4="b")
        rStr = script.toExecutableString()

        assert rStr == "boum.sh arg1 arg2 -arg3=a -arg4=b", \
                        "Problem with " + rStr
        print rStr

    def testEmptyScript(self):
        script = WindowsScript("empty", "boum.sh")
        rStr = script.toExecutableString()

        assert rStr == "boum.sh", "Script not empty"
        print rStr

    def testAddArguments(self):
        script = WindowsScript("monScript", "boum.sh")
        script.addArg("arg1")
        script.addArg("a", "arg2")
        rStr = script.toExecutableString()

        assert rStr == "boum.sh arg1 -arg2=a", "Problem with" + rStr
        print rStr


class JsonDAOTest(unittest.TestCase):
    parameters = {"fileName": "resources/ScriptTest.json"}

    def testGetWindowsScript(self):
        dao = JsonWindowsScriptDAO(**self.parameters)
        script = dao.getScript("monScript")
        rStr = script.toExecutableString()

        assert rStr == "boum.sh arg1 -arg2=a", "Problem with " + rStr
        print "Loaded script: ", script

    def testGetAllWindowsScript(self):
        dao = JsonWindowsScriptDAO(**self.parameters)
        scripts = dao.getScripts()
        for script in scripts:
            rStr = script.toExecutableString()
            assert rStr
            print "Loaded script: ", script

    def testSaveScript(self):
        script = WindowsScript("savedScript", "boum.sh", "args1", arg2="b")
        dao = JsonWindowsScriptDAO(**self.parameters)

        assert dao.saveScript(script) == True, "Script not saved"
        print "Script saved"


class ScriptServiceTest(unittest.TestCase):
    configFile = "resources/ScriptServiceTestConfig.json"

    def setUp(self):
        with open(self.configFile) as f:
            parameters = json.load(f, encoding=f.encoding)
            self.factory = ScriptServiceFactory(**parameters)

    def runTest(self):
        service = self.factory.service
        assert service
        print service

        script = service.getScript("monScript")
        assert script
        print script

        scripts = service.getScripts()
        assert scripts
        for key, value in scripts.items():
            print key, ": ", value

        assert service.saveScript(script, "json") == True, "Script not saved"
        print "Script saved"

        assert service.saveScript(script) == True, \
                                                "Script without ns not saved"
        print "Script saved"
