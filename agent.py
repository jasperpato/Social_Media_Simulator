import numpy as np
import networkx as nx

REJECTION_PROBABILITY = 0.7
SIGNAL_CONFIDENCE = 0.6         # probability of a signal supporting ground truth 


class Agent:
    
    def __init__(self, p=SIGNAL_CONFIDENCE, is_biased=False):
        ''' Initialises an agent with an initial signal s_i that is informative of the ground truth X
        where p is the probability of s_i matching X. I.e., P(s_i = +1|X = +1) '''
        
        self.is_biased = is_biased
        self.signal_mix = np.array([0, 0])       # [support ground truth, detract from ground truth]
        self.signal_mix[np.random.choice([0, 1], p=[p, 1-p])] += 1


    def receive_signals(self, signal_mix):
        ''' Receives a signal mix from another agent and updates its own signal mix accordingly '''
        if not self.is_biased: 
            self.signal_mix += signal_mix
        else:
            self.__receive_signals_biased(self, signal_mix)


    def update_opinion(self):
        ''' Updates the opinion of the agent based on the signal mix '''
        self.opinion = self.signal_mix[0] / (np.sum(self.signal_mix))
        self.orientation = 1 if self.opinion > 0.5 else -1

    
    def __receive_signals_biased(self, signal_mix):
        ''' Receives a signal mix from another agent and updates its own signal mix accordingly '''
        ind_congruent = 0
        ind_incongruent = 1

        if self.orientation == -1:
            ind_congruent = 1
            ind_incongruent = 0

        self.signal_mix[ind_congruent] += signal_mix[ind_congruent]
        for _ in range(signal_mix[ind_incongruent]):
            if np.random.random() < REJECTION_PROBABILITY:
                self.signal_mix[ind_congruent] += 1       # if signal is rejected, replace it with a signal that supports the agent's opinion
            else:
                self.signal_mix[ind_incongruent] += 1
            

        

    
    


