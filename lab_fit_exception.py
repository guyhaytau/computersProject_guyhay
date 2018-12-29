class LabFitException(Exception):
	"""Custom Exception that can be catched in main.py"""
	def __init__(self, message):
		super(LabFitException, self).__init__()
		self.message = message