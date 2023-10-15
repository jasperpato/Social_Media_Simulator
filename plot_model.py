'''
Plots the confirmation bias model used for the explanation of our approach
'''

import matplotlib.pyplot as plt
import numpy as np

def plot_bias_models():

	def plot_model(b, ax):
		x = 2-b
		y = 1 - x/2

		ax.plot((0, x), (1, y), color='blue')
		ax.plot((x, 2), (y, 0), linestyle='dashed', color='blue')

		if b:
			ax.plot((x, 2), (y, 1), color='red')

			ax.plot((x, 2), (0, 0), color='green')
			ax.plot((x, x), (-0.05, 0.05), color='green')
			ax.plot((2, 2), (-0.05, 0.05), color='green')
			ax.text((2+x)/2, -0.075, 'B', color='green', fontsize=10)

		ax.set_title(f'Confirmation Bias Model (B = {b})', fontsize=12)


	fig, axs = plt.subplots(2, 2, figsize=(14, 8), sharex=True, sharey=True)

	plot_model(0, axs[0, 0])
	plot_model(1, axs[0, 1])
	plot_model(0.75, axs[1, 0])
	plot_model(0.25, axs[1, 1])

	fig.text(0.5, 0.04, 'Difference in opinion, d', ha='center', fontsize=12)
	fig.text(0.08, 0.5, 'Probability of strengthening opinion, P(S)', va='center', rotation='vertical', fontsize=12)

	plt.savefig('data/bias-model.png', dpi=600, bbox_inches='tight')


def plot_poster_distribution_model(dist):
	opinions = np.arange(-1.0, 1.0, 0.01)

	if dist == 'uniform':
		probs = np.ones_like(opinions)
	elif dist == 'bimodal':
		probs = np.cos((opinions + 1) / 2 * np.pi) ** 2
	elif dist == 'centered':
		probs = np.cos(opinions / 2 * np.pi) ** 2
	elif dist == 'skewed':
		probs = np.cos((opinions + 1) / 4 * np.pi) ** 2
	else:
		raise ValueError('Invalid poster distribution')
	
	probs /= np.sum(probs)
	fig, ax = plt.subplots(figsize=(8, 6))
	ax.plot(opinions, probs)
	ax.set_yticks([])
	fig.savefig(f'data/platform-vs-agent-bias/{dist}_dist.png', dpi=600, bbox_inches='tight')


if __name__ == '__main__':
	plot_poster_distribution_model('uniform')
	plot_poster_distribution_model('bimodal')
	plot_poster_distribution_model('centered')
	plot_poster_distribution_model('skewed')
	