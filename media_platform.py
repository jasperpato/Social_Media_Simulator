from agent import Agent
import matplotlib.pyplot as plt
from globals import *
import random

class MediaPlatform():
	
	def __init__(self, bias=0, verbose=False):
		self.verbose = verbose
		self.agents = [Agent(bias=bias, is_poster=i < NUM_POSTERS) for i in range(NUM_AGENTS)]
		self.prev_opinions = [a.opinion for a in self.agents]
		self.num_same = 0

	def time_step(self):
		'''
		Each agent consumes the same subset of posts
		'''
		self.posts = random.sample([a.opinion for a in self.agents if a.is_poster], POSTS_PER_DAY)
		for a in self.agents:
			for p in self.posts:
				a.consume_post(p)
			a.opinions.append(a.opinion)

	def converged(self):
		'''
		Return True if no opinions have changed in the last CONVERGENCE_NUM time steps
		'''
		opinions = [a.opinion for a in self.agents]
		if opinions[NUM_POSTERS:] == self.prev_opinions[NUM_POSTERS:]:
			self.num_same += 1
		else:
			self.prev_opinions = opinions
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
		Return the fractions of agents holding the extreme opinions [-1, 1]
		'''
		pos = len([a for a in self.agents if a.opinion >= 0]) / NUM_AGENTS
		neg = len([a for a in self.agents if a.opinion < 0]) / NUM_AGENTS

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
		for i, a in enumerate(self.agents[NUM_POSTERS:]):
			ax.plot(a.opinions, label=str(i))

if __name__ == '__main__':
	m = MediaPlatform(bias=0.7)
	m.simulate()
	print(m.fractions())
	m.graph()
	plt.show(block=True)