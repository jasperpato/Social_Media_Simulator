import random
import networkx as nx
from agent import Agent
import matplotlib.pyplot as plt
from globals import *

class MediaPlatform():
	
	def __init__(self):
		self.graph = nx.random_regular_graph(K, NUM_AGENTS)
		for n in self.graph:
				self.graph.nodes[n]['self'] = Agent(is_biased=random.random() < B)

		self.polarisations = []
		self.positives = []

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
		for n0 in self.graph: # loop through each node
			agent = self.graph.nodes[n0]['self']
			
			for n1 in self.graph[n0]: # loop through the node's neighbours
				neighbour = self.graph.nodes[n1]['self']
				agent.receive_mix(neighbour.avg_mix)
			
			agent.update_orientation()
		
		self.positives.append(self.fraction_positive())
		self.polarisations.append(self.polarisation())

	def simulate(self):
		for i in range(NUM_TIME_STEPS):
			print(f'Time step {i}')
			self.time_step()

	def graph_polarisations(self):
		fig, ax = plt.subplots()
		ax.plot(self.polarisations, label='Polarisation')
		ax.plot(self.positives, label='Fraction positive')
		ax.plot([1-p for p in self.positives], label='Fraction negative')
		ax.legend()
		plt.show(block=True)

if __name__ == '__main__':
	m = MediaPlatform()
	m.simulate()
	m.graph_polarisations()