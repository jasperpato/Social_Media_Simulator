import matplotlib.pyplot as plt

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

fig.text(0.5, 0.04, 'Difference in opinion, |o1 - o2|', ha='center', fontsize=12)
fig.text(0.08, 0.5, 'Probability of strengthening opinion, P(S)', va='center', rotation='vertical', fontsize=12)

plt.savefig('data/bias-model.png', dpi=600, bbox_inches='tight')