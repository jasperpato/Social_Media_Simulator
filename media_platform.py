import random
from agent import Agent
import matplotlib.pyplot as plt
from globals import *

class MediaPlatform():
	
	def __init__(self, orientation=1):
		self.orientation = orientation
		self.agents = [Agent() for _ in range(NUM_AGENTS)]
		self.positives = [self.fraction_positive()]

	def censor(self, orientation):
		return orientation != self.orientation and random.random() < I
	
	def fraction_positive(self):
		return len([a for a in self.agents if a.orientation == 1]) / NUM_AGENTS

	def time_step(self):
		self.posts = [a.orientation for a in self.agents if a.is_poster and not self.censor(a.orientation)]
		for a in self.agents:
			for p in self.posts:
				a.receive_signal(p)
			a.update_orientation()
		self.positives.append(self.fraction_positive())

	def simulate(self):
		for i in range(NUM_TIME_STEPS):
			print(f'Time step {i}')
			self.time_step()

	def graph(self):
		plt.plot(self.positives)
		plt.show(block=True)

if __name__ == '__main__':
	m = MediaPlatform(-1)

	try: m.simulate()
	except KeyboardInterrupt: pass

	m.graph()