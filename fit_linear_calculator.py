import config
import copy
import numpy as np
import matplotlib.pyplot as plt

class FitLinearCalculator(object):
	"""Will calculate all the linear fitted function's parameters"""
	def __init__(self, input_obj):
		super(FitLinearCalculator, self).__init__()
		self.input = input_obj
		self.a_value = 0
		self.a_uncertainty = 0
		self.b_value = 0
		self.b_uncertainty = 0
		self.chi = 0
		self.chi_reduced = 0

	def calculate_chi_chi_reduced(self, a_value = None, b_value = None, return_value = False):
		"""
		Calculates the chi and chi reduced value
		a_value - the a value to use, if none will use self.a_value
		b_value - the b value to use, if none will use self.b_value
		return_value - returns value instead of inserting it to
					   self.chi and self.chi_reduced
		"""
		a_value = a_value if a_value != None else self.a_value
		b_value = b_value if b_value != None else self.b_value
		chi_top_expression = self.input.y_values - (a_value * \
										  			self.input.x_values + \
										  			b_value)
		chi_expression = chi_top_expression / self.input.y_uncertainties
		chi = np.sum(np.power(chi_expression, 2))
		chi_reduced = chi / (len(self.input.x_values) - 2)

		if return_value:
			return chi, chi_reduced
		else:
			self.chi = chi
			self.chi_reduced = chi_reduced

	def calculate_linear_a_b_values(self):
		"""
		Calculates the linear fit's a and b values
		"""
		mean_xy = self.calculate_weighted_mean(self.input.x_values * \
											   self.input.y_values)
		x_mean = self.calculate_weighted_mean(self.input.x_values)
		y_mean = self.calculate_weighted_mean(self.input.y_values)
		mean_square_x = self.calculate_weighted_mean(np.power(self.input.x_values, 2))
		square_x_mean = np.power(x_mean, 2)

		y_uncertainties_power = np.power(self.input.y_uncertainties, 2)
		mean_square_y_uncertainty = self.calculate_weighted_mean(y_uncertainties_power)
		self.a_value = (mean_xy - (x_mean * y_mean)) / \
					   (mean_square_x - square_x_mean)

		self.a_uncertainty = mean_square_y_uncertainty / \
							 (len(self.input.x_values) * (mean_square_x - square_x_mean))

		self.a_uncertainty = np.power(self.a_uncertainty, 0.5)

		self.b_value = y_mean - self.a_value * x_mean

		self.b_uncertainty = (mean_square_y_uncertainty * mean_square_x) / \
							 (len(self.input.x_values) * (mean_square_x - square_x_mean))

		self.b_uncertainty = np.power(self.b_uncertainty, 0.5)

	def chose_best_a_b_values(self):
		"""
		Choses the best a and b values via comparing the chi value
		"""
		best_a = self.input.a_values[0]
		best_b = self.input.b_values[0]
		best_chi, best_chi_reduced = self.calculate_chi_chi_reduced(best_a, best_b, 
																	return_value = True)
		test_chi = best_chi
		for a_value in self.input.a_values:
			for b_value in self.input.b_values:
				# Calculates chi and determines if it is better
				test_chi, test_chi_reduced = self.calculate_chi_chi_reduced(a_value, b_value, 
																			return_value = True)
				if best_chi > test_chi:
					best_chi = test_chi
					best_chi_reduced = test_chi_reduced
					best_a = a_value
					best_b = b_value

		self.a_value = best_a
		self.b_value = best_b
		self.a_uncertainty = abs(self.input.a_step_size)
		self.b_uncertainty = abs(self.input.b_step_size)
		self.chi = best_chi
		self.chi_reduced = best_chi_reduced

	def create_a_plot_data_points(self):
		"""
		Creates the data points for the chi as a function of a
		returns the data points as two arrays
		first array will be the a values
		second array will be the chi values
		"""
		chi_values = []
		for a_value in self.input.a_values:
			# Calculates chi and chi reduced
			chi, chi_reduced = self.calculate_chi_chi_reduced(a_value, self.b_value, 
															  return_value = True)
			chi_values.append(chi)

		return copy.deepcopy(self.input.a_values), np.array(chi_values)

	def print_output(self):
		print(config.LINEAR_OUTPUT_FORMAT.format(self.a_value,
												 self.a_uncertainty,
												 self.b_value,
												 self.b_uncertainty,
												 self.chi,
												 self.chi_reduced))

	def plot(self, save_plot_name = None, plot = False):
		"""
		plots the data points and linear function created
		if save_plot_name is not None saves plot to current directory
		with save_plot_name
		if plot is true shows plot on screen
		"""
		linear_function = self.create_linear_function()
		fig = plt.figure()
		ax = plt.axes()
		x = np.linspace(np.min(self.input.x_values), 
						np.max(self.input.x_values), 1000)
		ax.plot(x, np.vectorize(linear_function)(x), color = 'r')
		plt.errorbar(self.input.x_values, self.input.y_values,
					 xerr = self.input.x_uncertainties,
					 yerr = self.input.y_uncertainties, fmt='+',
					 ecolor='b')
		plt.xlabel(self.input.x_axis_title)
		plt.ylabel(self.input.y_axis_title)

		if plot:
			plt.show()

		if save_plot_name:
			plt.savefig(save_plot_name + '.svg')

		# Closes figure window so it won't show when another function calls plt.show()
		# This happens regardless of if plt.show was called in this function
		plt.close()

	def plot_a_chosing_plot(self, a_values, chi_values, save_plot_name = None, 
							plot = False):
		"""
		plots the chi_values as a function of a_values
		if save_plot_name is not None saves plot to current directory
		with save_plot_name
		if plot is true shows plot on screen
		"""
		fig = plt.figure()
		ax = plt.axes()
		ax.plot(a_values, chi_values, color = 'b')
		plt.xlabel(config.A_PLOT_X_LABEL)
		plt.ylabel(config.A_PLOT_Y_LABEL_FORMAT.format(np.round(self.b_value, 1)))

		if plot:
			plt.show()

		if save_plot_name:
			plt.savefig(save_plot_name + '.svg', bbox_inches='tight')

		# Closes figure window so it won't show when another function calls plt.show()
		# This happens regardless of if plt.show was called in this function
		plt.close()

	def create_and_plot_a_chosing_plot(self, save_plot_name = None, 
									   plot = False):
		"""
		Plots and creates the a chosing plot data points
		if save_plot_name is not None saves plot to current directory
		with save_plot_name
		if plot is true shows plot on screen
		"""
		a_values, chi_values = self.create_a_plot_data_points()
		self.plot_a_chosing_plot(a_values, chi_values, save_plot_name = save_plot_name, plot = plot)

	def calculate_weighted_mean(self, data_points):
		"""
		Calculates a weighted mean value
		the weights are self.y_uncertainties
		"""
		square_weights = np.power(self.input.y_uncertainties, 2)
		square_weights_devided = np.sum(np.power(1 / self.input.y_uncertainties, 2))
		return np.sum(data_points / square_weights) / square_weights_devided

	def create_linear_function(self):
		def linear_function(x):
			return self.a_value * x + self.b_value

		return linear_function

	def calculate(self, chose_ab = False):
		if chose_ab and self.input.contains_ab_values:
			self.chose_best_a_b_values()
		else:
			self.calculate_linear_a_b_values()
			self.calculate_chi_chi_reduced()


		