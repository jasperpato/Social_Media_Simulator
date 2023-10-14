NUM_AGENTS = 500
NUM_TIME_STEPS = 1000
NUM_SIMULATIONS = 500

# number of time steps with no change to end the simulation
CONVERGENCE_NUM = 10

# proportion of posting agents
P = 0.5

# standard deviation of Gaussian noise applied to posts
POST_NOISE = 0

# proportion of posts consumed per day
C = 0.1

# change in agent's opinion due to a post
D = 0.1

# agent bias
B = 0.3

# biased platform parameters
PLATFORM_BIAS = 0
PLATFORMS = [round(i / 10, 1) for i in range(0, 51)] # 0-5 in steps of 0.1

RECOMMENDATION_BIAS = 1

POLARISATION_CUTOFF = 0.75
