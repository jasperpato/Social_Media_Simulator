from media_platform import MediaPlatform
import matplotlib.pyplot as plt
import json
from globals import *


DATA_NAME = f'b{B}-p{P}-c{C}-platform{PLATFORM_BIAS}'


def save(fractions, filename):
	data = {
		'parameters': {
			'NUM_AGENTS': NUM_AGENTS,
			'NUM_TIME_STEPS': NUM_TIME_STEPS,
			'CONVERGENCE_NUM': CONVERGENCE_NUM,
			'NUM_SIMULATIONS': NUM_SIMULATIONS,
			'B': B,
			'P': P,
			'C': C,
			'D': D,
			'POST_NOISE': POST_NOISE,
			'PLATFORM_BIAS': PLATFORM_BIAS,
			'RECOMMENDATION_BIAS': RECOMMENDATION_BIAS
		},
		'data': fractions
	}
	with open(filename, 'w') as f:
		json.dump(data, f, indent=2)


def simulate(rec):
	'''
	Execute an entire simulation
	'''
	m = MediaPlatform(rec_bias=rec)
	m.simulate()
	return [int(m.platform_opinion), *[float(f) for f in m.fractions()]]


def variance(lst):
	avg = sum(lst) / len(lst)
	return sum([(x - avg)**2 for x in lst]) / len(lst)


def plot(fractions):
	'''
	Plot bias vs polarisation
	'''
	x, y = zip(*[(k, round(sum(v) / NUM_SIMULATIONS, 4)) for k, v in fractions.items()])

	fig, ax = plt.subplots()
	ax.plot(x, y)
	plt.xlabel('Bias')
	plt.ylabel('Mean Polarisation')
	plt.savefig(f'data/bias-avg-{DATA_NAME}.png')

	x, y = zip(*[(k, round(variance(v), 4)) for k, v in fractions.items()])

	fig, ax = plt.subplots()
	ax.plot(x, y)
	plt.xlabel('Bias')
	plt.ylabel('Polarisation Variance')
	plt.savefig(f'data/bias-var-{DATA_NAME}.png')

	# plt.show(block=True)
	# plt.show(block=True)


if __name__ == '__main__':
	import pathlib

	data = {}
	try:
		for rec in RECOMMENDATIONS:
			print(rec)
			data[rec] = []
			for i in range(NUM_SIMULATIONS):
				results = simulate(rec)
				data[rec].append(results)
			# fractions[b] = round(sum(fractions[b]) / NUM_SIMULATIONS, 4)

	except KeyboardInterrupt:
		exit()
		# pass

	print(data)

	save(data, filename=f'data/rec-vs-polarisation/data-{DATA_NAME}.json')

	# backup
	save(data, filename=pathlib.Path.home() / f'data-{DATA_NAME}.json')

	# plot(fractions)