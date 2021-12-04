import random

import math
from scipy.optimize import fsolve
from scipy.stats import skewnorm
from collections import defaultdict
from .agent import Agent


"""
Start with Nerd class:
- Regression to predict future value (linear, quadratic, etc.)
- Base signal: history of scores, time remaining [history of shares]
- Time weighting: 1/x
- Budget awareness: budget-remaining/rounds-remaining vs budget/round

ML agent?
other-aware agent?
late bidder - David Parkes

"""
        
class Nerd(Agent):
    def __init__(self, id, name, balance):
        super().__init__(id, name, balance)
        self.type = 'zero_intelligence'
        
    def purchase(self, mechanism, liquidity, outcomes, history, round_num, shares, probabilities, cost, signal):
        
        # print("SIGNAL", signal)
        print("PROBABILITIES", probabilities )
        
        purchase = { outcome : random.random() * self.balance for outcome in outcomes }
        return purchase
    