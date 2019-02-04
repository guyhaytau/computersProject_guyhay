import config
import utils
import traceback
from lab_fit_exception import LabFitException
from input_parser import InputParser
from fit_linear_calculator import FitLinearCalculator
import argparse



def search_best_parameter(file_path):
	input_parser = InputParser(file_path = file_path, contains_ab_values = True)
	file_input = input_parser.start()
	linear_calc = FitLinearCalculator(file_input)
	linear_calc.calculate(chose_ab = True)
	linear_calc.print_output()
	linear_calc.plot(save_plot_name = config.LINEAR_PLOT_FILE_NAME)
	linear_calc.create_and_plot_a_chosing_plot(save_plot_name = config.A_PLOT_FILE_NAME)

def fit_linear(file_path):
	input_parser = InputParser(file_path = file_path)
	file_input = input_parser.start()
	linear_calc = FitLinearCalculator(file_input)
	linear_calc.calculate()
	linear_calc.print_output()
	linear_calc.plot(save_plot_name = config.LINEAR_PLOT_FILE_NAME)

def parse_args():
	parser = argparse.ArgumentParser(description='Fits a function to a data set')
	parser.add_argument('-f','--file_path', help='data file path', required=True)
	parser.add_argument('-b','--bonus', help='bonus data file path', action="store_true")
	args = vars(parser.parse_args())
	return args


def main(file_path, bonus):
	file_path_column = r"C:\studies\computers\inputOutputExamples\workingCols\input.txt"
	file_path_row = r"C:\studies\computers\inputOutputExamples\workingRows\input.txt"

	try:
		if bonus:
			search_best_parameter(file_path)
		else:
			fit_linear(file_path)
	except LabFitException as e:
		print(e.message)
	except Exception as e:
		print("{0}:".format(config.UNKNOWN_ERROR))
		traceback.print_exc()

if __name__ == '__main__':
	args_dict = parse_args()
	main(args_dict['file_path'], args_dict['bonus'])