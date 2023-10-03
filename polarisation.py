import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

NUM_AGENTS     = 10e3
NUM_TIME_STEPS = 10e3

K = 8 # degree of regular graph
F = 10e-2 # probability of an agent being biased
P = 0.53 # probability of an agent's initial orientation being 1
Q = 1 # probability of a biased agent rejecting an incongruent signal

# ghost node numbers
POS_GHOST = NUM_AGENTS
NEG_GHOST = NUM_AGENTS + 1

class Simulation():
	
	def __init__(self):
		self.graph = nx.random_regular_graph(K, NUM_AGENTS) # only used to assign neighbours
		self.signal_mixes = np.random.binomial(1, P, NUM_AGENTS)
		self.biases = np.random.binomial(1, F, NUM_AGENTS)
		
		self.polarisations = []
		self.average_signal_mixes = []

		self.update_orientations()
		self.construct_matrix()

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
		self.average_signal_mixes.append(np.average(self.signal_mixes))

		self.signal_mixes = np.dot(self.A, np.append(self.signal_mixes, [1, 0]))[:NUM_AGENTS] # append ghost nodes to signal mix vector
		self.update_orientations()
		self.update_matrix()

	def simulate(self):
		for i in range(NUM_TIME_STEPS):
			print(f'Time step {i}')
			self.time_step()

	def graph_polarisations(self):
		plt.plot(self.polarisations, self.average_signal_mixes)
		plt.show(block=True)

if __name__ == '__main__':
	s = Simulation()
	s.simulate()
	print(s.polarisations[-1])
	s.graph_polarisations()