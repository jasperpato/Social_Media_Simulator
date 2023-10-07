from agent import Agent
from media_platform import MediaPlatform
import matplotlib.pyplot as plt
import numpy as np
import random
from globals import *
import sys

PLATFORM_BIAS = 2
RECOMMENDATION_BIAS = 1


class BiasedMediaPlatform(MediaPlatform):
      def __init__(self, opinion=1, verbose=False):
            super().__init__(opinion, verbose)  
            self.posts = np.array([a.opinion for a in self.agents[:NUM_POSTERS]])
            [self.platform_opinion] = random.sample([-1, 1], 1)
		
		
      def serve_posts(self):
            self.posts = np.array([a.opinion for a in self.agents[:NUM_POSTERS]])
            ctc = np.zeros((NUM_POSTERS, NUM_AGENTS))  # creator to consumer matrix
            ctc = ctc + np.reshape(self.posts, (NUM_POSTERS, 1))
                  
            # calculate similarity between creator and consumer opinions
            ctc_consumer_sim = np.log(np.abs(ctc - self.prev_opinions + sys.float_info.epsilon) / 2)
            # calculate similarity between creator and platform opinions
            ctc_platform_sim = np.log(np.abs(ctc - self.platform_opinion + sys.float_info.epsilon) / 2)
            
            ctc = PLATFORM_BIAS * ctc_platform_sim + RECOMMENDATION_BIAS * ctc_consumer_sim
            ctc = ctc / np.max(ctc, axis=0, keepdims=True)               # normalize with max of each agent's posts
            ctc[np.diag_indices(NUM_POSTERS)] = 0                        # posters should not consume their own posts
            return ctc


      def time_step(self):
            '''
                  Each agent consumes its own served posts
            '''
            ctc = self.serve_posts().T                                              # transpose to get consumer to creator matrix
            posts_received = (np.random.rand(NUM_AGENTS, NUM_POSTERS) < ctc)        # return boolean matrix of posts served to each agent
            for i in range(NUM_AGENTS):
                  posts_i = self.posts[posts_received[i]]
                  post_scores = ctc[i][posts_received[i]]

                  # sort posts by score and take the top POSTS_PER_DAY
                  selected_posts = posts_i[np.argsort(post_scores)][::-1][:POSTS_PER_DAY]
                  unselected_posts = self.posts[~posts_received[i]]
                  
                  if len(selected_posts) < POSTS_PER_DAY:
                        sampled_posts = np.random.choice(unselected_posts, size = POSTS_PER_DAY - len(selected_posts), replace = False)
                        selected_posts = np.concatenate((selected_posts, sampled_posts))

                  for p in selected_posts:
                        self.agents[i].consume_post(p)
			
	
def simulate():
	'''
	Execute an entire simulation
	'''
	m = BiasedMediaPlatform()
	m.simulate()
	m.graph()
	return (m.fractions(), m.platform_opinion)

SIMULATIONS = 1

if __name__ == '__main__':
      fractions = []
      platform_opinions = []
      try:
            for i in range(SIMULATIONS):
                  f, opinion = simulate()
                  fractions.append(f)
                  platform_opinions.append(opinion)

      except KeyboardInterrupt:
            pass

      print(fractions)
      print(platform_opinions)
      plt.show(block=True)

