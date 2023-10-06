NUM_AGENTS = 100
NUM_TIME_STEPS = 500

CONVERGENCE_NUM = 10 # number of time steps with no change to end the simulation

# ---- parameters -----

P = 0.3 # proportion of posting agents
C = 1 # proportion of posts consumed per day

B = 0.3 # level of agents' confirmation bias (between 0 and 1)

D = 0.1 # value of change in opinion due to a post

# ---------------------

NUM_POSTERS = int(NUM_AGENTS * P)
POSTS_PER_DAY = int(NUM_POSTERS * C)

if B > 0:
	M = (2 - B)/(2 * B)
	C = 1 - 2*M