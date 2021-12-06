from collections import defaultdict
import math
import random
import pandas as pd
import numpy as np

from components.history import History
# from components.stats import Stats
from components.params import MetaParams, Params
from components.agent import Agent, ZeroInt, Basic, Superfan, Nerd1, Nerd2, Nerd3, Nerd4, Nerd5, Nerd6

def sim(params, meta_params):
    
    data = pd.read_csv('./data/cgame_cw1.csv')  
    # winner = data['winner'].values
    # winner = data.iloc[num_rounds].idxmax(axis=1)
    
    # initiate
    round_num = 0
    # single set of parameters, per round
    results_full = pd.DataFrame(columns=meta_params.results_full)
    results_full['round_num'] = range(int(params.num_rounds)+1) # Is this necessary? Just use index?

    outcomes = params.outcomes
    mechanism = params.mechanism 
    liquidity = params.liquidity
    num_rounds = params.num_rounds
    
    winner = data.iloc[-1].idxmax()
    
    # variable
    agents_list = [eval(agent) for agent in params.agents_list]
    shares = results_full['shares']
    shares[0] = params.i_shares  
    payments = results_full['payments']
    payments[0] = {agent.id: 0 for agent in agents_list}
    p_shares = results_full['p_shares'] 
    p_shares[0] = {agent.id: {outcome: 0.0 for outcome in outcomes} for agent in agents_list}
    total_p_shares = results_full['total_p_shares'] 
    total_p_shares[0] = {agent.id: {outcome: 0.0 for outcome in outcomes} for agent in agents_list}
    agent_beliefs = results_full['agent_beliefs'] 
    agent_beliefs[0] = {agent.id: {outcome: 0.0 for outcome in outcomes} for agent in agents_list}
    
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
        time_interval = 60.0 / num_rounds
        data_test = pd.DataFrame(np.zeros((int(num_rounds), 3)), columns=['time_remaining'] + [outcome for outcome in outcomes])
        for row, row_data in data.iterrows():
            # timestamp = round(row_data['time_remaining'] / time_interval) * time_interval
            index = round(row_data['time_remaining'] / time_interval)
            data_test.iloc[index] = row_data
        data_test = data_test.reindex(index=data_test.index[::-1])
        data_test = data_test.reset_index().T.tail(3).T
        for row, row_data in data_test.iterrows():
            for outcome in outcomes:
                if row > 0:
                    if data_test.iloc[row][outcome] < data_test.iloc[row-1][outcome]:
                        data_test.iloc[row][outcome] = data_test.iloc[row-1][outcome]
            data_test.iloc[row]['time_remaining'] = 60 - row * time_interval
        return data_test
    
    data_processed = process_data(data, num_rounds)

    # Introduce new agent mid-simulation - is this necessary?
    def init_agent(agents_list, newagent_name, newagent_balance):
        agents_list.update(
            Agent(len(agents_list)+1, newagent_name, newagent_balance))

    history = History(cost, shares, probabilities, p_shares, payments)

    # round is an arbitrary alias for a unit of time, agents can choose to trade in different round intervals, simulating trade frequency
    def run_round(shares, round_num):

        signal = data_processed.iloc[0:round_num]

        p_shares[round_num]= {}
        total_p_shares[round_num] = {}
        agent_beliefs[round_num] = {}
        payments[round_num]= {}
        
        # Log purchased shares determined by agents
        shares[round_num] = { outcome: shares[round_num-1][outcome] for outcome in outcomes }
        for agent in agents_list:
            [requested_purchase, belief] = agent.purchase(mechanism, liquidity, outcomes, history, round_num, shares, probabilities, cost, signal, num_rounds)
            # implement proportional capping? Burden of checking balance feasibility lies on the agent for now.
            # new_request = { outcome : 0 if sum(list(requested_purchase.values())) == 0 else agent.balance if requested_purchase[outcome] == sum(list(requested_purchase.values())) else requested_purchase[outcome] * agent.balance / sum(list(requested_purchase.values())) for outcome in outcomes }
            # p_shares[round_num][agent.id] = requested_purchase if all( i >= 0 for i in list(requested_purchase.values())) and CostOfTrans(shares[round_num-1], requested_purchase) <= agent.balance else { outcome : 0.0 for outcome in outcomes}
            p_shares[round_num][agent.id] = requested_purchase
            total_p_shares[round_num][agent.id] = { outcome: sum(p_shares[r][agent.id][outcome] for r in range(round_num)) for outcome in outcomes }
            agent_beliefs[round_num][agent.id] = belief
            
            payments[round_num][agent.id] = CostOfTrans(shares[round_num-1], p_shares[round_num][agent.id])
            
            agent.balance -= payments[round_num][agent.id]
            for outcome in outcomes:
                shares[round_num][outcome] += p_shares[round_num][agent.id][outcome]
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
        
        print("\n\t=== Round %d ===" % round_num)
        print("\tPurchased shares: %s" % p_shares[round_num])
        print("\tTotal purchased shares: %s" % total_p_shares[round_num])
        print("\tAgent beliefs: %s" % agent_beliefs[round_num])
        print("\tUpdated shares: %s" % shares[round_num])
        print("\tPayments made: %s" % payments[round_num])
        print("\tUpdated probabilities: %s" % probabilities[round_num])
        print("\tUpdated cost: %s\n" % cost[round_num])
        
    # print("\n\t=== Results ===\n\n", results_full)

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
    
     # UNPACKING DATATYPES =====================================================================================================================
    
    results_full_unpkd = results_full.copy()
    
    shares_unpkd = results_full_unpkd["shares"].apply(pd.Series)
    shares_unpkd = shares_unpkd.add_prefix('shares_')
    results_full_unpkd = pd.concat([results_full_unpkd.drop('shares', axis=1), shares_unpkd], axis=1)  
    
    probabilities_unpkd = results_full_unpkd["probabilities"].apply(pd.Series)
    probabilities_unpkd = probabilities_unpkd.add_prefix('probability_')
    results_full_unpkd = pd.concat([results_full_unpkd.drop('probabilities', axis=1), probabilities_unpkd], axis=1)
    
    pshares_unpkd = results_full_unpkd["p_shares"].apply(pd.Series)
    pshares_unpkd = pshares_unpkd.add_prefix('purchase_agent')

    pshares_unpkd_unpkd = pshares_unpkd.copy()
    for col in pshares_unpkd.columns.values:
        newcol = pshares_unpkd[col].apply(pd.Series)
        newcol = newcol.add_prefix('%s_'%col)
        pshares_unpkd_unpkd = pd.concat([pshares_unpkd_unpkd, newcol], axis=1)
    pshares_unpkd_unpkd = pshares_unpkd_unpkd.drop(pshares_unpkd.columns.values, axis=1)
    
    results_full_unpkd = pd.concat([results_full_unpkd.drop('p_shares', axis=1), pshares_unpkd_unpkd], axis=1)
    
    
    ################################################################################################################################################
    total_pshares_unpkd = results_full_unpkd["total_p_shares"].apply(pd.Series)
    total_pshares_unpkd = total_pshares_unpkd.add_prefix('totalpurchase_agent')

    total_pshares_unpkd_unpkd = total_pshares_unpkd.copy()
    for col in total_pshares_unpkd.columns.values:
        newcol = total_pshares_unpkd[col].apply(pd.Series)
        newcol = newcol.add_prefix('%s_'%col)
        total_pshares_unpkd_unpkd = pd.concat([total_pshares_unpkd_unpkd, newcol], axis=1)
    total_pshares_unpkd_unpkd = total_pshares_unpkd_unpkd.drop(total_pshares_unpkd.columns.values, axis=1)
    
    results_full_unpkd = pd.concat([results_full_unpkd.drop('total_p_shares', axis=1), total_pshares_unpkd_unpkd], axis=1)
    
    ################################################################################################################################################
    
    agent_beliefs_unpkd = results_full_unpkd["agent_beliefs"].apply(pd.Series)
    agent_beliefs_unpkd = agent_beliefs_unpkd.add_prefix('belief_agent')

    agent_beliefs_unpkd_unpkd = agent_beliefs_unpkd.copy()
    for col in agent_beliefs_unpkd.columns.values:
        newcol = agent_beliefs_unpkd[col].apply(pd.Series)
        newcol = newcol.add_prefix('%s_'%col)
        agent_beliefs_unpkd_unpkd = pd.concat([agent_beliefs_unpkd_unpkd, newcol], axis=1)
    agent_beliefs_unpkd_unpkd = agent_beliefs_unpkd_unpkd.drop(agent_beliefs_unpkd.columns.values, axis=1)
    
    results_full_unpkd = pd.concat([results_full_unpkd.drop('agent_beliefs', axis=1), agent_beliefs_unpkd_unpkd], axis=1)
    
    ################################################################################################################################################
    
    

    payments_unpkd = results_full_unpkd["payments"].apply(pd.Series)
    payments_unpkd = payments_unpkd.add_prefix('payment_agent')
    
    results_full_unpkd = pd.concat([results_full_unpkd.drop('payments', axis=1), payments_unpkd], axis=1)
    
    results_primary = results_full_unpkd.iloc[-1][meta_params.results_primary]
    agent_payoffs = { agent.id : agent.balance + total_p_shares[num_rounds][agent.id][outcome] if outcome == winner else agent.balance for outcome in outcomes for agent in agents_list }
    
    return results_full_unpkd, results_primary, agent_payoffs