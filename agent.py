import numpy as np
from globals import *
from utils import *
from post import Post

class Agent():
	def __init__(self, opinions=None) -> None:
		self.opinions = opinions or get_random_opinions()

	def __repr__(self) -> str:
		return 'Agent\n' + np.array2string(self.opinions)
	
	def generate_post(self, noise=POST_GEN_NOISE) -> Post:
		'''returns a Post that aligns with the Agent's opinions +/i a random float in [-noise, noise)'''
		return Post(self.opinions + noise * (2 * np.random.rand(NUM_OPINIONS) - 1))
	
if __name__ == '__main__':
	print(Agent())