import config
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

	def calculate_chi_chi_reduced(self):
		"""
		Calculates the chi and chi reduced value
		"""
		chi_top_expression = self.input.y_values - (self.a_value * \
										  			self.input.x_values + \
										  			self.b_value)
		chi_expression = chi_top_expression / self.input.y_uncertainties
		self.chi = np.sum(np.power(chi_expression, 2))
		self.chi_reduced = self.chi / (len(self.input.x_values) - 2)

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

		mean_square_y_uncertainty = self.calculate_weighted_mean(np.power(self.input.y_uncertainties, 2))
		self.a_value = (mean_xy - (x_mean * y_mean)) / \
					   (mean_square_x - square_x_mean)

		self.a_uncertainty = mean_square_y_uncertainty / \
							 (len(self.input.x_values) * (mean_square_x - square_x_mean))

		self.a_uncertainty = np.power(self.a_uncertainty, 0.5)

		self.b_value = y_mean - self.a_value * x_mean

		self.b_uncertainty = (mean_square_y_uncertainty * mean_square_x) / \
							 (len(self.input.x_values) * (mean_square_x - square_x_mean))

		self.b_uncertainty = np.power(self.b_uncertainty, 0.5)

	def print_output(self):
		print(config.LINEAR_OUTPUT_FORMAT.format(self.a_value,
												 self.a_uncertainty,
												 self.b_value,
												 self.b_uncertainty,
												 self.chi,
												 self.chi_reduced))

	def plot(self, save_plot_name = None, save_plot = True, plot = False):
		"""
		plots the data points and linear function created
		if save_plot is true saves plot to current directory
		with save_plot_name
		if plot is true shows plot on screen
		"""
		linear_function = self.create_linear_function()
		fig = plt.figure()
		ax = plt.axes()
		x = np.linspace(np.min(self.input.x_values), 
						np.max(self.input.x_values), 1000)
		ax.plot(x, np.vectorize(linear_function)(x), color = 'r');
		plt.errorbar(self.input.x_values, self.input.y_values,
					 xerr = self.input.x_uncertainties,
					 yerr = self.input.y_uncertainties, fmt='+',
					 ecolor='b')
		plt.xlabel(self.input.x_axis_title)
		plt.ylabel(self.input.y_axis_title)

		if plot:
			plt.show()

		if save_plot:
			plt.savefig(save_plot_name + '.svg')

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


	def calculate(self):
		self.calculate_linear_a_b_values()
		self.calculate_chi_chi_reduced()


		