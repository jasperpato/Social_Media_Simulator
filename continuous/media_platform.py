import random
from agent import Agent
import matplotlib.pyplot as plt
from globals import *

class MediaPlatform():
	
	def __init__(self, opinion=1):
		self.opinion = opinion
		self.agents = [Agent() for _ in range(NUM_AGENTS)]

	def time_step(self):
		self.posts = [a.opinion for a in self.agents if a.is_poster]
		for a in self.agents:
			for p in self.posts:
				a.consume_post(p)

	def simulate(self):
		for i in range(NUM_TIME_STEPS):
			print(f'Time step {i}')
			self.time_step()

	def graph(self):
		fig, ax = plt.subplots()
		for i, a in enumerate(self.agents):
			ax.plot(a.opinions, label=str(i))
		plt.show(block=True)

if __name__ == '__main__':
	m = MediaPlatform()

	try: m.simulate()
	except KeyboardInterrupt: pass

	m.graph()