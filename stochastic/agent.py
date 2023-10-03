import numpy as np
from globals import *

class Agent:
    
    def __init__(self, is_biased=False):
        self.is_biased = is_biased
        self.signal_mixes = [1 if P < np.random.random() else 0]
        self.update_orientation()

    def incongruent(self, signal_mix):
        return (signal_mix < 0.5 and self.orientation == 1) or (signal_mix >= 0.5 and self.orientation == -1)

    def receive_mix(self, signal_mix):
        '''
        Receives a signal mix from another agent and updates its own signal mix accordingly
        '''
        if self.is_biased and self.incongruent(signal_mix):
            signal_mix += 2 * Q * abs(signal_mix - 0.5) * (self.orientation)
        self.signal_mixes.append(signal_mix)

    def update_orientation(self):
        '''
        Updates the orientation of the agent based on the signal mix
        '''
        self.avg_mix = sum(self.signal_mixes) / len(self.signal_mixes)
        self.orientation = 1 if self.avg_mix > 0.5 else -1