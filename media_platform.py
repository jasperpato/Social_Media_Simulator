import matplotlib.pyplot as plt
import numpy as np
from globals import *
import sys
import time


class MediaPlatform():
	def __init__(
		self,
		agent_bias=B,
		posting_agents=P,
		post_noise=POST_NOISE,
		prop_posts_consumed=C,
		platform_bias=PLATFORM_BIAS,
		rec_bias=RECOMMENDATION_BIAS,
		verbose=False
	):
		self.agent_bias = agent_bias
		self.posting_agents = posting_agents
		self.post_noise = post_noise
		self.prop_posts_consumed = prop_posts_consumed
		self.platform_bias = platform_bias
		self.rec_bias = rec_bias
		self.verbose = verbose

		self.num_posters = round(P * NUM_AGENTS)
		self.posts_per_day = round(C * self.num_posters)

		self.num_same = 0
		[self.platform_opinion] = np.random.choice([-1, 1], 1)

		self.m = 0
		self.c = 0

		if self.agent_bias > 0:
			self.m = (2 - agent_bias) / (2 * agent_bias)
			self.c = 1 - 2 * self.m

		self.agent_opinions = np.random.uniform(-1, 1, NUM_AGENTS)
		self.t_agent_opinion = self.agent_opinions.copy()
		self.prev_opinions = self.agent_opinions.copy()


	def change_agent_opinions(self, posts):
		diff = np.abs(posts - self.agent_opinions)
		strengthen_probs = np.zeros(NUM_AGENTS)
		
		fun1 = diff <= 2 - self.agent_bias
		fun2 = diff > 2 - self.agent_bias

		strengthen_probs[fun1] = 1 - diff[fun1] / 2
		strengthen_probs[fun2] = self.m * diff[fun2] + self.c

		strengthened = np.random.random(NUM_AGENTS) < strengthen_probs
		self.agent_opinions[strengthened] += np.sign(self.agent_opinions[strengthened]) * D			# strengthen opinions
		self.agent_opinions[~strengthened] -= np.sign(self.agent_opinions[~strengthened]) * D		# weaken opinions
		self.agent_opinions = np.clip(self.agent_opinions, -1, 1)
		
		
	def serve_posts(self):
		ctc = np.zeros((self.num_posters, NUM_AGENTS))  # creator to consumer matrix
		ctc = ctc + np.reshape(self.posts, (self.num_posters, 1))
             
		# calculate similarity between creator and consumer opinions
		ctc_consumer_sim = 1 - np.abs(ctc - self.agent_opinions) / 2 + sys.float_info.epsilon
		# calculate similarity between creator and platform opinions
		ctc_platform_sim = 1 - np.abs(ctc - self.platform_opinion) / 2 + sys.float_info.epsilon
            
		ctc = self.platform_bias * ctc_platform_sim + self.rec_bias * ctc_consumer_sim
		ctc = ctc / np.max(ctc, axis=0, keepdims=True)               # normalize with max of each agent's posts
		ctc[np.diag_indices(self.num_posters)] = 0                        # posters should not consume their own posts
		return ctc


	def time_step(self):
		'''
		Each agent consumes its own served posts
		'''
		self.posts = self.agent_opinions[:self.num_posters] 								# posts are the opinions of the posting agents
		self.posts += np.random.normal(scale=self.post_noise, size=self.posts.shape) 	# add noise to posts
		self.posts = np.clip(self.posts, -1, 1) 									# clip posts to [-1, 1]

		if self.platform_bias or self.rec_bias:
			ctc = self.serve_posts()
			tiled_posts = np.tile(self.posts, (NUM_AGENTS, 1))
			sort_order = np.argsort(ctc.T, axis=1)[:, ::-1]
			tiled_posts = np.take_along_axis(tiled_posts, sort_order, axis=1)

			for i in range(self.posts_per_day):
				selected_posts = tiled_posts[:, i]
				self.change_agent_opinions(selected_posts)
		else:
			selected_posts = np.random.choice(self.posts, self.posts_per_day)
			for i in range(self.posts_per_day):
				posts_i = np.tile(selected_posts[i], NUM_AGENTS)
				self.change_agent_opinions(posts_i)
		
		self.t_agent_opinion = np.vstack((self.t_agent_opinion, self.agent_opinions))

	
	def converged(self):
		'''
		Return True if no opinions have changed in the last CONVERGENCE_NUM time steps
		'''
		if np.all(self.agent_opinions == self.prev_opinions):
			self.num_same += 1
		else:
			self.prev_opinions = self.agent_opinions.copy()
			self.num_same = 0

		return self.num_same == CONVERGENCE_NUM


	def simulate(self):
		'''
		Execute the specified time steps, or until convergence of opinions
		'''
		for i in range(NUM_TIME_STEPS):
			if self.verbose:
				print(f'Time step {i}')
			self.time_step()
			if self.converged():
				return


	def fractions(self):
		'''
		Return the fractions of agents holding positive and negative opinions
		'''
		pos = np.sum(self.agent_opinions > POLARISATION_CUTOFF) / NUM_AGENTS
		neg = np.sum(self.agent_opinions < -POLARISATION_CUTOFF) / NUM_AGENTS

		if self.verbose:
			print(f'Fraction positive {pos}')
			print(f'Fraction negative {neg}')

		return [pos, neg]
	

	def polarisation(self):
		'''
		Return polarisation value between [0, 1]
		'''
		return min(self.fractions())


	def graph(self):
		'''
		Graph every agent's opinion changing over time
		'''
		_, ax = plt.subplots()
		for i in range(NUM_AGENTS):
			ax.plot(self.t_agent_opinion[:, i], label=i)
		

if __name__ == '__main__':
	start_time = time.time()
	np.random.seed(0)
	m = MediaPlatform(agent_bias=0)
	m.simulate()
	print(m.fractions())
	print(m.platform_opinion)
	print(f'--- {round(time.time() - start_time, 4)} seconds ---')
	m.graph()
	plt.show(block=True)