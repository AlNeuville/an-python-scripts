from app.execution import ExecutionManager
from app.gui import CommandLinePrompt
from app.model import ScriptFactory


class MainWindowController:
	def __init__(self, root, view, scripts=None):
		if scripts is None:
			scripts = dict()

		self.root = root
		self.view = view
		self.scripts = scripts
		self.execution_manager = ExecutionManager()
		self.execution_manager.start()

		self.view.initialize(self)

		for script_name, script in self.scripts:
			self.view.insert_script_name(script_name)

	def on_add(self):
		response_view = CommandLinePrompt(self.view)
		response_controller = CommandLineEntryController(response_view)
		self.view.wait_window(response_view)

		if not response_controller.canceled:
			script = ScriptFactory.create_script(
				response_controller.script_name, response_controller.command_line)
			self.scripts[script.name] = script
			self.view.insert_script_name(script.name)

	def on_remove(self):
		scripts_names = self.view.get_selected_script_names()
		for name in scripts_names:
			del self.scripts[name]
			self.view.delete_script_name(name)

	def on_execute(self):
		script_names = self.view.get_selected_script_names()
		scripts = [self.scripts[name] for name in script_names]
		for script in scripts:
			self.execution_manager.add_execution(script, self.display_result)

	def display_result(self, result):
		self.view.display_script_result(result)

	def on_exit(self):
		if self.execution_manager.is_alive():
			self.execution_manager.stop()
			self.execution_manager.join()
		self.root.destroy()


class CommandLineEntryController:
	def __init__(self, view):
		self.canceled = False
		self.script_name = None
		self.command_line = None
		self.view = view
		self.view.initialize(self)

	def on_cancel(self):
		self.canceled = True
		self.view.destroy()

	def on_ok(self):
		self.script_name = self.view.script_name.get()
		self.command_line = self.view.command_line.get()
		self.view.destroy()
