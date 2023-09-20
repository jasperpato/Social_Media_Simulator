import numpy as np
from globals import *

def get_random_opinions(size=NUM_OPINIONS) -> np.ndarray:
	'''return np.ndarray of floats in [-1, 1)'''
	return 2 * np.random.rand(size) - 1