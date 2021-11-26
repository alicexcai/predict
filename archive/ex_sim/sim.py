from collections import defaultdict
import itertools
import pandas as pd
import market as tosim
# from gui import *

test_param_ranges = {
    'loglevel': ['info'], # ['info', 'debug']
    'mechanism': ['vcg'], # ['vcg', 'gsp', 'switch']
    'num_rounds': [3], # int
    'min_val': [25], # int
    'max_val': [175],
    'budget': [500000], # int
    'max_perms': [10],# int
    'iters': [1], # int
    'seed': [1, 2], # int
    'agent_names': [['Truthful', 'Truthful', 'Truthful']] # Truthful, NANewbb
}

class Params():
    
    def __init__(self, loglevel='info', mechanism='vcg', num_rounds=48, min_val=25, max_val=175, budget=500000, max_perms=120, iters=1, seed=None, agent_names=['Truthful', 'Truthful', 'Truthful']):
        self.loglevel = loglevel
        self.mechanism = mechanism
        self.num_rounds = num_rounds
        self.min_val = min_val
        self.max_val = max_val
        self.budget = budget
        self.max_perms = max_perms
        self.iters = iters
        self.seed = seed
        self.agent_names = agent_names

ParamsDefault = Params(loglevel='info', mechanism='gsp', num_rounds=48, min_val=25, max_val=175, budget=500000, max_perms=120, iters=1, seed=None, agent_names=['Truthful', 'Truthful', 'Truthful'])

def runParamExplore(param_ranges):
    
    output = defaultdict(dict)

    for index, params in enumerate(itertools.product(param_ranges['loglevel'], param_ranges['mechanism'], param_ranges['num_rounds'], param_ranges['min_val'], param_ranges['max_val'], param_ranges['budget'], param_ranges['max_perms'], param_ranges['iters'], param_ranges['seed'], param_ranges['agent_names'])):
        ParamsIn = Params(*params)
        print("keys", param_ranges.keys())
        test_dict = {list(param_ranges.keys())[i] : params[i] for i in range(len(params))}
        print("TEST", test_dict)
        output[index] = {'Parameters': test_dict, 'Results': tosim.main(ParamsIn)}
        print("OUTPUT", output)

    import json
    outputf = json.dumps(output, sort_keys=True, indent=2)
    print(outputf)

    with open('Output.txt', 'w') as outfile:
        outfile.write(outputf)
        
runParamExplore(test_param_ranges)