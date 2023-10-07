import matplotlib.pyplot as plt
from media_platform import MediaPlatform

SIMULATIONS = 20

def simulate():
	'''
	Execute an entire simulation
	'''
	m = MediaPlatform()
	m.simulate()
	return m.polarisation()


if __name__ == '__main__':
	fractions = []
	try:
		for i in range(SIMULATIONS):
			f = simulate()
			fractions.append(f)

	except KeyboardInterrupt:
		pass

	print(fractions)
	plt.show(block=True)