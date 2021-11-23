import simpy
import random
import statistics
import vcg as vcg
import gsp as gsp
import lmsr as lmsr
import stats as stats
from collections import defaultdict
import logging
import csv

'''
Features
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
agent_names = ["default", "johnharvard", "yalie"]
for agent in agent_names:
    globals()[agent] = importlib.import_module(agent)

outcomes = []
predictions_i = {outcome : [0] for outcome in outcomes} # initializing the predictions

parameters = defaultdict() # parameter : value

# truth source - data
with open('data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row['time'], row['score'])



# What are the outputs / metrics?

# Outputs (single round): perform statistics on the following
utilities = [] # ctr(value - bid)
payments = defaultdict(list()) # agent : [list of payments as tuple (trading agent (AMM), quantity, price, time)]
predictions = defaultdict(list()) # outcome : [probabilities every 1 s]
prices = [] # instantaneous prices determined every 1 s (arbitrary?) by imported payment rule
revenue = 0 # final revenue for auction

# Statistics
ag_utilities = [] # list of lists
ag_payments = [] # list of dicts of lists
ag_predictions = [] # list of dicts of lists
ag_prices = [] # list of lists
ag_revenue = [] # list of floats

# Statistical Analysis
stats.graph(ag_utilities, ag_payments, ag_predictions, ag_prices, ag_revenue)



