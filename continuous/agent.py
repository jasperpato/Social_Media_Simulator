import numpy as np
from globals import *

class Agent:
    
    def __init__(self):
        self.is_poster = np.random.random() < P
        self.opinion = 2 * np.random.random() - 1
        self.opinions = [self.opinion]

    def consume_post(self, opinion):

        if self.opinion == 0:
            if opinion == 0:
                self.opinion += D if np.random.random() < 0.5 else -D
            else:
                self.opinion += D if opinion > 0 else -D

        else:
            diff = abs(opinion - self.opinion)
            
            if np.random.binomial(1, (1 - diff if diff < 1 else diff - 1)):
                self.opinion += D if self.opinion > 0 else D # strengthen opinion
            else:
                self.opinion += -D if self.opinion > 0 else D # weaken opinion

        self.opinion = max(-1, self.opinion)
        self.opinion = min(1, self.opinion)

        self.opinions.append(self.opinion)
