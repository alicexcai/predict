from agent import Agent

class Params():

    def __init__(self,
                 outcomes=['Y', 'N'],
                 agents_dict={Agent(1, 'first', 1000)},
                 mechanism='logarithmic',
                 liquidity=100.0,
                 i_shares={0: {'Y': 0.0, 'N': 0.0}},

                 num_rounds=100,
                 loglevel='info',
                 num_iterations=1,
                 ):
        self.outcomes = outcomes
        self.agents_dict = agents_dict
        self.mechanism = mechanism
        self.liquidity = liquidity
        self.i_shares = i_shares
        self.num_rounds = num_rounds
        self.loglevel = loglevel
        self.num_iterations = num_iterations