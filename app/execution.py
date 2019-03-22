import subprocess
from queue import Queue, Empty
from threading import Thread, Event


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
				args = [script.application] + script.arguments

				callback("Launch '" + ' '.join(args) + "'\n")
				process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
				while True:
					output = process.stdout.readline()
					if output == '' and process.poll() is not None:
						break
					if output:
						callback(output)
				callback("\n")
			except Empty:
				pass
