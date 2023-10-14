from media_platform import MediaPlatform
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import pathlib
from globals import *

DATA_NAME = f'b{B}-p{P}-c{C}-rec{RB}'


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
			'N': N,
			'PB': PB,
			'RB': RB
	},
		'data': fractions
	}
	with open(filename, 'w') as f:
		json.dump(data, f, indent=2)


def simulate(platform_bias):
	'''
	Execute an entire simulation
	'''
	m = MediaPlatform(platform_bias=platform_bias)
	m.simulate()
	return m


def variance(lst):
	avg = sum(lst) / len(lst)
	return sum([(x - avg)**2 for x in lst]) / len(lst)


def plot_bias_vs_polarisation(fractions):
	'''
	Plot bias vs polarisation
	'''
	x, y = zip(*[(k, round(sum(v) / NUM_SIMULATIONS, 4)) for k, v in fractions.items()])

	_, ax = plt.subplots()
	ax.plot(x, y)
	plt.xlabel('Bias')
	plt.ylabel('Mean Polarisation')
	plt.savefig(f'data/bias-avg-{DATA_NAME}.png')

	x, y = zip(*[(k, round(variance(v), 4)) for k, v in fractions.items()])

	_, ax = plt.subplots()
	ax.plot(x, y)
	plt.xlabel('Bias')
	plt.ylabel('Polarisation Variance')
	plt.savefig(f'data/bias-var-{DATA_NAME}.png')

	# plt.show(block=True)
	# plt.show(block=True)


def simulate_platform_bias():
	data = {}
	platforms = [round(i / 10, 1) for i in range(0, 51)] # 0-5 in steps of 0.1
	try:
		for plat in platforms:
			print(plat)
			data[plat] = []
			for i in range(NUM_SIMULATIONS):
				results = simulate(plat)
				data[plat].append(results)
			# fractions[b] = round(sum(fractions[b]) / NUM_SIMULATIONS, 4)

	except KeyboardInterrupt:
		exit()

	print(data)

	save(data, filename=f'data/plat-vs-polarisation/data-{DATA_NAME}.json')

	# backup
	save(data, filename=pathlib.Path.home() / f'data-{DATA_NAME}.json')


def simulate_platform_vs_agent_bias(num_steps):
	data = np.zeros((num_steps, num_steps))
	agent_biases = np.linspace(0, 1, num_steps)
	platform_biases = np.linspace(0, 2, num_steps)
	try:
		for i, b in enumerate(tqdm(agent_biases)):
			for j, p in enumerate(platform_biases):
				m = simulate(agent_bias=b, platform_bias=p, post_noise=0)
				data[i, j] = m.fractions()[m.platform_opinion]
	except KeyboardInterrupt:
		exit()

	plt.imshow(data, cmap='viridis', interpolation='lanczos')
	plt.colorbar()
	plt.xticks(np.arange(0, num_steps, 10), np.round(platform_biases[::10], 2))
	plt.yticks(np.arange(0, num_steps, 10), np.round(agent_biases[::10], 2))
	plt.show(block=True)

	os.makedirs('data/platform-vs-agent-bias', exist_ok=True)
	data_name = f'n{N}-p{P}-c{C}-rec{RB}'
	np.save(f'data/platform-vs-agent-bias/data-{DATA_NAME}.npy', data)



if __name__ == '__main__':
	simulate_platform_vs_agent_bias(100)