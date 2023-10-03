import numpy as np

REJECTION_PROBABILITY = 0.7
SIGNAL_CONFIDENCE = 0.6 # probability of a signal supporting ground truth 

class Agent:
    
    def __init__(self, p=SIGNAL_CONFIDENCE, is_biased=False):
        '''
        Initialises an agent with an initial signal s_i that is informative of the ground truth X
        where p is the probability of s_i matching X. I.e., P(s_i = +1 | X = +1)
        '''
        self.is_biased = is_biased
        self.signal_sums = [0, 1] if p < np.random.random() else [1, 0]
        self.update_orientation()

    def receive_sums(self, neighbour: 'Agent'):
        '''
        Receives a signal mix from another agent and updates its own signal mix accordingly
        '''
        if self.is_biased:
            self.__receive_signals_biased(neighbour)
        else:
            self.signal_sums += neighbour.signal_sums
            
    
    def __receive_signals_biased(self, neighbour: 'Agent'):
        '''
        Receives a signal mix from another agent and updates its own signal mix accordingly
        '''
        ind_congruent, ind_incongruent = [0, 1] if self.orientation == 1 else [1, 0]

        # signals that align with agent's orientation
        self.signal_sums[ind_congruent] += neighbour.signal_sums[ind_congruent]
        
        # signals that do not align (may get rejected)
        num_rejected = np.random.binomial(neighbour.signal_sums[ind_incongruent], REJECTION_PROBABILITY)
        self.signal_sums[ind_congruent] += num_rejected
        self.signal_sums[ind_incongruent] += neighbour.signal_sums[ind_incongruent] - num_rejected

    def update_orientation(self):
        '''
        Updates the orientation of the agent based on the signal mix
        '''
        self.signal_mix = self.signal_sums[0] / (np.sum(self.signal_sums))
        self.orientation = 1 if self.signal_mix > 0.5 else -1