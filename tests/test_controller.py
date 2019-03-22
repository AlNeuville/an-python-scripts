from tkinter import Tk, StringVar
from unittest import TestCase
from unittest.mock import MagicMock, patch

from app.controller import MainWindowController, CommandLineEntryController
from app.gui import MainWindow, CommandLinePrompt
from app.model import ScriptFactory


class TestMainWindowController(TestCase):
	def setUp(self):
		self.mocked_tk = MagicMock(Tk)
		self.mocked_view = MagicMock(MainWindow)
		self.controller = MainWindowController(self.mocked_tk, self.mocked_view)

	def test_init_creation(self):
		self.assertEqual(self.mocked_tk, self.controller.root)
		self.assertEqual(self.mocked_view, self.controller.view)
		self.assertDictEqual({}, self.controller.scripts)

	def test_exit(self):
		self.controller.on_exit()
		self.mocked_tk.destroy.assert_called_once()

	def test_remove_script(self):
		script = ScriptFactory.create_script("name", "application args")
		self.controller.scripts.setdefault(script.name, script)
		self.mocked_view.get_selected_script_names.return_value = ["name"]

		self.controller.on_remove()

		self.assertDictEqual({}, self.controller.scripts)

	@patch('app.controller.CommandLinePrompt')
	@patch('app.controller.CommandLineEntryController')
	def test_add_script(self, mocked_prompt_controller, _mocked_prompt_view):
		mocked_prompt_controller.return_value.canceled = False
		mocked_prompt_controller.return_value.script_name = "name"
		mocked_prompt_controller.return_value.command_line = "application args"

		self.controller.on_add()

		self.assertEqual(1, len(self.controller.scripts))

	def test_display_result(self):
		self.controller.display_result("result")

		self.mocked_view.display_script_result.assert_called_once_with("result")


class TestCommandLineEntryController(TestCase):
	def setUp(self):
		self.mocked_view = MagicMock(CommandLinePrompt)
		self.controller = CommandLineEntryController(self.mocked_view)

	def test_on_cancel(self):
		self.controller.on_cancel()

		self.assertTrue(self.controller.canceled)
		self.mocked_view.destroy.assert_called_once()

	def test_on_ok(self):
		mocked_script_name = MagicMock(StringVar)
		mocked_script_name.get.return_value = "name"
		mocked_command_line = MagicMock(StringVar)
		mocked_command_line.get.return_value = "application args"
		self.mocked_view.script_name = mocked_script_name
		self.mocked_view.command_line = mocked_command_line

		self.controller.on_ok()

		self.assertEqual("name", self.controller.script_name)
		self.assertEqual("application args", self.controller.command_line)
		mocked_command_line.get.assert_called_once()
		mocked_script_name.get.assert_called_once()
		self.mocked_view.destroy.assert_called_once()
