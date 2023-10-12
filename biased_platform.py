from agent import Agent
from media_platform import MediaPlatform
import matplotlib.pyplot as plt
import numpy as np
import random
from globals import *
import sys

PLATFORM_BIAS = 1
RECOMMENDATION_BIAS = 1


class BiasedMediaPlatform(MediaPlatform):
      def __init__(self, opinion=1, verbose=False):
            super().__init__(opinion, verbose)  
            self.posts = np.array([a.opinion for a in self.agents[:NUM_POSTERS]])
            [self.platform_opinion] = random.sample([-1, 1], 1)
		
		
      def serve_posts(self):
            ctc = np.zeros((NUM_POSTERS, NUM_AGENTS))  # creator to consumer matrix
            ctc = ctc + np.reshape(self.posts, (NUM_POSTERS, 1))
                  
            # calculate similarity between creator and consumer opinions
            ctc_consumer_sim = 2 - np.abs(ctc - self.prev_opinions) + sys.float_info.epsilon
            # calculate similarity between creator and platform opinions
            ctc_platform_sim = 2 - np.abs(ctc - self.platform_opinion) + sys.float_info.epsilon
            
            ctc = PLATFORM_BIAS * ctc_platform_sim + RECOMMENDATION_BIAS * ctc_consumer_sim
            ctc = ctc / np.max(ctc, axis=0, keepdims=True)               # normalize with max of each agent's posts
            ctc[np.diag_indices(NUM_POSTERS)] = 0                        # posters should not consume their own posts
            return ctc


      def time_step(self):
            '''
                  Each agent consumes its own served posts
            '''
            self.posts = np.array([a.opinion for a in self.agents[:NUM_POSTERS]])
            ctc = self.serve_posts()
            
            for i in range(NUM_AGENTS):
                  # sort posts by score and take the top POSTS_PER_DAY
                  selected_posts = self.posts[np.argsort(ctc[:, i])][::-1][:POSTS_PER_DAY]

                  for p in selected_posts:
                        self.agents[i].consume_post(p)
                  
                  self.agents[i].opinions.append(self.agents[i].opinion)
			
	
if __name__ == '__main__':
	if __name__ == '__main__':
		np.random.seed(40)
		m = BiasedMediaPlatform()
		m.simulate()
		print(m.fractions())
		print(m.platform_opinion)
		m.graph()
		plt.show(block=True)

