import numpy as np
from globals import *
from utils import *
from agent import Agent
from post import Post

class MediaPlatform():
	def __init__(self, opinions=None) -> None:
		self.opinions = opinions or get_random_opinions()
		self.agents = [Agent() for _ in range(NUM_AGENTS)]
		self.posts = []

	def get_prob(self, p: Post, a: Agent):
		'''
		returns probability of choosing a post for an agent
		the probability is related to the similarity between the post's opinions and the platform's
		and the similarity between the post's opinions and the agent's
		'''
		return PLATFORM_INFLUENCE * similarity(p.opinions, self.opinions) + (1 - PLATFORM_INFLUENCE) * similarity(p.opinions, a.opinions)

	def choose_posts(self, a: Agent):
		return np.random.choice(self.posts, size=POSTS_PER_DAY, p=[self.get_prob(p, a) for p in self.posts])

	def day(self):
		self.posts = [a.generate_post() for a in np.random.choice(self.agents, size=PROPORTION_POSTING_AGENTS * NUM_AGENTS)]
		for a in self.agents:
			[a.consume_post(p) for p in self.choose_posts(a)]

	def __repr__(self) -> str:
		return f'{self.__class__.__name__} {np.array2string(self.opinions)}'