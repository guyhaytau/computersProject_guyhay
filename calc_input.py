import config
import utils
import numpy as np
from matplotlib import pyplot
from lab_fit_exception import LabFitException

class CalcInput(object):
	"""Holds all the information from the input file"""
	def __init__(self, x_values = None, x_uncertainties = None,
				 y_values = None, y_uncertainties = None, 
				 x_axis_title = config.X_AXIS_DEFAULT, 
				 y_axis_title = config.Y_AXIS_DEFAULT):
		super(CalcInput, self).__init__()
		self.x_values = x_values if x_values != None else [] 
		self.x_uncertainties = x_uncertainties if x_uncertainties != None \
												else []
		self.y_values = y_values if y_values != None else []
		self.y_uncertainties = y_uncertainties if y_uncertainties != None \
												else []
		self.x_axis_title = x_axis_title
		self.y_axis_title = y_axis_title

	def is_valid(self):
		"""
		Checks that the data is valid
		1. Checks same amount of data in x_values, y_values,
		   x_uncertainties, y_uncertainties
		2. Checks all data values are floats
		3. Checks all uncertainty values are above 0
		"""
		# Checks that there is a unified length between data rows
		x_values_length = len(self.x_values)
		if x_values_length != len(self.x_uncertainties) or \
		   x_values_length != len(self.y_values) or \
		   x_values_length != len(self.y_uncertainties):
		   raise LabFitException("{0} {1}".format(config.INPUT_EXCEPTION_PREFIX, 
													   config.DIFFERENT_DATA_AMOUNTS))

		if not np.issubdtype(self.x_uncertainties.dtype, np.number) or \
		   not np.issubdtype(self.x_values.dtype, np.number) or \
		   not np.issubdtype(self.y_uncertainties.dtype, np.number) or \
		   not np.issubdtype(self.y_values.dtype, np.number):
			raise LabFitException("{0} {1}".format(config.INPUT_EXCEPTION_PREFIX, 
													   config.INVALID_DATA_VALUE))
 
		minimum_uncertainty = min(self.x_uncertainties + self.y_uncertainties)
		if minimum_uncertainty <= 0:
			raise LabFitException("{0} {1}".format(config.INPUT_EXCEPTION_PREFIX, 
													   config.INVALID_UNCERTAINTIES))
 

	def __str__(self):
		return "X Values: {0}\n".format(self.x_values) + \
			   "X Uncertainties: {0}\n".format(self.x_uncertainties) + \
			   "Y Values:{0}\n".format(self.y_values) + \
			   "Y Uncertainties:{0}\n".format(self.y_uncertainties) + \
			   "X axis: {0}\n".format(self.x_axis_title) + \
			   "Y axis: {0}\n".format(self.y_axis_title)
