NUM_AGENTS = 100
NUM_TIME_STEPS = 500

# ---- parameters -----

P = 0.3 # proportion of posting agents
C = 1 # proportion of posts consumed per day

B = 0.3 # level of agents' confirmation bias (between 0 and 1)

D = 0.1 # value of change in opinion due to a post

# ---------------------

NUM_POSTERS = int(NUM_AGENTS * P)
POSTS_PER_DAY = int(NUM_POSTERS * C)

M = -(B + 1)/(B - 1)/2
C = 1 - 2*M