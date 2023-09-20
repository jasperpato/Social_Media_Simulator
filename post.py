import numpy as np
from globals import *
from utils import *

class Post():
	def __init__(self, opinions) -> None:
		self.opinions = opinions

	def __repr__(self) -> str:
		return 'Post\n' + np.array2string(self.opinions)