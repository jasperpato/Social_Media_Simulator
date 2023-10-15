
# ----------------- simulation parameters ----------------------#

NUM_AGENTS = 5
NUM_TIME_STEPS = 1
NUM_SIMULATIONS = 5
POLARISATION_CUTOFF = 0.75	# agents with opinions outside [-cutoff, cutoff] are considered polarised
CONVERGENCE_NUM = 10		# number of time steps with no change to end the simulation

# ----------------- default hyperparameters ---------------------------#

B = 0.25		# agent bias
P = 0.5		# proportion of posting agents
N = 0		# standard deviation of Gaussian noise applied to posts
C = 0.1		# proportion of posts consumed per day
D = 0.1		# change in agent's opinion due to a post
PB = 1		# platform bias
RB = 1		# recommendation bias

