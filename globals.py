NUM_AGENTS = 100
NUM_TIME_STEPS = 100

# number of time steps with no change to end the simulation
CONVERGENCE_NUM = 10

# proportion of posting agents
P = 0.3

# standard deviation of Gaussian noise applied to posts
POST_NOISE = 0.05

# proportion of posts consumed per day
C = 0.1

# change in agent's opinion due to a post
D = 0.1

# biased platform parameters
PLATFORM_BIAS = 1
RECOMMENDATION_BIAS = 0

# ---------- simulations ----------

# STEP = 0.01
# BS = [round(STEP * i, 3) for i in range(0, int(1 / STEP) + 1)]

BS = [0.5]

NUM_SIMULATIONS = 1

# ---------- util ----------

NUM_POSTERS = int(NUM_AGENTS * P)
POSTS_PER_DAY = int(NUM_POSTERS * C)
