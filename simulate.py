from media_platform import MediaPlatform
import matplotlib.pyplot as plt
import json
from globals import *

def save(fractions, filename):
	data = {
		'parameters': {
			'NUM_AGENTS': NUM_AGENTS,
			'NUM_TIME_STEPS': NUM_TIME_STEPS,
			'CONVERGENCE_NUM': CONVERGENCE_NUM,
			'NUM_SIMULATIONS': NUM_SIMULATIONS,
			'P': P,
			'C': C,
			'D': D
		},
		'data': fractions
	}
	with open(filename, 'w') as f:
		json.dump(data, f, indent=2)

def simulate(b):
	'''
	Execute an entire simulation
	'''
	m = MediaPlatform(bias=b)
	m.simulate()
	# m.graph()
	return m.polarisation()


if __name__ == '__main__':
	fractions = {}
	try:
		for b in BS:
			print(b)
			fractions[b] = []
			for i in range(NUM_SIMULATIONS):
				# print(f'bias {b}, trial {i}')
				f = simulate(b)
				fractions[b].append(f)
			fractions[b] = round(sum(fractions[b]) / NUM_SIMULATIONS, 4)

	except KeyboardInterrupt:
		pass

	print(fractions)
	save(fractions, filename='data/data3.json')

	plt.plot(fractions.keys(), fractions.values())
	plt.xlabel('Bias')
	plt.ylabel('Polarisation')
	plt.savefig('data/bias-polarisation3.png')
	plt.show(block=True)

	# plt.show(block=True)