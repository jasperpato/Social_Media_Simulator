import numpy as np
from globals import *
from utils import *
from post import Post

class Agent():
	def __init__(self, opinions=None):
		self.opinions = opinions or get_random_opinions()

	def __repr__(self):
		return f'{self.__class__.__name__} {np.array2string(self.opinions)}'
	
	def generate_post(self) -> Post:
		'''returns a Post that aligns with the Agent's opinions +/- a random float in [-noise, noise)'''
		return Post(self.opinions + POST_GENERATION_NOISE * (2 * np.random.rand(NUM_OPINIONS) - 1))
	
	def consume_post(self, post: Post):
		self.opinions += POST_INFLUENCE * post.opinions

if __name__ == '__main__':
	a = Agent()
	a.generate_post()
