import matplotlib.pyplot as plt

def plot_model(b):
	x = 2-b
	y = 1 - x/2

	plt.plot((0, x), (1, y), color='blue')
	plt.plot((x, 2), (y, 0), linestyle='dashed', color='blue')

	if b:
		plt.plot((x, 2), (y, 1), color='red')

		plt.plot((x, 2), (0, 0), color='green')
		plt.plot((x, x), (-0.05, 0.05), color='green')
		plt.plot((2, 2), (-0.05, 0.05), color='green')
		plt.text((2+x)/2, -0.05, 'B', color='green')

	plt.xlabel('Difference in opinion, |o1 - o2|')
	plt.ylabel('Probability of strengthening opinion, P(S)')
	plt.title(f'Confirmation Bias Model (B = {b})')

plot_model(0)
plt.savefig('data/model/bias-model-0.png')

plt.figure()

plot_model(0.5)
plt.savefig('data/model/bias-model-0.5.png')

plt.figure()

plot_model(1)
plt.savefig('data/model/bias-model-1.png')

plt.show(block=True)