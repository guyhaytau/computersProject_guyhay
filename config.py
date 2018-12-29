X_COLUMN_NAME = 'x'
X_UNCERTAINTY_COLUMN_NAME = 'dx'
Y_COLUMN_NAME = 'y'
Y_UNCERTAINTY_COLUMN_NAME = 'dy'
AXIS_NAME = 'axis'
MAX_DATA_TYPE_AMOUNT = 4
X_AXIS_INPUT_STRING = 'x axis:'
Y_AXIS_INPUT_STRING = 'y axis:'
X_AXIS_DEFAULT = 'x axis'
Y_AXIS_DEFAULT = 'y axis'

# The output format for the linear fit
# 0 - a value
# 1 - a uncertainty
# 2 - b value
# 3 - b uncertainty
# 4 - chi2 value
# 5 - chi2 uncertainty
LINEAR_OUTPUT_FORMAT = """
a = {0}+-{1}
b = {2}+-{3}
chi2 = {4}
chi2_reduced = {5}
"""
LINEAR_PLOT_FILE_NAME = "linear_fit"

# Error Strings
INPUT_EXCEPTION_PREFIX = "Input file error:"
UNKNOWN_TITLE = "Found unknown title."
EMPTY_INPUT_FILE = "Input file is empty."
NOT_ENOUGH_DATA_ROWS = "Not enough data rows."
UNKNOWN_FILE_TYPE = "Unknown file type."
DIFFERENT_DATA_AMOUNTS = "Data lists are not the same length."
INVALID_UNCERTAINTIES = "Not all uncertainties are positive."
INVALID_DATA_VALUE = "Data has a non float value."
UNKNOWN_ERROR = "Unkown Error."
