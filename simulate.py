'''
Runs different experiments and collects data
'''

from media_platform import MediaPlatform
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import json
import os
import pathlib
from globals import *

DATA_NAME = f'b{B}-p{P}-c{C}-rec{RB}'

def save(data, filename):
	json_data = {
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
		'data': data
	}
	with open(filename, 'w') as f:
		json.dump(json_data, f, indent=2)


def simulate(b=B, p=P, n=N, c=C, d=D, pb=PB, rb=RB, poster_dist='uniform'):
	'''
	Execute an entire simulation
	'''
	m = MediaPlatform(b, p, n, c, d, pb, rb, poster_dist)
	m.simulate()
	f = m.fractions()
	return [int(m.platform_opinion), float(f[1]), float(f[-1])]


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
			for _ in range(NUM_SIMULATIONS):
				results = simulate(pb=plat)
				data[plat].append(results)
			# fractions[b] = round(sum(fractions[b]) / NUM_SIMULATIONS, 4)

	except KeyboardInterrupt:
		exit()

	print(data)

	save(data, filename=f'data/platform-vs-polarisation/data-{DATA_NAME}.json')

	# backup
	save(data, filename=pathlib.Path.home() / f'data-{DATA_NAME}.json')


def simulate_rec_bias():
	data_name = f'b{B}-p{P}-c{C}-platform{PB}'

	data = {}
	recs = [round(i / 10, 1) for i in range(0, 51)] # 0-5 in steps of 0.1
	try:
		for rec in recs:
			print(rec)
			data[rec] = []
			for _ in range(NUM_SIMULATIONS):
				results = simulate(rb=rec)
				data[rec].append(results)
			# fractions[b] = round(sum(fractions[b]) / NUM_SIMULATIONS, 4)

	except KeyboardInterrupt:
		exit()

	print(data)

	save(data, filename=f'data/rec-vs-polarisation/data-{data_name}.json')

	# backup
	save(data, filename=pathlib.Path.home() / f'data-{data_name}.json')


def simulate_plat_vs_agent_bias(poster_dist, num_steps=100):
	data = np.zeros((num_steps, num_steps))
	agent_biases = np.linspace(0, 1, num_steps)
	platform_biases = np.linspace(0, 2, num_steps)
	try:
		for i, b in enumerate(tqdm(agent_biases)):
			for j, pb in enumerate(platform_biases):
				d = 0
				for _ in range(10):
					m = simulate(b=b, pb=pb, rb=1, poster_dist=poster_dist)
					d += m.fractions()[m.platform_opinion]
				data[i, j] = d / 10
	except KeyboardInterrupt:
		exit()

	os.makedirs('data/platform-vs-agent-bias', exist_ok=True)
	data_name = f'p{P}-c{C}-n{N}-{poster_dist}'
	np.save(f'data/platform-vs-agent-bias/data-{data_name}.npy', data)


def plot_plat_vs_agent_bias():
	a1 = np.load('data/platform-vs-agent-bias/data-p0.3-c0.1-n0-uniform.npy')
	a2 = np.load('data/platform-vs-agent-bias/data-p0.3-c0.1-n0-bimodal.npy')
	a3 = np.load('data/platform-vs-agent-bias/data-p0.3-c0.1-n0-centered.npy')
	a4 = np.load('data/platform-vs-agent-bias/data-p0.3-c0.1-n0-skewed.npy')

	def plot_model(arr, ax, title):
		im = ax.imshow(arr, cmap='seismic', interpolation='spline36', origin='lower', vmin=0.4, vmax=1.0)
		ax.set_title(title, fontsize=12)
		ax.set_xticks(np.arange(10, 100, 10), np.round(np.linspace(0.2, 1.8, 9), 2), rotation=45)
		ax.set_yticks(np.arange(10, 100, 10), np.round(np.linspace(0.1, 0.9, 9), 2))
		return im
	
	fig, axs = plt.subplots(2, 2, figsize=(12, 12), sharex=True, sharey=True)

	im1 = plot_model(a1, axs[0, 0], 'Uniform Distribution')
	plot_model(a2, axs[1, 0], 'Bimodal Distribution')
	plot_model(a3, axs[0, 1], 'Centered Distribution')
	plot_model(a4, axs[1, 1], 'Skewed Distribution')

	plt.suptitle('Platform vs Agent Bias for Different Poster Opinion Distributions', fontsize=16)
	cbax_ax = fig.add_axes([0.92, 0.15, 0.01, 0.7])
	cbar = fig.colorbar(im1, cax=cbax_ax)
	cbar.ax.get_yaxis().labelpad = 30
	cbar.ax.set_ylabel('Proportion of agents aligning with platform opinion', rotation=270, fontsize=12)
	fig.text(0.5, 0.04, 'Platform Bias / Recommendation Bias, PB / RB', ha='center', fontsize=12)
	fig.text(0.08, 0.5, 'Agent Bias, B', va='center', rotation='vertical', fontsize=12)
	fig.savefig(f'data/platform-vs-agent-bias/heatmap.png', dpi=600, bbox_inches='tight')


if __name__ == '__main__':
	# plot_plat_vs_agent_bias()

	simulate_rec_bias()