class CalcInput(object):
	"""Holds all the information from the input file"""
	def __init__(self, x_values = None, x_uncertainties = None,
				 y_values = None, y_uncertainties = None):
		super(CalcInput, self).__init__()
		self.x_values = x_values if x_values != None else [] 
		self.x_uncertainties = x_uncertainties if x_uncertainties != None \
												else []
		self.y_values = y_values if y_values != None else []
		self.y_uncertainties = y_uncertainties if y_uncertainties != None \
												else []

	def __str__(self):
		return "X Values: {0}\n".format(self.x_values) + \
			   "X Uncertainties: {0}\n".format(self.x_uncertainties) + \
			   "Y Values:{0}\n".format(self.y_values) + \
			   "Y Uncertainties:{0}\n".format(self.y_uncertainties)
