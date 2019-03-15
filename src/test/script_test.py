#!usr/bin/env python
# -*- coding:utf-8 -*-

"""
Created on 20 juin 2012

@author: Alexandre Neuville
"""

import unittest
import json
from script import Script, WindowsScript, JsonWindowsScriptDAO, ScriptServiceFactory


class ScriptTest(unittest.TestCase):
    def testSequenceOnlyArgs(self):
        script = Script("monScript", "boum.sh", "arg1", "arg2")
        self.assertIsNotNone(script)
        print(script)

    def testDictionnaryOnlyArgs(self):
        script = Script("monScript", "boum.sh", arg1="a", arg2="b")
        self.assertIsNotNone(script)
        print(script)

    def testCompleteArgs(self):
        script = Script("monScript", "boum.sh", "arg1", "arg2", arg3="a",
                        arg4="b")
        self.assertIsNotNone(script)
        print(script)

    def testEmptyScript(self):
        script = Script("empty")
        self.assertIsNotNone(script)
        print(script)

    def testAddArguments(self):
        script = Script("monScript", "boum.sh")

        script.addArg("arg1")
        script.addArg("a", "arg2")

        self.assertIsNotNone(script)
        print(script)


class WindowsScriptTest(unittest.TestCase):
    
    def testSequenceOnlyArgs(self):
        script = WindowsScript("monScript", "boum.sh", "arg1", "arg2")
        r_str = script.toExecutableString()

        self.assertEqual("cmd /C boum.sh arg1 arg2", r_str)
        print(r_str)

    def testDictionnaryOnlyArgs(self):
        script = WindowsScript("monScript", "boum.sh", arg1="a", arg2="b")
        r_str = script.toExecutableString()

        self.assertEqual("cmd /C boum.sh -arg1=a -arg2=b", r_str)
        print(r_str)

    def testCompleteArgs(self):
        script = WindowsScript("monScript", "boum.sh", "arg1", "arg2", arg3="a", arg4="b")
        r_str = script.toExecutableString()

        self.assertEqual("cmd /C boum.sh arg1 arg2 -arg3=a -arg4=b", r_str)
        print(r_str)

    def testEmptyScript(self):
        script = WindowsScript("empty", "boum.sh")
        r_str = script.toExecutableString()

        self.assertEqual("cmd /C boum.sh", r_str)
        print(r_str)

    def testAddArguments(self):
        script = WindowsScript("monScript", "boum.sh")
        script.addArg("arg1")
        script.addArg("a", "arg2")
        r_str = script.toExecutableString()

        self.assertEqual("cmd /C boum.sh arg1 -arg2=a", r_str)
        print(r_str)


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

        self.assertEqual("cmd /C boum.sh arg1 -arg2=a", r_str)
        print("Loaded script: ", script)

    def testGetAllWindowsScript(self):
        dao = JsonWindowsScriptDAO(**self.parameters)
        scripts = dao.getScripts()
        for script in scripts:
            r_str = script.toExecutableString()
            self.assertIsNotNone(r_str)
            print("Loaded script: ", script)

    def testSaveScript(self):
        script = WindowsScript("savedScript", "boum.sh", "args1", arg2="b")
        dao = JsonWindowsScriptDAO(**self.parameters)

        self.assertTrue(dao.saveScript(script))
        print("Script saved")


class ScriptServiceTest(unittest.TestCase):
    def setUp(self):
        with open("resources/ScriptServiceTestConfig.json") as f:
            parameters = json.load(f, encoding=f.encoding)
            self.factory = ScriptServiceFactory(**parameters)

    def runTest(self):
        service = self.factory.service
        self.assertIsNotNone(service)
        print(service)

        script = service.getScript("monScript")
        self.assertIsNotNone(script)
        print(script)

        scripts = service.getScripts()
        self.assertIsNotNone(scripts)
        for key, value in scripts.items():
            print(key, ": ", value)

        self.assertTrue(service.saveScript(script, "json"))
        print("Script saved")

        self.assertTrue(service.saveScript(script))
        print("Script saved")
