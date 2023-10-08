from media_platform import MediaPlatform
import matplotlib.pyplot as plt
import json

BS = [round(0.01 * i, 2) for i in range(0, 101)]
NUM_SIMULATIONS = 100

def save(fractions, filename='data/data.txt'):
	with open(filename, 'w') as f:
		json.dump(fractions, f, indent=2)

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
			fractions[b] = []
			for i in range(NUM_SIMULATIONS):
				f = simulate(b)
				fractions[b].append(f)
			fractions[b] = round(sum(fractions[b]) / NUM_SIMULATIONS, 4)

	except KeyboardInterrupt:
		pass

	print(fractions)
	save(fractions)

	plt.plot(fractions.keys(), fractions.values())
	plt.xlabel('Bias')
	plt.ylabel('Polarisation')
	plt.show(block=True)

	# plt.show(block=True)