'''
Runs different experiments and collects data

usage:
	python3 simulate.py [agent | platform | recommendation | heatmap]
'''

from media_platform import MediaPlatform
from tqdm import tqdm
import numpy as np
import json
import os
from globals import *


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


def simulate_agent_bias():
	bs = [round(i / 100, 2) for i in range(101)]
	data = {}
	for b in bs:
		print(b)
		data[b] = []
		for _ in range(NUM_SIMULATIONS):
			results = simulate(b=b)
			data[b].append(min(results[1:]))
	
	save(data, filename=f'data/bias-vs-polarisation/data-p{P}-c{C}-plat1-rec1.json')


def simulate_platform_bias():
	data = {}
	platforms = [round(i / 10, 1) for i in range(0, 51)] # 0-5 in steps of 0.1

	for plat in platforms:
		print(plat)
		data[plat] = []
		for _ in range(NUM_SIMULATIONS):
			results = simulate(pb=plat)
			data[plat].append(results)

	save(data, filename=f'data/platform-vs-polarisation/data-b{B}-p{P}-c{C}-rec{RB}.json')


def simulate_rec_bias():
	data = {}
	recs = [round(i / 10, 1) for i in range(0, 51)] # 0-5 in steps of 0.1

	for rec in recs:
		print(rec)
		data[rec] = []
		for _ in range(NUM_SIMULATIONS):
			results = simulate(rb=rec)
			data[rec].append(results)

	save(data, filename=f'data/rec-vs-polarisation/data-b{B}-p{P}-c{C}-platform{PB}.json')


def simulate_plat_vs_agent_bias(poster_dist, num_steps=100):
	data = np.zeros((num_steps, num_steps))
	agent_biases = np.linspace(0, 1, num_steps)
	platform_biases = np.linspace(0, 2, num_steps)

	for i, b in enumerate(tqdm(agent_biases)):
		for j, pb in enumerate(platform_biases):
			d = 0
			for _ in range(10):
				m = simulate(b=b, pb=pb, rb=1, poster_dist=poster_dist)
				d += m.fractions()[m.platform_opinion]
			data[i, j] = d / 10

	os.makedirs('data/platform-vs-agent-bias', exist_ok=True)
	np.save(f'data/platform-vs-agent-bias/data-p{P}-c{C}-n{N}-{poster_dist}.npy', data)


if __name__ == '__main__':
	import sys

	if 'agent' in sys.argv:
		simulate_agent_bias()

	elif 'platform' in sys.argv:
		simulate_platform_bias()
	
	elif 'recommendation' in sys.argv:
		simulate_rec_bias()

	elif 'heatmap' in sys.argv:
		simulate_plat_vs_agent_bias()

	else:
		simulate_agent_bias()