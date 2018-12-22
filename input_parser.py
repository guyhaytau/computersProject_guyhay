import config
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
		at self.raw_data parameter
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
		return False

	def check_if_column_type(self):
		"""
		Checks if the raw_data is of column type
		checks first row for all four title names
		"""
		data_lines = self.raw_data.splitlines()
		if len(data_lines) == 0:
			import pdb; pdb.set_trace()
			raise "SSSSSSSSS"

		title_line = data_lines[0].lower()
		if title_line.find(config.X_COLUMN_NAME) == -1 or \
		   title_line.find(config.X_UNCERTAINTY_COLUMN_NAME) == -1 or \
		   title_line.find(config.Y_COLUMN_NAME) == -1 or \
		   title_line.find(config.Y_UNCERTAINTY_COLUMN_NAME) == -1:
		   return False

		return True

	def parse_data_column_type(self):
		"""
		Parses raw_data as a column type
		and insert the data into self.input
		"""
		data_lines = self.raw_data.splitlines()
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
				import pdb; pdb.set_trace()
				raise "SSSSSSSSSSSss"

		# Insert data into self.input object
		for row in data_lines[1:]:
			if len(row) == 0 or row.find(config.AXIS_NAME) != -1:
				break
			data_line_columns = row.split()
			self.input.x_values.append(data_line_columns[x_index])
			self.input.x_uncertainties.append(
									data_line_columns[x_uncertainty_index])
			self.input.y_values.append(data_line_columns[y_index])
			self.input.y_uncertainties.append(
									data_line_columns[y_uncertainty_index])

	def check_if_row_type(self):
		"""
		Checks if the raw_data is of row type
		checks first element in the first config.MAX_DATA_TYPE_AMOUNT rows
		"""
		data_lines = self.raw_data.splitlines()
		if len(data_lines) == config.MAX_DATA_TYPE_AMOUNT:
			import pdb; pdb.set_trace()
			raise "SSSSSSSSS"

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
		for row in data_lines[:config.MAX_DATA_TYPE_AMOUNT]:
			data_columns = row.lower().split()
			title = data_columns[0]
			if title == config.X_COLUMN_NAME:
				self.input.x_values.extend(data_columns[1:]) 
			elif title == config.X_UNCERTAINTY_COLUMN_NAME:
				self.input.x_uncertainties.extend(data_columns[1:])
			elif title == config.Y_COLUMN_NAME:
				self.input.y_values.extend(data_columns[1:])
			elif title == config.Y_UNCERTAINTY_COLUMN_NAME:
				self.input.y_uncertainties.extend(data_columns[1:])
			else:
				import pdb; pdb.set_trace()
				raise "SSSSSSSSSSSss"

		print("all good")

	def is_valid(self):
		"""
		Checks if self.input is valid
		"""
		x_values_length = len(self.input.x_values)
		if x_values_length != len(self.input.x_uncertainties) or \
		   x_values_length != len(self.input.y_values) or \
		   x_values_length != len(self.input.y_uncertainties):
		   raise "SSSSSSSSSS"
		print("Todo bien senor")

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
	# input_parser = InputParser(file_path = r"C:\studies\computers\inputOutputExamples\workingCols\input.txt")
	input_parser = InputParser(file_path = r"C:\studies\computers\inputOutputExamples\workingRows\input.txt")
	input_parser.start()

if __name__ == '__main__':
	main()