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

        '''
        TO DO:
        write code for purchase strategy
        '''
        
        purchase = signal
        
        return purchase
    
    # Is this necessary?
    def __repr__(self):
        return "%s(id = %d, name = %s, balance = %d)" % (
            self.__class__.__name__, self.id, self.name, self.balance)