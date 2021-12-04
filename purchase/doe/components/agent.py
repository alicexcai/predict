import random

import math
from scipy.optimize import fsolve
from scipy.stats import skewnorm
from collections import defaultdict

# import numpy as np

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
    
    def purchase(self, mechanism, liquidity, outcomes, history, round_num, shares, probabilities, cost, signal):
        purchase = { outcome : 1 for outcome in outcomes }
        return purchase
    
    def __repr__(self):
        return "{class_name}({attributes})".format(class_name = type(self).__name__, attributes = self.__dict__)

class Basic(Agent):
    
    def __init__(self, id, name, balance):
        super().__init__(id, name, balance)
        self.type = 'basic'

    def purchase(self, mechanism, liquidity, outcomes, history, round_num, shares, probabilities, cost, signal):

        '''
        TO DO:
        write code for purchase strategy
        '''
        
        # Bid until probabilities = belief
        purchase = {}
        def calculate_shares(belief):
            for outcome in outcomes:
                if belief[outcome] > probabilities[round_num-1][outcome]:
                    if mechanism == 'logarithmic':
                        purchase[outcome] = math.log((sum([math.exp(shares[round_num-1][outcome] / liquidity) for outcome in outcomes]) * belief[outcome])/(1-belief[outcome]))   
                    # not sure if this is correct? pulled from https://slidetodoc.com/a-utility-framework-for-boundedloss-market-makers-yiling/
                    elif mechanism == 'quadratic':
                        purchase[outcome] = math.sqrt((sum([math.exp(shares[round_num-1][outcome] / liquidity) for outcome in outcomes]) * belief[outcome])/(1-belief[outcome]))
                else:
                    purchase[outcome] = 0
            return purchase
        
        # Adjust how agents calculate belief
        belief = { outcome : (signal.iloc[round_num-1][outcome] / sum([signal.iloc[round_num-1][outcome] for outcome in outcomes])) for outcome in outcomes }
        purchase = calculate_shares(belief)
        
        return purchase
    
        
class ZeroInt(Agent):
    def __init__(self, id, name, balance):
        super().__init__(id, name, balance)
        self.type = 'zero_intelligence'
        
    def purchase(self, mechanism, liquidity, outcomes, history, round_num, shares, probabilities, cost, signal):
        purchase = { outcome : random.random() * self.balance for outcome in outcomes }
        return purchase
    
class Superfan(Agent):
    def __init__(self, id, name, balance, team):
        super().__init__(id, name, balance)
        self.type = 'superfan'
        self.team = team
        
    def purchase(self, mechanism, liquidity, outcomes, history, round_num, shares, probabilities, cost, signal):
        lean_less_r = float(skewnorm.rvs(1000, loc=0, scale = 0.25, size=1))
        lean_more_r = float(skewnorm.rvs(-1000, loc=1, scale = 0.25, size=1))
        lean_less = lean_less_r if lean_less_r >= 0 and lean_less_r <= 1 else 0 if lean_less_r < 0 else 1
        lean_more = lean_more_r if lean_more_r >= 0 and lean_more_r <= 1 else 0 if lean_more_r < 0 else 1
        purchase = { outcome : lean_less * self.balance for outcome in outcomes }
        purchase[self.team] = lean_more * self.balance
        return purchase

class Dummy(Agent):
    def __init__(self, id, name, balance):
        super().__init__(id, name, balance)
        self.type = 'dummy'
        
    def purchase(self, mechanism, liquidity, outcomes, history, round_num, shares, probabilities, cost, signal):
        purchase = { outcome : random.random() * self.balance for outcome in outcomes }
        return purchase