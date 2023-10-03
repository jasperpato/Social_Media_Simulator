import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

NUM_AGENTS     = 100
NUM_TIME_STEPS = 100

K = 10  # degree of regular graph
B = 0.1 # probability of an agent being biased
P = 0.5 # probability of an agent's initial orientation being 1
Q = 0.5 # probability of a biased agent rejecting an incongruent signal

# ghost node numbers
POS_GHOST = NUM_AGENTS
NEG_GHOST = NUM_AGENTS + 1

class MediaPlatform():
	
	def __init__(self):
		self.graph = nx.random_regular_graph(K, NUM_AGENTS) # only used to assign neighbours
		self.signal_mixes = np.random.binomial(1, P, NUM_AGENTS)
		self.biases = np.random.binomial(1, B, NUM_AGENTS)
		self.polarisations = []

		self.update_orientations()
		self.construct_matrix()
		print(self.A)

	def update_orientations(self):
		self.orientations = np.array([1 if self.signal_mixes[i] > 0.5 else -1 for i in range(NUM_AGENTS)])

	def construct_matrix(self):
		'''
		Construct initial update matrix
		'''
		self.A = np.identity(NUM_AGENTS + 2)

		# loop through rows of matrix
		for r in range(NUM_AGENTS):
			# loop through neighbours
			for c in self.graph[r]:
					self.A[r][c] = 1 - Q if self.biases[r] else 1
			
			# connect to corresponding ghost node
			if self.biases[r]:
				self.A[r][POS_GHOST if self.orientations[r] == 1 else NEG_GHOST] = K * Q
		
		# ghost nodes
		self.A[POS_GHOST][POS_GHOST] = K + 1
		self.A[NEG_GHOST][NEG_GHOST] = K + 1

		self.A /= K + 1

	def update_matrix(self):
		'''
		Switch biased agents' ghost nodes edge weight if their orientation has changed
		'''
		for r in range(NUM_AGENTS):
			if self.biases[r]:
				self.A[r][POS_GHOST] = K * Q / (K + 1) if self.orientations[r] == 1 else 0
				self.A[r][NEG_GHOST] = 0 if self.orientations[r] == 1 else K * Q / (K + 1)

	def polarisation(self):
		'''
		The fraction of agents of the minority orientation
		'''
		f = len([o for o in self.orientations if o == 1]) / NUM_AGENTS
		return min([f, 1-f])

	def time_step(self):
		self.polarisations.append(self.polarisation())
		print(self.signal_mixes)
		self.signal_mixes = np.dot(self.A, np.append(self.signal_mixes, [1, 0]))[:NUM_AGENTS] # append ghost nodes to signal mix vector
		self.update_orientations()
		self.update_matrix()

	def simulate(self):
		for i in range(NUM_TIME_STEPS):
			print(f'Time step {i}')
			self.time_step()

	def graph_polarisations(self):
		plt.plot(self.polarisations)
		plt.show(block=True)

if __name__ == '__main__':
	m = MediaPlatform()
	m.simulate()
	m.graph_polarisations()