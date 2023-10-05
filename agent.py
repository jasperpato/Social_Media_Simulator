import random
from globals import *

class Agent:
    
    def __init__(self):
        self.is_poster = random.random() < K
        self.is_biased = random.random() < B
        self.signals = [1 if random.random() < P else -1]
        self.update_orientation()

    def update_orientation(self):
        '''
        Current orientation is equal to the most common signal received
        '''
        self.orientation = 1 if sum(self.signals) / len(self.signals) >= 0 else -1

    def receive_signal(self, signal):
        '''
        Receives a signal from another agent
        '''
        if self.is_biased and signal != self.orientation and random.random() < Q:
            self.signals.append(self.orientation)
            return
        self.signals.append(signal)