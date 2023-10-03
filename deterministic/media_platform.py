import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

NUM_AGENTS = 10
NUM_TIME_STEPS = 100

K = 4 # degree of regular graph
B = 0.4 # probability biased

P = 0.6 # probability of a signal supporting ground truth 
Q = 0.7 # rejection probability for biased agents

# ghost node numbers
POS_GHOST = NUM_AGENTS
NEG_GHOST = NUM_AGENTS + 1

class MediaPlatform():
	
	def __init__(self):
		self.graph = nx.random_regular_graph(K, NUM_AGENTS)
		self.signal_mixes = np.random.binomial(1, P, NUM_AGENTS)
		self.biases = np.random.binomial(1, B, NUM_AGENTS)

		self.update_orientations()

		# add ghost nodes
		self.graph.add_node(POS_GHOST)
		self.graph.add_node(NEG_GHOST)

		# add edges between agents and ghost nodes
		for n in self.graph:
			if n not in [POS_GHOST, NEG_GHOST]:
				self.graph.add_edge(n, POS_GHOST)
				self.graph.add_edge(n, NEG_GHOST)

		self.polarisations = []

		self.construct_matrix()
		print(self.A)

	def update_orientations(self):
		self.orientations = np.array([1 if self.signal_mixes[i] > 0.5 else -1 for i in range(NUM_AGENTS)])

	def construct_matrix(self):
		'''
		Construct initial update matrix
		'''
		self.A = np.identity(NUM_AGENTS + 2)

		# ghost nodes
		self.A[POS_GHOST][POS_GHOST] = K + 1
		self.A[NEG_GHOST][NEG_GHOST] = K + 1

		# loop through rows of matrix
		for r in range(NUM_AGENTS):
			# loop through neighbours
			for c in self.graph[r]:
					self.A[r][c] = 1 - Q if self.biases[r] else 1
			
			# connect to corresponding ghost node
			if self.biases[r]:
				self.A[r][POS_GHOST if self.orientations[r] == 1 else NEG_GHOST] = K * Q

		self.A /= K + 1

	def fraction_positive(self):
		'''
		Returns the fraction of agents with positive orientation
		'''
		return len([n for n in self.graph if self.graph.nodes[n]['self'].orientation == 1]) / NUM_AGENTS
	
	def polarisation(self):
		'''
		The fraction of agents of the minority orientation
		'''
		f = self.fraction_positive()
		return min([f, 1-f])

	def time_step(self):
		self.polarisations.append(self.polarisation())

	def simulate(self):
		for i in range(NUM_TIME_STEPS):
			print(f'Time step {i}')
			self.time_step()

	def graph_polarisations(self):
		plt.plot(self.polarisations)
		plt.show(block=True)

if __name__ == '__main__':
	m = MediaPlatform()
	# m.simulate()
	# m.graph_polarisations()