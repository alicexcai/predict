import random

import math
from scipy.optimize import fsolve
from scipy.stats import skewnorm
from collections import defaultdict
from .agent import Agent


import numpy as np
import matplotlib.pyplot as plt  # To visualize
import pandas as pd  # To read data
from sklearn.linear_model import LinearRegression


"""
Start with Nerd class:
- Regression to predict future value (linear, quadratic, etc.)
- Base signal: history of scores, time remaining [history of shares]
- Time weighting: 1/x
- Budget awareness: budget-remaining/rounds-remaining vs budget/round

ML agent?
other-aware agent?
late bidder - David Parkes

"""


class Nerd(Agent):
    def __init__(self, id, name, balance):
        super().__init__(id, name, balance)
        self.type = 'zero_intelligence'
        
    def purchase(self, mechanism, liquidity, outcomes, history, round_num, shares, probabilities, cost, signal, num_rounds):
        
        # print("SIGNAL", signal)
        print("PROBABILITIES", probabilities )
        linear_regression_data = defaultdict()
        projected_scores = defaultdict()
        for outcome in outcomes:
            X = signal['time_remaining'].values.reshape(-1, 1)  # values converts it into a numpy array
            Y = signal[outcome].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
            linear_regressor = LinearRegression()  # create object for the class
            model = linear_regressor.fit(X, Y)  # perform linear regression
            Y_pred = linear_regressor.predict(X)  # make predictions
            linear_regression_data[outcome] = {'intercept': model.intercept_, 'slope': model.coef_, 'confidence': model.score(X, Y)}
            print("ERROR", signal.iloc[round_num-1][outcome], float(model.coef_), signal.iloc[round_num-1]['time_remaining'])
            projected_scores[outcome] = signal.iloc[round_num-1][outcome] - float(model.coef_) * signal.iloc[round_num-1]['time_remaining']
        print(linear_regression_data)
        
        weights = { 'projected': 0.5, 'current': 0.5}
        def calculate_predicted_probabilities (projected_scores, signal, weights):
            prediction = { outcome : (weights['projected'] * projected_scores[outcome] + weights['current'] * signal.iloc[round_num-1][outcome] / 2) / sum([(weights['projected'] * projected_scores[outcome] + weights['current'] * signal.iloc[round_num-1][outcome] / 2) for outcome in outcomes]) for outcome in outcomes}
            return prediction
        
        belief = calculate_predicted_probabilities(projected_scores, signal, weights)

        purchase = {}
        def calculate_shares(belief):
            for outcome in outcomes:
                if belief[outcome] > probabilities[round_num-1][outcome]:
                    if mechanism == 'logarithmic':
                        purchase[outcome] = math.log((sum([math.exp(shares[round_num-1][outcome] / liquidity) for outcome in outcomes]) * belief[outcome])/(1-belief[outcome]))   
                    # not sure if this is correct? pulled from https://slidetodoc.com/a-utility-framework-for-boundedloss-market-makers-yiling/
                    elif mechanism == 'quadratic':
                        purchase[outcome] = math.sqrt((sum([math.exp(shares[round_num-1][outcome] / liquidity) for outcome in outcomes]) * belief[outcome])/(1-belief[outcome]))
                else:
                    purchase[outcome] = 0
            return purchase
        
        # print("BELIEF", belief)
        purchase = calculate_shares(belief)
        print("PRUCAHSE", purchase)
        
        def calculate_weighted_purchase(purchase, round_num):
            print("NUM ROUNDS - ROUND NUM", num_rounds, round_num)
            weighted_purchase = { outcome : purchase[outcome] * 1 / (num_rounds + 1 - round_num) for outcome in outcomes }
            print("WEIGHTED PURCHASE", weighted_purchase)
            return weighted_purchase
        
        final_purchase = calculate_weighted_purchase(purchase, round_num)
        
        # if round_num == 60:
        #     plt.scatter(X, Y)
        #     plt.plot(X, Y_pred, color='red')
        #     plt.show()
        
        return final_purchase
    