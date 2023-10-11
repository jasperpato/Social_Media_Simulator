from media_platform import MediaPlatform
import matplotlib.pyplot as plt
import numpy as np
import random
from globals import *
import sys


class BiasedMediaPlatform(MediaPlatform):
	def __init__(self, bias=0, verbose=False):
		super().__init__(bias=bias, verbose=verbose)  
		self.posts = np.array([a.opinion for a in self.agents[:NUM_POSTERS]])
		[self.platform_opinion] = random.sample([-1, 1], 1)
		
		
	def serve_posts(self):
		self.posts = np.array([a.opinion for a in self.agents[:NUM_POSTERS]])
		ctc = np.zeros((NUM_POSTERS, NUM_AGENTS))  # creator to consumer matrix
		ctc = ctc + np.reshape(self.posts, (NUM_POSTERS, 1))
             
		# calculate similarity between creator and consumer opinions
		ctc_consumer_sim = 2 - np.abs(ctc - self.prev_opinions) + sys.float_info.epsilon
		# calculate similarity between creator and platform opinions
		ctc_platform_sim = 2 - np.abs(ctc - self.platform_opinion) + sys.float_info.epsilon
            
		ctc = PLATFORM_BIAS * ctc_platform_sim + RECOMMENDATION_BIAS * ctc_consumer_sim
		ctc = ctc / np.max(ctc, axis=0, keepdims=True)               # normalize with max of each agent's posts
		ctc += np.random.normal(scale=0.2, size=ctc.shape)
		ctc[np.diag_indices(NUM_POSTERS)] = 0                        # posters should not consume their own posts
		
		ctc = ctc.T  # transpose to get consumer to creator matrix
		return ctc


	def time_step(self):
		'''
		Each agent consumes its own served posts
		'''
		ctc = self.serve_posts()

		for i in range(NUM_AGENTS):
			post_scores = ctc[i, :]
			selected_posts = self.posts[np.argsort(post_scores)][::-1][:POSTS_PER_DAY]
			
			for p in selected_posts:
				self.agents[i].consume_post(p)
			
			self.agents[i].opinions.append(self.agents[i].opinion)
		
	
def simulate():
	'''
	Execute an entire simulation
	'''
	m = BiasedMediaPlatform(bias=0)
	m.simulate()
	m.graph()
	return (m.fractions(), m.platform_opinion)

if __name__ == '__main__':
	fractions = []
	platform_opinions = []
	try:
		for i in range(NUM_SIMULATIONS):
			f, opinion = simulate()
			fractions.append(f)
			platform_opinions.append(opinion)

	except KeyboardInterrupt:
		pass

	print(fractions)
	print(platform_opinions)
	plt.show(block=True)