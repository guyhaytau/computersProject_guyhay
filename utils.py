import copy
import config
from lab_fit_exception import LabFitException

def convert_str_list_to_floats(str_list):
	try:
		return [float(i) for i in str_list]
	except ValueError as e:
		raise LabFitException("{0} {1}".format(config.INPUT_EXCEPTION_PREFIX, 
													   config.INVALID_DATA_VALUE))

def delete_empty_rows(dr, only_begining = False):
	"""
	Deletes empty rows from a list of strings
	only_begining flag is to erase only the row at the begining
	"""
	data_lines = copy.deepcopy(dr)

	while len(data_lines[0]) == 0:
		data_lines = data_lines[1:]

	if only_begining:
		return data_lines

	fixed_data_rows = []
	for row_index in range(len(data_lines)):
		row = data_lines[row_index]
		if len(row) != 0:
			fixed_data_rows.append(row)

	return fixed_data_rows 