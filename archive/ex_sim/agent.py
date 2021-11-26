#!/usr/bin/env python # omit?

from gsp import GSP
from util import argmax_index # what is this for?
import sympy
from sympy.abc import x
from market import Probabilities


class Agent():

    def __init__(self, id, name, balance):
        self.id = id
        self.name = name  # alias
        self.balance = balance
        self.type = 'default'
        
        # agent-centric history
    def get_history(self, history):
        # agent purchase history stored in a dictionary of dictionaries { round : { outcome : shares, ... }, ... } for each agent
        agent_history = { round : history.p_shares[self.id] for round in history.rounds }
        return agent_history

    def purchase(self, history, round_num, shares, signal):
        
        # signal = {'outcome': 'probability', ... }, derived from change in information * weight
        # code for purchase strategy
        
        target_shares = sympy.solve(Probabilities(x, round_num) - signal, 'x')
        # purchase = {}
        # for outcome in shares[round_num].keys():
        #     purchase[outcome] = target_shares[round_num][outcome] - shares[round_num][outcome]
        purchase = { outcome : target_shares[round_num][outcome] - shares[round_num][outcome] for outcome in shares[round_num].keys() }
        
        return purchase
    
    # Is this necessary?
    def __repr__(self):
        return "%s(id = %d, name = %d, balance = %d)" % (
            self.__class__.__name__, self.id, self.name, self.balance)
