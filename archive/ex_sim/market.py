# doesn't matter what data structures are used within the simulation, as long as they can be parsed to optain the data necessary for graphing

'''
TODO:
-set constraints 

'''


from collections import defaultdict

from optparse import OptionParser
import itertools
import logging
import math
import random
import sys

from history import History
from stats import Stats

from .params import Params
from .agent import Agent

# from util import shuffled, mean, stddev

# Infinite stream of zeros
zeros = itertools.repeat(0)

config = Params(
    outcomes=['A', 'B', 'C'],
    # agents_dict={1: {'name': 'default', 'type': 'default', 'balance': 1000}, 2: {'name': 'default2',
    #                                                                              'type': 'default', 'balance': 1000}, 3: {'name': 'default3', 'type': 'default', 'balance': 1000}},
    agents_dict={Agent(1, 'first', 1000), Agent(2, 'second', 1000)},
    mechanism='logarithmic',
    liquidity=100.0,
    i_shares={0: {'A': 0.0, 'B': 0.0, 'C': 0.0}},

    num_rounds=100,
    loglevel='info',
    num_iterations=1,
)


def sim(config):

    outcomes = config.outcomes
    mechanism = config.mechanism
    liquidity = config.liquidity
    num_rounds = config.num_rounds
    # store shares, base other calculations on shares
    # assert mechanism == 'logarithmic' or 'quadratic', ValueError('mechanism must be logarithmic, quadratic, or linear')

    # variable
    agents_dict = config.agents_dict
    shares = config.i_shares
    payments = {0: {agent.id: {outcome: 0.0 for outcome in outcomes}
                    for agent in agents_dict}}
    p_shares = {0: {outcome: 0.0 for outcome in outcomes}}

    def Cost(shares, round_num):
        if mechanism == 'logarithmic':
            cost = liquidity * \
                math.log(sum([math.exp(shares[round_num][outcome] / liquidity)
                         for outcome in outcomes]))
        elif mechanism == 'quadratic':
            # is this correct?
            cost = liquidity * \
                sum([(shares[round_num][outcome] / liquidity) ** 2 for outcome in outcomes])

        return cost

    def Probabilities(shares, round_num):
        probabilities = {outcome: math.exp(shares[round_num][outcome] / liquidity) / sum(
            [math.exp(shares[round_num][outcome] / liquidity) for outcome in outcomes]) for outcome in outcomes}

        if mechanism == 'logarithmic':
            probabilities = {outcome: math.exp(shares[round_num][outcome] / liquidity) / sum(
                [math.exp(shares[round_num][outcome] / liquidity) for outcome in outcomes]) for outcome in outcomes}
        elif mechanism == 'quadratic':
            # is this correct?
            probabilities = {outcome: (shares[round_num][outcome] / liquidity) ** 2 / sum(
                [(shares[round_num][outcome] / liquidity) ** 2 for outcome in outcomes]) for outcome in outcomes}
        return probabilities

    def CostOfTrans(shares, p_shares):
        before_cost = Cost(shares, round_num)
        new_shares = {
            outcome: shares[round_num][outcome] + p_shares[round_num][outcome] for outcome in outcomes}
        after_cost = Cost(new_shares)
        cost_of_trans = after_cost - before_cost
        return cost_of_trans

    probabilities = {
        0: {outcome: Probabilities(shares, round_num=0) for outcome in outcomes}}
    cost = Cost(shares, round_num=0)

    # Introduce new agent mid-simulation - is this necessary?
    def init_agent(agents_dict, newagent_name, newagent_balance):
        # new_agent = Agent(len(agents_dict)+1, new_agent_name, new_agent_balance)
        agents_dict.update(
            Agent(len(agents_dict)+1, newagent_name, newagent_balance))

    # # Dictionaries : round # : data
    # shares = defaultdict(dict)  # { round # : { outcome : shares } }
    # # { round # : { agent : { outcome : payment } }
    # payments = defaultdict(defaultdict(dict))
    # costs = []  # { round # : cost }
    # # { round # : { outcome : probability } }
    # probabilities = defaultdict(dict)
    # revenue = 0  # final net revenue
    # utilities = {}  # { agent : final utility }
    # # { round # : { agent : { outcome : p_share } } }
    # p_shares = defaultdict(defaultdict(dict))

    history = History(cost, shares, probabilities, p_shares, payments)

    # round is an arbitrary alias for a unit of time, agents can choose to trade in different round intervals, simulating trade frequency
    def run_round(shares, round_num):
        
        # example signal
        signal = { outcome : random.random() for outcome in outcomes }

        # Log purchased shares determined by agents
        for agent in agents_dict:
            requested_purchase = agent.purchase(history, round_num, shares, signal)
            if requested_purchase <= agent.balance:
                p_shares[round_num][agent.id] = requested_purchase
            elif requested_purchase > agent.balance:
                p_shares[round_num][agent.id] = agent.balance
        # update shares
            for outcome in outcomes:
                # shares for each round = after purchase
                shares[round_num][outcome] += p_shares[round_num][agent.id][outcome]
        # update agent balance, calculate payments based on mechanism
            payments[round_num][agent.id] = CostOfTrans(
                shares, p_shares[round_num][agent.id])
            agent.balance -= payments[round_num][agent.id]

        # new cost and probabilities post-purchase
        cost[round_num] = Cost(shares, round_num)
        probabilities[round_num] = Probabilities(shares, round_num)

        '''
        Introduce round-specific actions here:
        
        e.g. introduce new agents at certain rounds:
        if round_num == 10:
            init_agent(agents_dict, agent)
            
        e.g. add balance to agents at certain rounds:
        if round_num == 10:
            for agent in agents_dict:
                agents_dict[agent].balance += 1000
        '''

        # Debugging. Set to True to see what's happening.
        log_console = True
        if log_console:
            logging.info("\t=== Round %d ===" % round_num)
            logging.info("\tPurchased shares: %s" % p_shares[round_num])
            logging.info("\tUpdated shares: %s" % shares[round_num])
            logging.info("\tPayments made: %s" % payments[round_num])
            logging.info("\tUpdated probabilities: %s" %
                         probabilities[round_num])
            logging.info("\tUpdated cost: %s" % cost[round_num])

    # RUN ROUNDS
    for round_num in range(config.num_rounds):
        # Consider using 240 rounds to simulate a 4 hour game with trading every 1 sec?

        run_round(shares, round_num)

    return history

# Not sure how much of this is useful?


def configure_logging(loglevel):
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    root_logger = logging.getLogger('')
    strm_out = logging.StreamHandler(sys.__stdout__)
    strm_out.setFormatter(logging.Formatter('%(message)s'))
    root_logger.setLevel(numeric_level)
    root_logger.addHandler(strm_out)


# def main(params):  # pass in params object
#     logging.info("Parameters: ", params)
#     configure_logging(params.loglevel)

#     logging.info("Starting simulation...")

#     #  iters = no. of samples to take
#     for i in range(params.iterations):
#         logging.info("==== Iteration %d / %d ====" %
#                      (i, params.iterations))

#         history = sim(params)
#         stats = Stats(history)
#         # Print stats in console?
#         logging.info("==== Stats for Iteration %d ====\n %d" %
#                      (i, stats))
        
#     # Output data into HDF5 / database
#     return stats

# if __name__ == "__main__":
#     main(sys.argv)

sim(config)