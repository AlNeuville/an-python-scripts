class Script:
	def __init__(self, name):
		self.name = name
		self.application = ''
		self.arguments = []

	def to_command_line(self):
		command = [self.application] + self.arguments
		return ' '.join(command)

	def __str__(self):
		return "Script{name=" + self.name + ",application=" + self.application + ",arguments=" + str(
			self.arguments) + "}"


class ScriptFactory:
	@staticmethod
	def create_script(name, command_line):
		parts = command_line.split(' ')
		script = Script(name)
		script.application = parts[0]
		script.arguments = parts[1:]
		return script
