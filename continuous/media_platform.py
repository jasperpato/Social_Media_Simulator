from agent import Agent
import matplotlib.pyplot as plt
from globals import *

class MediaPlatform():
	
	def __init__(self, opinion=1, verbose=False):
		self.opinion = opinion
		self.verbose = verbose
		self.agents = [Agent(is_poster = i < NUM_POSTERS) for i in range(NUM_AGENTS)]
		
		# for convergence
		self.prev_opinions = [a.opinion for a in self.agents]
		self.num_same = 0

	def time_step(self):
		self.posts = [a.opinion for a in self.agents if a.is_poster][:POSTS_PER_DAY]
		for a in self.agents:
			for p in self.posts:
				a.consume_post(p)

	def simulate(self):
		for i in range(NUM_TIME_STEPS):
			if self.verbose:
				print(f'Time step {i}')

			self.time_step()

			# test for convergence
			opinions = [a.opinion for a in self.agents]
			if opinions == self.prev_opinions:
				self.num_same += 1
			else:
				self.prev_opinions = opinions
				self.num_same = 0

			if self.num_same == CONVERGENCE_NUM:
				return

	def fractions(self):
		pos = len([a for a in self.agents if a.opinion == 1])
		neg = len([a for a in self.agents if a.opinion == -1])

		if self.verbose:
			print(f'Fraction positive {pos / NUM_AGENTS}')
			print(f'Fraction negative {neg / NUM_AGENTS}')

		return [pos, neg]

	def graph(self):
		_, ax = plt.subplots()
		for i, a in enumerate(self.agents):
			ax.plot(a.opinions, label=str(i))

def simulate():
	m = MediaPlatform()
	m.simulate()
	m.graph()
	return m.fractions()

SIMULATIONS = 20

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