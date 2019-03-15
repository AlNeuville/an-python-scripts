from gui import CommandLinePrompt
from model import ScriptFactory


class MainWindowController:
	def __init__(self, root, view, scripts=None):
		if scripts is None:
			scripts = dict()

		self.scripts = scripts
		self.root = root
		self.view = view

		self.view.initialize(self)

	def on_add(self):
		response_view = CommandLinePrompt(self.view)
		response_controller = CommandLineEntryController(response_view)
		response_view.mainloop()

		script = ScriptFactory.create_script(response_controller.script_name, response_controller.command_line)
		self.scripts[script.name] = script
		self.view.add_script(script.name)

	def on_remove(self):
		scripts_names = self.view.remove_scripts()
		for name in scripts_names:
			del self.scripts[name]

	def on_execute(self):
		pass

	def on_exit(self):
		self.root.destroy()


class CommandLineEntryController:
	def __init__(self, view):
		self.script_name = None
		self.command_line = None
		self.view = view
		self.view.initialize(self)

	def on_cancel(self):
		self.view.destroy()

	def on_ok(self):
		self.script_name = self.view.script_name.get()
		self.command_line = self.view.command_line.get()
		self.view.destroy()
