import numpy as np
from globals import *
from utils import *
from agent import Agent
from post import Post
import matplotlib.pyplot as plt

class MediaPlatform():
	def __init__(self, opinions=None) -> None:
		self.opinions = opinions or get_random_opinions()
		self.agents = [Agent() for _ in range(NUM_AGENTS)]
		self.posts = []

	def get_probs(self, a: Agent):
		'''
		returns probabilities of choosing each post for an agent
		each probability is related to the similarity between the post's opinions and the platform's
		and the similarity between the post's opinions and the agent's
		'''
		values = [PLATFORM_INFLUENCE * norm_similarity(p.opinions, self.opinions) + (1 - PLATFORM_INFLUENCE) * norm_similarity(p.opinions, a.opinions) for p in self.posts]
		total = sum(values)
		l = len(values)
		return [v / total if total else 1/l for v in values]

	def choose_posts(self, a: Agent):
		return np.random.choice(self.posts, size=POSTS_PER_DAY, p=self.get_probs(a))

	def day(self):
		# generate the daily posts
		self.posts = [a.generate_post() for a in np.random.choice(self.agents, size=int(PROPORTION_POSTING_AGENTS * NUM_AGENTS))]
		
		# give posts to each agent
		for a in self.agents:
			[a.consume_post(p) for p in self.choose_posts(a)]

	def get_average_similarities(self):
		sims = [similarity(a.opinions, self.opinions) for a in self.agents]
		return sum(sims) / len(sims)

	def simulate(self):
		self.average_similarities = []
		for _ in range(NUM_DAYS):
			self.day()
			self.average_similarities.append(self.get_average_similarities())

	def graph(self):
		plt.plot(self.average_similarities)
		plt.show(block=True)

	def __repr__(self) -> str:
		return f'{self.__class__.__name__} {np.array2string(self.opinions)}'
	
if __name__ == '__main__':
	m = MediaPlatform()
	m.simulate()
	m.graph()