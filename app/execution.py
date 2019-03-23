import subprocess
from queue import Queue, Empty
from threading import Thread, Event


class Executor(Thread):
	def __init__(self, script, callback):
		super().__init__()
		self.args = [script.application] + script.arguments
		self.callback = callback
		self.daemon = True

	def run(self):
		self.callback("Launch '" + ' '.join(self.args) + "'\n")
		# noinspection PyArgumentList
		with subprocess.Popen(
				self.args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True) as process:
			while True:
				line = process.stdout.readline()
				if not line:
					break
				else:
					self.callback(line)
		self.callback("\n")


class ExecutionManager(Thread):
	def __init__(self):
		super().__init__()
		self._stop_event = Event()
		self._queue = Queue()

	def add_execution(self, script, callback):
		self._queue.put((script, callback))

	def stop(self):
		self._stop_event.set()

	def run(self):
		while not self._stop_event.is_set():
			try:
				script, callback = self._queue.get(timeout=0.5)
				executor = Executor(script, callback)
				executor.start()
				executor.join()
			except Empty:
				pass
