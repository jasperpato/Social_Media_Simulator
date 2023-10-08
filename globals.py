NUM_AGENTS = 100
NUM_TIME_STEPS = 500

# number of time steps with no change to end the simulation
CONVERGENCE_NUM = 5

# proportion of posting agents
P = 0.3

# proportion of posts consumed per day
C = 1

# change in agent's opinion due to a post
D = 0.1

# -----------------------------------------

NUM_POSTERS = int(NUM_AGENTS * P)
POSTS_PER_DAY = int(NUM_POSTERS * C)
