import numpy as np
from globals import *

class Agent:
    
    def __init__(self, is_biased=False):
        self.is_biased = is_biased
        self.signal_mix = 1 if P < np.random.random() else 0
        self.num_signals = 1
        self.update_orientation()

    def receive_sums(self, neighbour: 'Agent'):
        '''
        Receives a signal mix from another agent and updates its own signal mix accordingly
        '''
        if self.is_biased:
            num_pos = neighbour.signal_mix * neighbour.num_signals
            num_incongruent = neighbour.num_signals - num_pos if self.orientation == 1 else num_pos
            num_incongruent -= np.random.binomial(num_incongruent, Q) # replace incongruent signals with prob Q
            self.signal_mix = (self.signal_mix * self.num_signals + (neighbour.num_signals - num_incongruent)) / (self.num_signals + neighbour.num_signals)
        
        else:
            self.signal_mix = (self.signal_mix * self.num_signals + neighbour.signal_mix * neighbour.num_signals) / (self.num_signals + neighbour.num_signals)
        
        self.num_signals += neighbour.num_signals

    def update_orientation(self):
        '''
        Updates the orientation of the agent based on the signal mix
        '''
        self.orientation = 1 if self.signal_mix > 0.5 else -1