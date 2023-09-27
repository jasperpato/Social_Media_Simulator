import numpy as np
import random
import networkx as nx

from agent import Agent

NUM_AGENTS = 100
K = 10
PROBABILITY_BIASED = 0.1


class MediaPlatform():
	def __init__(self):
		self.graph = nx.random_regular_graph(K, NUM_AGENTS)
		for n in self.graph:
			if random.random() > PROBABILITY_BIASED:
				self.graph.nodes[n]['self'] = Agent()
			else: 
				self.graph.nodes[n]['self'] = Agent(is_biased=True)

if __name__ == '__main__':
	m = MediaPlatform()