import main as mm



file_path_column = r"C:\studies\computers\inputOutputExamples\workingCols\input.txt"
file_path_row = r"C:\studies\computers\inputOutputExamples\workingRows\input.txt"
file_path_bonus = r"C:\studies\computers\inputOutputExamples\bonus\input.txt"


if __name__ == '__main__':
	# mm.fit_linear(file_path_column)
	# mm.fit_linear(file_path_row)
	mm.search_best_parameter(file_path_bonus)
