# [ABANDONED] An attempt to make sim_mvp.py more sophisticated. Abandoned for ./simulation suite.

import simpy
import random
import statistics
from collections import defaultdict
import logging
import csv
import math
import numpy as np

'''
FEATURES
-config, default config

'''


# import importlib
# agent_names = ["truthfulA", "johnharvardA", "yalieA"]
# for agent in agent_names:
#     globals()[agent] = importlib.import_module(agent)

# with open('data.csv', newline='') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         print(row['time'], row['harvard_score'], row['yale_score'])

parameters = defaultdict()
outcomes = []
# prices = {outcome: [0] for outcome in outcomes}
total_shares = defaultdict(list)
# liquidity = 100.0
total_payments = defaultdict(list)
total_costs = []
total_probabilities = defaultdict(list)
revenue = 0
utilities = []

ag_total_payments = []
ag_total_probabilities = []
ag_total_costs = []
ag_revenue = []
ag_utilities = []

def IncrementRound(purchased_shares, shares, round):
    round += 1
    for outcome in outcomes:
        shares[outcome] += purchased_shares[outcome]
    return shares

def Cost(shares, liquidity):
    cost = liquidity * \
        math.log(sum([math.exp(shares[outcome] / liquidity)
                 for outcome in outcomes]))
    return cost

def Probabilities(shares, liquidity):
    probabilities = {outcome: math.exp(shares[outcome] / liquidity) / sum(
        [math.exp(shares[outcome] / liquidity) for outcome in outcomes]) for outcome in outcomes}
    return probabilities


def CostOfTrans(shares, purchased_shares, liquidity):
    before_cost = Cost(shares, liquidity)
    after_cost = Cost(IncrementRound(purchased_shares, shares, round), liquidity)
    cost_of_trans = after_cost - before_cost
    return cost_of_trans


def UnitCosts(shares, liquidity):
    unit_costs = {outcome : CostOfTrans(shares, {outcome: np.identity(len(outcomes))[i][j] 
                    for j, outcome in enumerate(outcomes)}, liquidity) for i, outcome in enumerate(outcomes)}
    return unit_costs



def main():
    # demo

    print('Starting prediction market...')
    print('Initial parameters:\n' + str(parameters))
    for i in range(50):
        
        ps = {outcome: random.randint(1, 50) for outcome in outcomes}
        print('BEFORE', shares)
        IncrementRound(ps, shares, round)
        print('AFTER', shares)
        # does this update shares globally or do we need shares = IncrementRound(ps, shares, round)?
        print('Round ' + str(round) +
                     ' Update: new purchase of ' + str(ps) + ' shares')
        
        print('Cost of transaction: ' + str(CostOfTrans(shares, ps, liquidity)))
        print('Updated probabilities: ' + str(Probabilities(shares, liquidity)))
        print('Updated unit costs: ' + str(UnitCosts(shares, liquidity)))
        
        print('Updating total data...\n')
        
        total_costs.append(Cost(shares, liquidity))
        for outcome in outcomes:
            total_probabilities[outcome].append(Probabilities(shares, liquidity)[outcome])
            total_payments[outcome].append(CostOfTrans(shares, ps, liquidity))
            total_shares[outcome].append(shares[outcome])
    print('Updated total data:\nTotal Costs: ' + str(total_costs) + '\nTotal Probabilities: ' + str(total_probabilities) + '\nTotal Payments: ' + str(total_payments) + '\nTotal Shares: ' + str(total_shares))

    


# TEST

liquidity = 100.0
outcomes = ["A", "B", "C"]

round = 0
shares = {"A": 0, "B": 0, "C": 0}

probabilities = Probabilities(shares, liquidity)
cost = Cost(shares, liquidity)
parameters = {"outcomes": outcomes, "initial shares": shares, "initial cost": cost,
              "initial probabilities": probabilities, "liquidity param": liquidity}

main()
