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

def variance(lst):
	avg = sum(lst) / len(lst)
	return sum([(x - avg)**2 for x in lst]) / len(lst)

if __name__ == '__main__':
	fractions = {}
	try:
		for b in BS:
			print(b)
			fractions[b] = []
			for i in range(NUM_SIMULATIONS):
				f = simulate(b)
				fractions[b].append(f)
			# fractions[b] = round(sum(fractions[b]) / NUM_SIMULATIONS, 4)

	except KeyboardInterrupt:
		exit()
		# pass

	print(fractions)
	save(fractions, filename='data/data1.json')

	x, y = zip(*[(k, round(sum(v) / NUM_SIMULATIONS, 4)) for k, v in fractions.items()])
	print(x, y)

	fig, ax = plt.subplots()
	ax.plot(x, y)
	plt.xlabel('Bias')
	plt.ylabel('Mean Polarisation')
	plt.savefig('data/bias-avg.png')

	x, y = zip(*[(k, round(variance(v), 4)) for k, v in fractions.items()])

	fig, ax = plt.subplots()
	ax.plot(x, y)
	plt.xlabel('Bias')
	plt.ylabel('Polarisation Variance')
	plt.savefig('data/bias-var.png')

	# plt.show(block=True)
	# plt.show(block=True)