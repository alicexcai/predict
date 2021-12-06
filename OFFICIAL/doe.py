from collections import defaultdict
import itertools
import pandas as pd
import market as tosim
from components.params import MetaParams, Params
from components.agent import Agent
# from gui import *
from doepy import build
import sqlite3

experiment_name = input("Enter Experiment Name: ")

db = sqlite3.connect("%s.sqlite"%experiment_name)
cursor = db.cursor()

# Static for single experiment but combinatorial runs - pass in params_tested, params_const, metaparams
params_tested = build.full_fact(
    {'liquidity': [100.0],
    'num_rounds': [60.0]}
)
params_const = {
    'outcomes': ['Harvard', 'Yale'],
    # 'agents_list': ['Nerd1(1, \'first\', 1000)', 'Nerd2(2, \'second\', 1000)'],

    # 'agents_list': ['Nerd3(1, \'first\', 1000)', 'Nerd4(2, \'second\', 1000)'],
    # 'agents_list': ['Nerd1(1, \'first\', 1000)', 'Nerd2(2, \'second\', 1000)', 'Superfan(3, \'third\', 1000, \'Harvard\')'],
    'agents_list': ['Nerd3(1, \'first\', 1000)', 'Nerd4(2, \'second\', 1000)', 'Superfan(3, \'third\', 1000, \'Harvard\')'],

    'mechanism': 'logarithmic',
    'i_shares': {'Harvard': 100.0, 'Yale': 100.0 },
                }
meta_params = MetaParams(
    params_tested=['liquidity', 'num_rounds'],
    params_const=['outcomes', 'agents_list', 'mechanism', 'i_shares'],
    results_primary=['cost', 'probability_Harvard', 'probability_Yale', 'shares_Harvard', 'shares_Yale'],
    results_full=['cost', 'probabilities', 'shares', 'p_shares', 'total_p_shares', 'agent_beliefs', 'payments']
)

def doe(params_tested, params_const, meta_params):
    
    experiment_data = pd.DataFrame(columns=meta_params.params_const + meta_params.params_tested + meta_params.results_primary + ['agent_payoffs'])
    
    params = list()
    for i in range(len(params_tested)):
        params_all = params_const
        params_tested_dict = params_tested.iloc[i].to_dict()
        
        for param in params_tested_dict.keys():
            params_all[param] = params_tested_dict[param]
        
        run_id = i
        print("\n\n============= Run %s =============\n\n"%run_id)
        params = Params(params_all)
        
        # write results primary to sqlite database
        results_full, results_primary, agent_payoffs = tosim.sim(params, meta_params)
        
        # print("\n\n============= Results Full =============\n\n", results_full)
        
        for result in meta_params.results_primary:
            experiment_data.at[i, result] = results_primary[result]
        
        for param in meta_params.params_tested:
            experiment_data.at[i, param] = params_tested.iloc[i][param]
            
        for param_const in meta_params.params_const:
            experiment_data.at[i, param_const] = params_const[param_const]
            
        experiment_data.at[i, 'agent_payoffs'] = agent_payoffs
            
        results_full_str = results_full.copy()
        for col in list(results_full.columns.values):
            results_full_str[col] = results_full[col].astype(str) if type(results_full[col]) != int or str else results_full[col]
            
        params_tested_str = ''.join(['l', str(int(params_all['liquidity'])), '_r', str(int(params_all['num_rounds']))])
        print("STR\n\n\n\n\n\n", params_tested_str)
        
        # print([str(params_tested[param]) for param in params_tested])
        results_full.to_csv('%sRun%s_data_%s.csv'%(experiment_name,run_id, params_tested_str))    
        results_full_str.to_sql('run_data', con=db, if_exists='replace')
        
        cursor.execute("""DROP TABLE IF EXISTS run%s_data"""%run_id)
        cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS run%s_data as 
        select * from run_data
        """%run_id)
        
        # return experiment_data
    
    # print("\n\n============= Experiment Data =============\n\n", experiment_data)
    
    experiment_data_str = experiment_data.copy()
    for col in list(experiment_data.columns.values):
        experiment_data_str[col] = experiment_data[col].astype(str) if type(experiment_data[col]) != int or str else experiment_data[col]
    print(experiment_data_str)
    print(experiment_data_str.dtypes)
        
    print("\n\n\nERROR\n\n\n", experiment_data)
    experiment_data.to_csv('%s.csv'%experiment_name) 
    experiment_data_str.to_sql('experiment_data', con=db, if_exists='replace')
    cursor.execute(
    """
    CREATE TABLE %s_data as 
    select * from experiment_data
    """%experiment_name)

    cursor.execute("""DROP TABLE IF EXISTS %s_data"""%experiment_name)
    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS %s_data as 
    select * from experiment_data
    """%experiment_name)
    
    # print("\n\n================= ULTIMATE TEST ================\n\n")
    # print(cursor.execute("SELECT * FROM %s_data"%experiment_name).fetchall())
    
    # cleanup
    cursor.execute("""DROP TABLE IF EXISTS experiment_data""")
    cursor.execute("""DROP TABLE IF EXISTS run_data""")

doe(params_tested, params_const, meta_params)