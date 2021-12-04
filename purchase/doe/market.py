from collections import defaultdict
import math
import random
import pandas as pd
import numpy as np

from components.history import History
from components.stats import Stats
from components.params import MetaParams, Params
from components.agent import Agent

def sim(params, meta_params):
    
    data = pd.read_csv('/Users/alicecai/Desktop/csecon/predict/predict/purchase/doe/data/data.csv')  
    
    # initiate
    round_num = 0
    # single set of parameters, per round
    results_full = pd.DataFrame(columns=meta_params.results_full)
    results_full['round_num'] = range(int(params.num_rounds)+1) # Is this necessary? Just use index?

    outcomes = params.outcomes
    mechanism = params.mechanism 
    liquidity = params.liquidity
    num_rounds = params.num_rounds
    
    # variable
    agents_list = params.agents_list
    shares = results_full['shares']
    shares[0] = params.i_shares  
    payments = results_full['payments']
    payments[0] = {agent.id: {outcome: 0.0 for outcome in outcomes} for agent in agents_list}
    p_shares = results_full['p_shares'] 
    p_shares[0] = {agent.id: {outcome: 0.0 for outcome in outcomes} for agent in agents_list}
    
    def Cost(shares):
        if mechanism == 'logarithmic':
            cost = liquidity * math.log(sum([math.exp(shares[outcome] / liquidity) for outcome in outcomes]))
        elif mechanism == 'quadratic':
            # is this correct?
            cost = liquidity * \
                sum([(shares[outcome] / liquidity) ** 2 for outcome in outcomes])
        return cost

    def Probabilities(shares):
        if mechanism == 'logarithmic':
            probabilities = {outcome: math.exp(shares[outcome] / liquidity) / sum(
                [math.exp(shares[outcome] / liquidity) for outcome in outcomes]) for outcome in outcomes}
        elif mechanism == 'quadratic':
            # is this correct?
            probabilities = {outcome: (shares[outcome] / liquidity) ** 2 / sum(
                [(shares[outcome] / liquidity) ** 2 for outcome in outcomes]) for outcome in outcomes}
        return probabilities

    def CostOfTrans(shares, requested_purchase):
        before_cost = Cost(shares)
        new_shares = {outcome: shares[outcome] + requested_purchase[outcome] for outcome in outcomes}
        after_cost = Cost(new_shares)
        cost_of_trans = after_cost - before_cost
        return cost_of_trans

    probabilities = results_full['probabilities']
    probabilities[0] = Probabilities(shares[0])
    cost = results_full['cost']
    cost[0] = Cost(shares[0])
    
    # do we need a function for this?
    def process_data(data, num_rounds):
        data_expanded  = pd.DataFrame(np.zeros((int(num_rounds), 3)), columns=['time_remaining', 'Harvard', 'Yale'])
        data_processed  = pd.DataFrame(np.zeros((int(num_rounds), 3)), columns=['time_remaining', 'Harvard', 'Yale'])
        time_interval = 60.0 / num_rounds
        harvard = 0
        yale = 0
        
        for row, timestamp in data.iterrows():
            timestamp_rounded = round(timestamp['time_remaining'] / time_interval) * time_interval
            data_expanded.iloc[int(timestamp_rounded)] = data.iloc[row]
            data_expanded.at[int(timestamp_rounded), 'time_remaining'] = timestamp_rounded
        data_processed = data_expanded.iloc[::-1]
        
        for row, timestamp in data_expanded.iterrows():
            harvard = data_expanded.at[row, 'Harvard'] if data_expanded.at[row, 'Harvard'] > 0 else harvard
            yale = data_expanded.at[row, 'Yale'] if data_expanded.at[row, 'Yale'] > 0 else yale
            data_processed.iloc[row] = [row, harvard, yale]
        
        data_processed = data_processed.reindex(index=data_processed.index[::-1])
        data_processed = data_processed.reset_index().T.tail(3).T
        
        return data_processed
    
    data_processed = process_data(data, num_rounds)

    # Introduce new agent mid-simulation - is this necessary?
    def init_agent(agents_list, newagent_name, newagent_balance):
        agents_list.update(
            Agent(len(agents_list)+1, newagent_name, newagent_balance))

    history = History(cost, shares, probabilities, p_shares, payments)

    # round is an arbitrary alias for a unit of time, agents can choose to trade in different round intervals, simulating trade frequency
    def run_round(shares, round_num):
        
        # example signal
        # signal = { outcome : random.random() for outcome in outcomes }
        
        signal = data_processed.iloc[0:round_num]
        
        # print('SIGNAL', signal)

        p_shares[round_num]= {}
        payments[round_num]= {}
        
        # Log purchased shares determined by agents
        for agent in agents_list:
            requested_purchase = agent.purchase(mechanism, liquidity, outcomes, history, round_num, shares, cost, signal)
            p_shares[round_num][agent.id] = requested_purchase if sum(requested_purchase.values()) <= agent.balance else {outcome: 0 for outcome in outcomes}
            # update agent balance, calculate payments based on mechanism
            
            cost_of_trans_dict = {}
            for outcome in outcomes:
                separated_shares = {out: 0.0 for out in outcomes}
                separated_shares[outcome] = shares[round_num-1][outcome]
                cost_of_trans_dict[outcome] = CostOfTrans(separated_shares, p_shares[round_num][agent.id])
            
            payments[round_num][agent.id] = cost_of_trans_dict
            agent.balance -= sum(list(payments[round_num][agent.id].values()))
            shares[round_num] = { outcome: shares[round_num-1][outcome] + p_shares[round_num][agent.id][outcome] for outcome in outcomes }
        # new cost and probabilities post-purchase
        cost[round_num] = Cost(shares[round_num])
        probabilities[round_num] = Probabilities(shares[round_num])

        '''
        Introduce round-specific actions here:
        
        e.g. introduce new agents at certain rounds:
        if round_num == 10:
            init_agent(agents_list, agent)
            
        e.g. add balance to agents at certain rounds:
        if round_num == 10:
            for agent in agents_list:
                agents_list[agent].balance += 1000
        '''
        
        # print("\n\t=== Round %d ===" % round_num)
        print("\tPurchased shares: %s" % p_shares[round_num])
        # print("\tUpdated shares: %s" % shares[round_num])
        # print("\tPayments made: %s" % payments[round_num])
        # print("\tUpdated probabilities: %s" % probabilities[round_num])
        # print("\tUpdated cost: %s\n" % cost[round_num])

    # RUN ROUNDS
    for round_num in range(1, int(params.num_rounds) + 1):
        # Consider using 240 rounds to simulate a 4 hour game with trading every 1 sec?
        run_round(shares, round_num)

    # print("\n\t=== Cumulative (%d Rounds) ===" % num_rounds)
    # print("\tPurchased Shares History: %s" % p_shares)
    # print("\tShares History: %s" % shares)
    # print("\tPayments History: %s" % payments)
    # print("\tProbabilities History: %s" % probabilities)
    # print("\tCost History: %s\n" % cost)
    
    results_primary = results_full.iloc[-1][meta_params.results_primary]
    
    return results_full, results_primary