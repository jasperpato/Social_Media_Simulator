from agent import Agent
import matplotlib.pyplot as plt
from globals import *

class MediaPlatform():
	
	def __init__(self, opinion=1, verbose=False):
		self.opinion = opinion
		self.verbose = verbose
		self.agents = [Agent(is_poster = i < NUM_POSTERS) for i in range(NUM_AGENTS)]
		
		self.prev_opinions = [a.opinion for a in self.agents]
		self.num_same = 0

	def time_step(self):
		'''
		Each agent consumes the same subset of posts
		'''
		self.posts = [a.opinion for a in self.agents if a.is_poster][:POSTS_PER_DAY]
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
		Execute the specified time steps
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
		pos = len([a for a in self.agents if a.opinion == 1])
		neg = len([a for a in self.agents if a.opinion == -1])

		if self.verbose:
			print(f'Fraction positive {pos / NUM_AGENTS}')
			print(f'Fraction negative {neg / NUM_AGENTS}')

		return [pos, neg]

	def graph(self):
		'''
		Graph every agent's opinion changing over time
		'''
		_, ax = plt.subplots()
		for i, a in enumerate(self.agents[NUM_POSTERS:]):
			ax.plot(a.opinions, label=str(i))

def simulate():
	'''
	Execute an entire simulation
	'''
	m = MediaPlatform()
	m.simulate()
	m.graph()
	return m.fractions()

SIMULATIONS = 1

if __name__ == '__main__':
	fractions = []
	try:
		for i in range(SIMULATIONS):
			f = simulate()
			fractions.append(f)

	except KeyboardInterrupt:
		pass

	print(fractions)
	plt.show(block=True)