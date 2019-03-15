from tkinter import Frame, Button, RIGHT, LEFT, BOTTOM, TOP, LabelFrame, BOTH, Listbox, Text, X, Y, SINGLE, Toplevel, \
	Entry, StringVar, END, MULTIPLE


class MainWindow(Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.script_list = None

	def initialize(self, controller):
		self.pack()

		main_panel = Frame(self)
		main_panel.pack(expand=True, fill=BOTH)

		script_panel = LabelFrame(main_panel, text="Scripts")
		script_panel.pack(side=LEFT, expand=True, fill=Y, padx=5, pady=5)

		self.script_list = Listbox(script_panel, selectmode=MULTIPLE)
		self.script_list.pack(side=TOP, expand=True, fill=BOTH, padx=5, pady=5)
		Button(script_panel, text="Exécuter", command=controller.on_execute).pack(side=BOTTOM, padx=5, pady=5)
		Button(script_panel, text="Supprimer", command=controller.on_remove).pack(side=BOTTOM, padx=5, pady=5)
		Button(script_panel, text="Ajouter", command=controller.on_add).pack(side=BOTTOM, padx=5, pady=5)

		console_panel = LabelFrame(main_panel, text="Console")
		console_panel.pack(side=RIGHT, expand=True, fill=BOTH, padx=5, pady=5)

		Text(console_panel, bg="black", fg="white").pack(expand=True, fill=BOTH, padx=5, pady=5)

		bottom_panel = Frame(self)
		bottom_panel.pack(side=BOTTOM, expand=True, fill=X)

		Button(bottom_panel, text="Quitter", command=controller.on_exit).pack(side=RIGHT, padx=5, pady=5)

	def add_script(self, script_name):
		self.script_list.insert(END, script_name)

	def remove_scripts(self):
		script_indexes = self.script_list.curselection()
		script_names = [self.script_list.get(index) for index in script_indexes]
		for index in script_indexes:
			self.script_list.delete(index)
		return script_names


class CommandLinePrompt(Toplevel):
	def __init__(self, master):
		super().__init__(master)
		self.script_name = StringVar('')
		self.command_line = StringVar('')
		self.frame = LabelFrame(self, text="Ligne de commande")
		self.frame.pack(expand=True, fill=BOTH, padx=5, pady=5)

	def initialize(self, controller):
		Entry(self.frame, textvariable=self.script_name).pack(expand=True, fill=X, padx=5, pady=5)
		Entry(self.frame, textvariable=self.command_line).pack(expand=True, fill=X, padx=5)
		Button(self.frame, text="Annuler", command=controller.on_cancel).pack(side=RIGHT, padx=5, pady=5)
		Button(self.frame, text="Ok", command=controller.on_ok).pack(side=RIGHT, padx=5, pady=5)
