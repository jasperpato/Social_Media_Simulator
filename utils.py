import numpy as np
from globals import *

def get_random_opinions() -> np.ndarray:
	'''return np.ndarray of floats in [-1, 1)'''
	return 2 * np.random.rand(NUM_OPINIONS) - 1

def similarity(a: np.ndarray, b: np.ndarray) -> float:
	'''returns the cosine similarity between [-1, 1] between two opinion vectors'''
	s = np.dot(a, b) / np.linalg.norm(a) / np.linalg.norm(b)
	return 0 if np.isnan(s) else s

def norm_similarity(a: np.ndarray, b: np.ndarray) -> float:
	'''returns the cosine similarity scaled to be between [0, 1] between two opinion vectors'''
	s = (np.dot(a, b) / np.linalg.norm(a) / np.linalg.norm(b) + 1) / 2
	return 0 if np.isnan(s) else s