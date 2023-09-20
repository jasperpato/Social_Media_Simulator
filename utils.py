import numpy as np
from globals import *

def get_random_opinions() -> np.ndarray:
	'''return np.ndarray of floats in [-1, 1)'''
	return 2 * np.random.rand(NUM_OPINIONS) - 1