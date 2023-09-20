import numpy as np

class Agent():
	def __init__(self, opinions=None):
		self.opinions = opinions or 2 * np.random.rand(10) - 1

	