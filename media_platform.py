import numpy as np
from globals import *
from utils import *

class MediaPlatform():
	def __init__(self, opinions=None) -> None:
		self.opinions = opinions or get_random_opinions()

	def __repr__(self) -> str:
		return 'Media Platform\n' + np.array2string(self.opinions)