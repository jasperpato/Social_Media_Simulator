NUM_AGENTS = 100
NUM_TIME_STEPS = 500

# number of time steps with no change to end the simulation
CONVERGENCE_NUM = 100

# -------------- PARAMETERS ---------------

# proportion of posting agents
P = 0.3

# proportion of posts consumed per day
C = 1

# level of agents' confirmation bias (between 0 and 1)
B = 0.25

# change in agent's opinion due to a post
D = 0.1

# -----------------------------------------

NUM_POSTERS = int(NUM_AGENTS * P)
POSTS_PER_DAY = int(NUM_POSTERS * C)

if B > 0:
	M = (2 - B)/(2 * B)
	C = 1 - 2*M