NUM_AGENTS = 500
NUM_TIME_STEPS = 500

# number of time steps with no change to end the simulation
CONVERGENCE_NUM = 10

# proportion of posting agents
P = 0.75

# standard deviation of Gaussian noise applied to posts
POST_NOISE = 0 # 0.05

# proportion of posts consumed per day
C = 0.1

# change in agent's opinion due to a post
D = 0.1

# biased platform parameters
PLATFORM_BIAS = 0
RECOMMENDATION_BIAS = 0

POLARISATION_CUTOFF = 0.75

# ---------- simulations ----------

STEP = 0.01
BS = [round(STEP * i, 3) for i in range(0, int(1 / STEP) + 1)]

NUM_SIMULATIONS = 500

# ---------- util ----------

NUM_POSTERS = int(NUM_AGENTS * P)
POSTS_PER_DAY = int(NUM_POSTERS * C)
