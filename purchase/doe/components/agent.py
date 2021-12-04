import random

import numpy as np

class Agent:
    
    def __init__(self, id, name, balance):
        self.id = id
        self.name = name  # alias
        self.balance = balance
        self.type = 'default'
        
    # agent-centric history
    def get_history(self, history):
        # agent purchase history stored in a dictionary of dictionaries { round : { outcome : shares, ... }, ... } for each agent
        agent_history = { round : history.p_shares[self.id] for round in history.rounds }
        return agent_history

    def purchase(self, mechanism, liquidity, outcomes, history, round_num, shares, cost, signal):

        '''
        TO DO:
        write code for purchase strategy
        '''
                
        # print("SIGNAL", signal)
        
        # print("HISTORY COST", history.cost)
        
        # print("CURRENT PRICE", cost)
        
        # print("ROUND NUM", round_num)
        
        # purchase = { 
        #             'Harvard': random.random() * self.balance/10 * (signal.iloc[round_num-1]['Harvard'] / (signal.iloc[round_num-1]['Harvard'] + signal.iloc[round_num-1]['Yale'])),
        #             'Yale': random.random() * self.balance/10 * (signal.iloc[round_num-1]['Yale'] / (signal.iloc[round_num-1]['Harvard'] + signal.iloc[round_num-1]['Yale']))}
        
        # format: { outcome :  shares, ... } Probability formula
        
        
    # def Probabilities(shares):
    #     if mechanism == 'logarithmic':
    #         probabilities = {outcome: math.exp(shares[outcome] / liquidity) / sum(
    #             [math.exp(shares[outcome] / liquidity) for outcome in outcomes]) for outcome in outcomes}
    #     elif mechanism == 'quadratic':
    #         # is this correct?
    #         probabilities = {outcome: (shares[outcome] / liquidity) ** 2 / sum(
    #             [(shares[outcome] / liquidity) ** 2 for outcome in outcomes]) for outcome in outcomes}
    #     return probabilities
        
        print("SIGNAL", signal)
        purchase = { outcome : random.random() * self.balance/100 * (signal.iloc[round_num-1][outcome] / sum([signal.iloc[round_num-1][outcome] for outcome in outcomes])) for outcome in outcomes }
        print("PURCHASE", purchase)
        
        # purchase = { outcome : random.random() for outcome in outcomes }
        # purchase = signal
        
        return purchase
    
    # Is this necessary?
    def __repr__(self):
        return "{class_name}({attributes})".format(class_name = type(self).__name__, attributes = self.__dict__)
        
class ZeroInt(Agent):
    def __init__(self, id, name, balance):
        super().__init__(id, name, balance)
        self.type = 'zero_intelligence'
        
    def purchase(self, mechanism, liquidity, outcomes, history, round_num, shares, cost, signal):
        purchase = signal
        return purchase

[id, name, balance] = [1, 'hi', 100]
test = ZeroInt(id, name, balance)
print(test.__repr__())