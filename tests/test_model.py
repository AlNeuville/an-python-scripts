import unittest

from app.model import ScriptFactory, Script


class TestScript(unittest.TestCase):
	def test_create_empty_script(self):
		script = Script("name")

		self.assertEqual("name", script.name)
		self.assertEqual("", script.application)
		self.assertEqual([], script.arguments)

	def test_create_script_with_factory(self):
		script = ScriptFactory.create_script("name", "application args1 args2")

		self.assertEqual("name", script.name)
		self.assertEqual("application", script.application)
		self.assertEqual(["args1", "args2"], script.arguments)
