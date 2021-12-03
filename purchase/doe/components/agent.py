import random

from numpy import round_

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
                
        print("SIGNAL", signal)
        
        print("HISTORY COST", history.cost)
        
        print("CURRENT PRICE", cost)
        
        print("ROUND NUM", round_num)
        
        purchase = { 
                    'Harvard': random.random() * self.balance/10 * (signal.iloc[round_num-1]['Harvard'] / (signal.iloc[round_num-1]['Harvard'] + signal.iloc[round_num-1]['Yale'])),
                    'Yale': random.random() * self.balance/10 * (signal.iloc[round_num-1]['Yale'] / (signal.iloc[round_num-1]['Harvard'] + signal.iloc[round_num-1]['Yale']))}
        
        # purchase = { outcome : random.random() * self.balance/10 * (signal.iloc[round_num][outcome] / sum([signal.iloc[round_num][outcome] for outcome in outcomes])) for outcome in outcomes }

        print("PURCHASE", purchase)
        # purchase = signal
        
        return purchase
    
    # Is this necessary?
    def __repr__(self):
        return "%s(id = %d, name = %s, balance = %d)" % (
            self.__class__.__name__, self.id, self.name, self.balance)
        
# class ZeroInt(Agent):
    