import numpy as np
import networkx as nx

NUM_AGENTS = 100
K = 10

class MediaPlatform():
	def __init__(self):
		self.graph = nx.random_regular_graph(K, NUM_AGENTS)
		for n in self.graph:
			self.graph.nodes[n]['opinion'] = np.random.choice([-1, 1])

if __name__ == '__main__':
	m = MediaPlatform()