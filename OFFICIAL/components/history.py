import copy
import pandas as pd

# History stores bare-bone basic information about the history of a game. More sophisticated queries can be made by agents if desired.
class History:
    
    class RoundHistory:
        
        """
        Allows agents to access the history of a previous round.
        Makes copies so clients can't change history.
        """
        
        # agent-agnostic aggregates by outcome
        def __init__(self, cost, shares, probabilities, p_shares, payments):
            self.cost = copy.deepcopy(cost) # float
            self.shares = copy.deepcopy(shares) # dict { outcome : shares }
            self.probabilities = copy.deepcopy(probabilities) # dict
            self.p_shares = copy.deepcopy(p_shares) # dict of dict { agent : { outcome : shares, ... }, ... }
            self.payments = copy.deepcopy(payments) # dict of dict { agent : { outcome : payments, ... }, ... }

    def __init__(self, cost, shares, probabilities, p_shares, payments):
        self.round = lambda round_num: History.RoundHistory(
            cost[round_num], shares[round_num], probabilities[round_num], p_shares[round_num], payments[round_num])
        self.cost = cost
        self.shares = shares
        self.probabilities = probabilities
        self.p_shares = p_shares
        self.payments = payments
        
    # unused - OMIT?
    def get_data(self, cost, shares, probabilities, p_shares, payments):
        history_data_dict = {'cost': cost, 
                'shares': shares, 
                'probabilities': probabilities,
                'p_shares': p_shares,
                'payments': payments
                }
        history_data = pd.DataFramefrom_dict(history_data_dict)
        return history_data
        
        

