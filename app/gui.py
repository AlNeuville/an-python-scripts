from tkinter import Frame, Button, RIGHT, LEFT, BOTTOM, TOP, LabelFrame, BOTH, Listbox, Text, X, Y, Toplevel, \
	Entry, END, StringVar, SINGLE, Scrollbar


class MainWindow(Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.listbox = None
		self.console = None

	def initialize(self, controller):
		self.pack()

		main_panel = Frame(self)
		main_panel.pack(expand=True, fill=BOTH)

		script_panel = LabelFrame(main_panel, text="Scripts")
		script_panel.pack(side=LEFT, expand=True, fill=Y, padx=5, pady=5)

		listbox_panel = Frame(script_panel)
		listbox_panel.pack(side=TOP, fill=BOTH, expand=True)

		self.listbox = Listbox(listbox_panel, selectmode=SINGLE)
		self.listbox.pack(side=LEFT, expand=True, fill=BOTH, padx=5, pady=5)
		listbox_scrollbar = Scrollbar(listbox_panel, command=self.listbox.yview)
		listbox_scrollbar.pack(side=RIGHT, fill=Y, pady=5)
		self.listbox.configure(yscrollcommand=listbox_scrollbar.set)

		button_size = 9
		button_panel = Frame(script_panel)
		button_panel.pack(side=BOTTOM, fill=X)
		Button(button_panel, text="Ajouter", command=controller.on_add, width=button_size).grid(
			row=0, column=0, padx=5)
		Button(button_panel, text="Supprimer", command=controller.on_remove, width=button_size).grid(
			row=0, column=1, padx=5)
		Button(button_panel, text="Exécuter", command=controller.on_execute, width=button_size).grid(
			row=1, column=0, padx=5, pady=5)

		console_panel = LabelFrame(main_panel, text="Console")
		console_panel.pack(side=RIGHT, expand=True, fill=BOTH, padx=5, pady=5)

		self.console = Text(console_panel, bg="black", fg="white")
		self.console.pack(side=LEFT, expand=True, fill=BOTH, padx=5, pady=5)
		console_scrollbar = Scrollbar(console_panel, command=self.console.yview)
		console_scrollbar.pack(side=RIGHT, fill=Y)
		self.console.configure(yscrollcommand=console_scrollbar.set)

		bottom_panel = Frame(self)
		bottom_panel.pack(side=BOTTOM, expand=True, fill=X)

		Button(bottom_panel, text="Quitter", command=controller.on_exit).pack(side=RIGHT, padx=5, pady=5)

	def insert_script_name(self, script_name):
		self.listbox.insert(END, script_name)

	def get_selected_script_names(self):
		script_indexes = self.listbox.curselection()
		return [self.listbox.get(index) for index in script_indexes]

	def delete_script_name(self, script_name):
		index = self.listbox.get(0, END).index(script_name)
		self.listbox.delete(index)

	def display_script_result(self, result):
		self.console.insert(END, result)


class CommandLinePrompt(Toplevel):
	def __init__(self, master):
		super().__init__(master)
		self.transient(master)
		self.grab_set()

		self.script_name = StringVar()
		self.command_line = StringVar()

		self.frame = LabelFrame(self, text="Ligne de commande")
		self.frame.pack(expand=True, fill=BOTH, padx=5, pady=5)

	def initialize(self, controller):
		Entry(self.frame, textvariable=self.script_name).pack(expand=True, fill=X, padx=5, pady=5)
		Entry(self.frame, textvariable=self.command_line).pack(expand=True, fill=X, padx=5)
		Button(self.frame, text="Annuler", command=controller.on_cancel).pack(side=RIGHT, padx=5, pady=5)
		Button(self.frame, text="Ok", command=controller.on_ok).pack(side=RIGHT, padx=5, pady=5)
