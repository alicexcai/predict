import vcg as vcg
import gsp as gsp
import lmsr as lmsr
import stats as stats

import simpy
import random
import statistics
from collections import defaultdict
import logging
import csv
import math

'''
Assumptions:
-LMSR AMM with payout of 1 per share

Features:
-randomized
-fit into PARAM
-clean / readable / as simple as possible

Cost Function
Cost of Transaction
Marginal Price aka probability

Classes:
Agents 
Bids
Markets

Meta:
history (round)
parameters
'''

# What are the inputs / parameters?

# imports all agents, modify code to be more useful later
import importlib
agent_names = ["truthfulA", "johnharvardA", "yalieA"] # list of agents
for agent in agent_names:
    globals()[agent] = importlib.import_module(agent)

outcomes = [] # list of outcomes
prices = {outcome : [0] for outcome in outcomes} # initializing the prices / predictions, not necessarily at 0
shares = [] # shares of each outcome

parameters = defaultdict() # parameter : value
# incorporate GUI / UI to initialize liquidity / other params
liquidity = 100.0 # beta, higher leads to smaller impact of trading

# truth source - data
with open('data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['time'], row['harvard_score'], row['yale_score'])


# What are the outputs / metrics?

# Outputs (single round): perform statistics on the following
utilities = [] # ctr(value - bid)
payments = defaultdict(list()) # agent : [list of payments as tuple (trading agent (AMM), quantity, price, time)]
prices = defaultdict(list()) # outcome : instantaneous prices determined every 1 s (arbitrary?) by imported payment rule
revenue = 0 # final revenue for auction

'''
predictions = prices # outcome : [probabilities every 1 s], pulled directly from prices
shares = defaultdict(list()) # shares of each outcome at each stage
'''

# Statistics
ag_utilities = [] # list of lists
ag_payments = [] # list of dicts of lists
ag_prices = [] # list of lists
ag_revenue = [] # list of floats

'''
ag_predictions = [] # list of dicts of lists
ag_shares = [] # list of dicts of lists
'''

# Statistical Analysis
stats.graph(ag_utilities, ag_payments, ag_prices, ag_revenue)


# Methods

# Probability = price
#  C(x,y) = 100.0 * ln(exp(20/100) + exp(10/100)) = 100.0 * ln(1.22 + 1.11) = 100.0 * 0.8444 = $84.44
# liquidity * ln(exp(share outcome i / liquidit + share outcome i / liqui))

# Current cost of one share of each outcome - should there be multiple costs (outcome array)?
def Cost(shares, liquidity):
    # sum = 0.0
    # for i in range(2):
    #     sum += math.exp(shares[i] / liquidity)
    # return liq * math.log(sum)
    cost = liquidity * math.log(sum([math.exp(shares[i] / liquidity) for i in range(len(outcomes))]))
    return cost

# Price of each outcome?
def Probabilities(shares, liquidity):
    result = [0.0, 0.0]
    denom = 0.0
    for i in range(len(outcomes)):
        denom += math.exp(shares[i] / liquidity)
    for i in range(2):
        result[i] = math.exp(shares[i] / liquidity) / denom
    return result

def CostOfTrans(shares, idx, nShares, liquidity):
    after = [0, 0]
    after[:] = shares
    after[idx] += nShares
    return Cost(after, liquidity) - Cost(shares, liquidity)

def CostForOneShare(shares, liquidity):
    result = [0.0, 0.0]
    result[0] = CostOfTrans(shares, 0, 1, liquidity)
    result[1] = CostOfTrans(shares, 1, 1, liquidity)
    return result