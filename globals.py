NUM_DAYS = 1000
NUM_AGENTS = 100
NUM_OPINIONS = 10

# making posts
PROPORTION_POSTING_AGENTS = 0.1
POST_GENERATION_NOISE = 0.2

# choosing posts for an agent
# posts that align with the agent's opinions have higher probability of being chosen
# posts that align with the platform's opinions have higher probability of being chosen for any agent
PLATFORM_INFLUENCE = 0.5

# consuming posts
POSTS_PER_DAY = 50 # must be <= NUM_AGENTS * PROPORTION_POSTING_AGENTS
POST_INFLUENCE = 0.1