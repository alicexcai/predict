from collections import defaultdict
import itertools
import pandas as pd
import market as tosim
from components.params import MetaParams, Params
from components.agent import Agent, Basic, ZeroInt, Superfan, Dummy
# from gui import *
from doepy import build
import sqlite3

# Static for single experiment but combinatorial runs - pass in params_tested, params_const, metaparams
params_tested = build.full_fact(
    {'liquidity': [100.0, 200.0],
    'num_rounds': [60.0, 70.0]}
)
params_const = {
    'outcomes': ['Harvard', 'Yale'],
    'agents_list': [Agent(1, 'first', 1000), Agent(id=2, name='second', balance=1000), Agent(3, 'third', 1000)],
    'mechanism': 'logarithmic',
    'i_shares': {'Harvard': 0.0, 'Yale': 0.0 },
                }
meta_params = MetaParams(
    params_tested=['liquidity', 'num_rounds'],
    params_const=['outcomes', 'agents_list', 'mechanism', 'i_shares'],
    results_primary=['cost', 'probabilities', 'shares'],
    results_full=['cost', 'probabilities', 'shares', 'p_shares', 'payments']
)

def doe(params_tested, params_const, meta_params):
    
    experiment_data = pd.DataFrame(columns=meta_params.params_const + meta_params.params_tested + meta_params.results_primary + ['results_full'])
    
    params = list()
    for i in range(len(params_tested)):
        params_all = params_const
        params_tested_dict = params_tested.iloc[i].to_dict()
        
        for param in params_tested_dict.keys():
            params_all[param] = params_tested_dict[param]
        
        # print('PARAMS ALL', params_all)
        
        run_id = i
        # print("RUN ID", run_id)
        params = Params(params_all)
        
        # write results primary to sqlite database
        results_full, results_primary = tosim.sim(params, meta_params)
        
        # print("\n\n============= Results Full =============\n\n", results_full)
        
        for result in meta_params.results_primary:
            experiment_data.at[i, result] = results_primary[result]
        
        for param in meta_params.params_tested:
            experiment_data.at[i, param] = params_tested.iloc[i][param]
            
        for param_const in meta_params.params_const:
            experiment_data.at[i, param_const] = params_const[param_const]
        
        results_full.to_csv('Run_%s.csv'%run_id)
        
        # return experiment_data
    
    # print("\n\n============= Experiment Data =============\n\n", experiment_data)
    experiment_data.to_csv('Experiment.csv')  
    

doe(params_tested, params_const, meta_params)