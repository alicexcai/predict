import sympy
from sympy.abc import x
import math


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

    def purchase(self, mechanism, liquidity, outcomes, history, round_num, shares, signal):
        
        # signal = {'outcome': 'probability', ... }, derived from change in information * weight
        # code for purchase strategy
        
        
        
        # def Probabilities(shares):
    
        #     if mechanism == 'logarithmic':
        #         probabilities = {outcome: math.exp(shares[round_num][outcome] / liquidity) / sum(
        #             [math.exp(shares[round_num][outcome] / liquidity) for outcome in outcomes]) for outcome in outcomes}
        #     elif mechanism == 'quadratic':
        #         # is this correct?
        #         probabilities = {outcome: (shares[round_num][outcome] / liquidity) ** 2 / sum(
        #             [(shares[round_num][outcome] / liquidity) ** 2 for outcome in outcomes]) for outcome in outcomes}
        #     return probabilities
        
        # target_shares = sympy.solve(Probabilities(x) - signal, 'x')
        
        # purchase = { outcome : target_shares[round_num][outcome] - shares[round_num][outcome] for outcome in shares[round_num].keys() }
        
        
        
        
        # purchase = {}
        # for outcome in shares[round_num].keys():
        #     purchase[outcome] = target_shares[round_num][outcome] - shares[round_num][outcome]
        
        purchase = signal
        # purchase = { outcome: 0.0 for outcome in outcomes }
        
        return purchase
    
    # Is this necessary?
    def __repr__(self):
        return "%s(id = %d, name = %d, balance = %d)" % (
            self.__class__.__name__, self.id, self.name, self.balance)