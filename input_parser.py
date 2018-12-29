import config
import utils
import numpy as np

from lab_fit_exception import LabFitException
from calc_input import CalcInput

class InputParser(object):
	"""
	Responsible for parsing any input files or data
	Returns a CalcInput object
	"""
	COLUMN_TYPE = 1
	ROW_TYPE = 2

	def __init__(self, file_path = None, raw_data = None):
		super(InputParser, self).__init__()
		self.file_path = file_path
		self.input = CalcInput()

	def read_input_file(self):
		"""
		Reads input file and stores the data
		at self.raw_data
		"""
		with open(self.file_path, 'r') as f:
			self.raw_data = f.read()

	def parse_raw_data(self, data_type):
		if InputParser.COLUMN_TYPE == data_type:
			self.parse_data_column_type()
		if InputParser.ROW_TYPE == data_type:
			self.parse_data_row_type()
		return False

	def decide_input_data_type(self):
		if self.check_if_column_type():
			return InputParser.COLUMN_TYPE
		if self.check_if_row_type():
			return InputParser.ROW_TYPE
		raise LabFitException("{0} {1}".format(config.INPUT_EXCEPTION_PREFIX, 
											   config.UNKNOWN_FILE_TYPE))

	def check_if_column_type(self):
		"""
		Checks if the raw_data is of column type
		checks first row for all four title names
		"""
		data_lines = self.raw_data.splitlines()
		data_lines = utils.delete_empty_rows(data_lines)

		# Checks if input data is empty
		if len(data_lines) == 0:
			raise LabFitException("{0} {1}".format(config.INPUT_EXCEPTION_PREFIX, 
												   config.EMPTY_INPUT_FILE))

		title_line = data_lines[0].lower()

		for title in title_line.split():
			if title != config.X_COLUMN_NAME and \
			   title != config.X_UNCERTAINTY_COLUMN_NAME and \
			   title != config.Y_COLUMN_NAME and \
			   title != config.Y_UNCERTAINTY_COLUMN_NAME:
			   return False

		return True

	def parse_data_column_type(self):
		"""
		Parses raw_data as a column type
		and insert the data into self.input
		"""
		data_lines = self.raw_data.splitlines()
		data_lines = utils.delete_empty_rows(data_lines)
		titles = data_lines[0].lower().split()

		# Finds data indexes
		for index, title in enumerate(titles):
			if title == config.X_COLUMN_NAME:
				x_index = index
			elif title == config.X_UNCERTAINTY_COLUMN_NAME:
				x_uncertainty_index = index
			elif title == config.Y_COLUMN_NAME:
				y_index = index
			elif title == config.Y_UNCERTAINTY_COLUMN_NAME:
				y_uncertainty_index = index
			else:
				raise LabFitException("{0} {1}".format(config.INPUT_EXCEPTION_PREFIX, 
													   config.UNKNOWN_TITLE))

		x_values = []
		x_uncertainties = []
		y_values = []
		y_uncertainties = []

		# Will hold the amount of rows read
		num_row_read = 0
		# Insert data into self.input object
		for row in data_lines[1:]:
			num_row_read += 1
			# Means end of input
			if row.find(config.AXIS_NAME) != -1:
				break
			data_line_columns = row.split()
			# Checks for unified amount of data
			if len(data_line_columns) != config.MAX_DATA_TYPE_AMOUNT:
				raise LabFitException("{0} {1}".format(config.INPUT_EXCEPTION_PREFIX, 
													   config.DIFFERENT_DATA_AMOUNTS))
			x_values.append(data_line_columns[x_index])
			x_uncertainties.append(data_line_columns[x_uncertainty_index])
			y_values.append(data_line_columns[y_index])
			y_uncertainties.append(data_line_columns[y_uncertainty_index])


		self.input.x_values = np.array(utils.convert_str_list_to_floats(x_values))
		self.input.x_uncertainties = np.array(utils.convert_str_list_to_floats(x_uncertainties))
		self.input.y_values = np.array(utils.convert_str_list_to_floats(y_values))
		self.input.y_uncertainties = np.array(utils.convert_str_list_to_floats(y_uncertainties))

		# Retrieves the x and y axis names
		for row in data_lines[num_row_read:]:
			if row.find(config.X_AXIS_INPUT_STRING) != -1:
				self.input.x_axis_title = row[len(config.X_AXIS_INPUT_STRING):].strip()
			if row.find(config.Y_AXIS_INPUT_STRING) != -1:
				self.input.y_axis_title = row[len(config.Y_AXIS_INPUT_STRING):].strip()

	def check_if_row_type(self):
		"""
		Checks if the raw_data is of row type
		checks first element in the first config.MAX_DATA_TYPE_AMOUNT rows
		"""
		data_lines = self.raw_data.splitlines()
		data_lines = utils.delete_empty_rows(data_lines)
		if len(data_lines) < config.MAX_DATA_TYPE_AMOUNT:
			raise LabFitException("{0} {1}".format(config.INPUT_EXCEPTION_PREFIX, 
													   config.NOT_ENOUGH_DATA_ROWS))

		for row in data_lines[:config.MAX_DATA_TYPE_AMOUNT]:
			data_columns = row.lower()
			title = data_columns.split()[0]
			if title != config.X_COLUMN_NAME and \
			   title != config.X_UNCERTAINTY_COLUMN_NAME and \
			   title != config.Y_COLUMN_NAME and \
			   title != config.Y_UNCERTAINTY_COLUMN_NAME:
			   return False

		return True

	def parse_data_row_type(self):
		"""
		Parses raw_data as a row type
		and insert the data into self.input
		"""
		data_lines = self.raw_data.splitlines()
		data_lines = utils.delete_empty_rows(data_lines)
		for row in data_lines[:config.MAX_DATA_TYPE_AMOUNT]:
			data_columns = row.lower().split()
			title = data_columns[0]
			if title == config.X_COLUMN_NAME:
				self.input.x_values = np.array(utils.convert_str_list_to_floats(data_columns[1:]))
			elif title == config.X_UNCERTAINTY_COLUMN_NAME:
				self.input.x_uncertainties = np.array(utils.convert_str_list_to_floats(data_columns[1:]))
			elif title == config.Y_COLUMN_NAME:
				self.input.y_values = np.array(utils.convert_str_list_to_floats(data_columns[1:]))
			elif title == config.Y_UNCERTAINTY_COLUMN_NAME:
				self.input.y_uncertainties = np.array(utils.convert_str_list_to_floats(data_columns[1:]))
			else:
				raise LabFitException("{0} {1}".format(config.INPUT_EXCEPTION_PREFIX, 
													   config.UNKNOWN_TITLE))

		# Retrieves the x and y axis names
		for row in data_lines[config.MAX_DATA_TYPE_AMOUNT:]:
			if row.find(config.X_AXIS_INPUT_STRING) != -1:
				self.input.x_axis_title = row[len(config.X_AXIS_INPUT_STRING):].strip()
			if row.find(config.Y_AXIS_INPUT_STRING) != -1:
				self.input.y_axis_title = row[len(config.Y_AXIS_INPUT_STRING):].strip()

	def is_valid(self):
		"""
		Checks if self.input is valid
		uses Input object is_valid function
		"""
		self.input.is_valid()

	def start(self):
		self.read_input_file()
		data_type = self.decide_input_data_type()
		self.parse_raw_data(data_type)
		self.is_valid()
		return self.input
		
def main():
	"""
	For Testing purposes
	"""
	try:
		# input_parser = InputParser(file_path = r"C:\studies\computers\inputOutputExamplesGood\inputOutputExamples\workingCols\input.txt")
		input_parser = InputParser(file_path = r"C:\studies\computers\inputOutputExamplesGood\inputOutputExamples\workingRows\input.txt")
		input_parser.start()
		print(input_parser.input)
	except LabFitException as e:
		print(e.message)
	except Exception as e:
		raise
	else:
		pass
	finally:
		pass

if __name__ == '__main__':
	main()