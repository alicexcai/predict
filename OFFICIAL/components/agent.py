import random
import math
from scipy.optimize import fsolve
from scipy.stats import skewnorm
from collections import defaultdict
from sklearn.linear_model import LinearRegression

class Agent:
    
    def __init__(self, id, name, balance):
        self.id = id
        self.name = name  # alias
        self.balance = balance
        self.type = 'default'
        
    # agent-centric history
    def get_history(self, history):
        agent_history = { round : history.p_shares[self.id] for round in history.rounds }
        return agent_history
    
    def purchase(self, mechanism, liquidity, outcomes, history, round_num, shares, probabilities, cost, signal, num_rounds):

        belief = { outcome : 1 for outcome in outcomes }
        purchase = belief
        return purchase, belief
    
    def __repr__(self):
        return "{class_name}({attributes})".format(class_name = type(self).__name__, attributes = self.__dict__)

class Basic(Agent):
    
    def __init__(self, id, name, balance):
        super().__init__(id, name, balance)
        self.type = 'basic'

    def purchase(self, mechanism, liquidity, outcomes, history, round_num, shares, probabilities, cost, signal, num_rounds):
        
        # Trade until probabilities = belief
        purchase = {}
        def calculate_shares(belief):
            for outcome in outcomes:
                if belief[outcome] > probabilities[round_num-1][outcome]:
                    if mechanism == 'logarithmic':
                        purchase[outcome] = math.log((sum([math.exp(shares[round_num-1][outcome] / liquidity) for outcome in outcomes]) * belief[outcome])/(1-belief[outcome]))   
                    elif mechanism == 'quadratic':
                        purchase[outcome] = math.sqrt((sum([math.exp(shares[round_num-1][outcome] / liquidity) for outcome in outcomes]) * belief[outcome])/(1-belief[outcome]))
                else:
                    purchase[outcome] = 0
            return purchase
        
        belief = { outcome : (signal.iloc[round_num-1][outcome] / sum([signal.iloc[round_num-1][outcome] for outcome in outcomes])) for outcome in outcomes }
        belief_final = { outcome : (belief[outcome] + 0.01) / (1 + 0.01 * len(outcomes)) for outcome in outcomes }
        purchase = calculate_shares(belief_final)
        
        def calculate_weighted_purchase(purchase, round_num):
            weighted_purchase = { outcome : purchase[outcome] * 1 / (num_rounds + 1 - round_num) for outcome in outcomes }
            return weighted_purchase
        
        final_purchase = calculate_weighted_purchase(purchase, round_num)
        
        return final_purchase, belief
    
        
class ZeroInt(Agent):
    def __init__(self, id, name, balance):
        super().__init__(id, name, balance)
        self.type = 'zero_intelligence'
        
    def purchase(self, mechanism, liquidity, outcomes, history, round_num, shares, probabilities, cost, signal, num_rounds):
        belief = { outcome : random.random() * self.balance for outcome in outcomes }
        purchase = belief
        return purchase, belief
    
class Superfan(Agent):
    def __init__(self, id, name, balance, team):
        super().__init__(id, name, balance)
        self.type = 'superfan'
        self.team = team
        
    def purchase(self, mechanism, liquidity, outcomes, history, round_num, shares, probabilities, cost, signal, num_rounds):
        lean_less_r = float(skewnorm.rvs(1000, loc=0, scale = 0.25, size=1))
        lean_less = lean_less_r if lean_less_r >= 0 and lean_less_r <= 1 else 0 if lean_less_r < 0 else 1

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
        
        belief = { outcome : (signal.iloc[round_num-1][outcome] / sum([signal.iloc[round_num-1][outcome] for outcome in outcomes])) for outcome in outcomes }
        belief_new = { outcome : lean_less * belief[outcome] for outcome in outcomes }
        belief_new[self.team] = 1 - lean_less * belief[self.team]
        belief_final = { outcome : (belief[outcome] + 0.01) / (1 + 0.01 * len(outcomes)) for outcome in outcomes }
        purchase = calculate_shares(belief_final)
        print("PRUCAHSE", purchase)
        
        def calculate_weighted_purchase(purchase, round_num):
            print("NUM ROUNDS - ROUND NUM", num_rounds, round_num)
            weighted_purchase = { outcome : purchase[outcome] * 1 / (num_rounds + 1 - round_num) for outcome in outcomes }
            print("WEIGHTED PURCHASE", weighted_purchase)
            return weighted_purchase
        
        final_purchase = calculate_weighted_purchase(purchase, round_num)
        
        return final_purchase, belief

# Nerd1 performs linear regression on the score history, takes the weighted average of the current and predicted score, and does 1/(60-x).
class Nerd1(Agent):
    def __init__(self, id, name, balance):
        super().__init__(id, name, balance)
        self.type = 'nerd1'
        
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
        
        print("BELIEF PRE", belief)
        belief = { outcome : (belief[outcome] + 0.01) / (1 + 0.01 * len(outcomes)) for outcome in outcomes }
        # belief = { outcome : (belief_pre[outcome] + probabilities[outcome]) / 2 for outcome in outcomes }
        print("BELIEF", belief)

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
        
        return final_purchase, belief

# Nerd2 performs linear regression on the score history, takes the weighted average of the current and predicted score, and does x/60.
class Nerd2(Agent):
    def __init__(self, id, name, balance):
        super().__init__(id, name, balance)
        self.type = 'nerd2'
        
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
        
        belief = { outcome : (belief[outcome] + 0.01) / (1 + 0.01 * len(outcomes)) for outcome in outcomes }

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
        
        purchase = calculate_shares(belief)
        
        def calculate_weighted_purchase(purchase, round_num):
            weighted_purchase = { outcome : purchase[outcome] * round_num / (num_rounds) for outcome in outcomes }
            return weighted_purchase
        
        final_purchase = calculate_weighted_purchase(purchase, round_num)
        
        # if round_num == 60:
        #     plt.scatter(X, Y)
        #     plt.plot(X, Y_pred, color='red')
        #     plt.show()
        
        return final_purchase, belief

# Nerd3 just looks at the current score as its prediction and does 1/(60-x)
class Nerd3(Agent):
    def __init__(self, id, name, balance):
        super().__init__(id, name, balance)
        self.type = 'nerd3'
        
    def purchase(self, mechanism, liquidity, outcomes, history, round_num, shares, probabilities, cost, signal, num_rounds):
        
        weights = { 'projected': 0.5, 'current': 0.5}
        def calculate_predicted_probabilities (signal, weights):
            prediction = { outcome : (weights['current'] * signal.iloc[round_num-1][outcome] ) / sum([(weights['current'] * signal.iloc[round_num-1][outcome] ) for outcome in outcomes]) for outcome in outcomes}
            return prediction
        
        belief = calculate_predicted_probabilities(signal, weights)
        belief = { outcome : (belief[outcome] + 0.01) / (1 + 0.01 * len(outcomes)) for outcome in outcomes }

        purchase = {}
        def calculate_shares(belief):
            for outcome in outcomes:
                if belief[outcome] > probabilities[round_num-1][outcome]:
                    if mechanism == 'logarithmic':
                        purchase[outcome] = math.log((sum([math.exp(shares[round_num-1][outcome] / liquidity) for outcome in outcomes]) * belief[outcome])/(1-belief[outcome]))   
                    elif mechanism == 'quadratic':
                        purchase[outcome] = math.sqrt((sum([math.exp(shares[round_num-1][outcome] / liquidity) for outcome in outcomes]) * belief[outcome])/(1-belief[outcome]))
                else:
                    purchase[outcome] = 0
            return purchase
        
        purchase = calculate_shares(belief)
        
        def calculate_weighted_purchase(purchase, round_num):
            weighted_purchase = { outcome : purchase[outcome] * 1 / (num_rounds + 1 - round_num) for outcome in outcomes }
            return weighted_purchase
        
        final_purchase = calculate_weighted_purchase(purchase, round_num)

        return final_purchase, belief

# Nerd4 just looks at the current score as its prediction and does x/60
class Nerd4(Agent):
    def __init__(self, id, name, balance):
        super().__init__(id, name, balance)
        self.type = 'nerd4'
        
    def purchase(self, mechanism, liquidity, outcomes, history, round_num, shares, probabilities, cost, signal, num_rounds):
        
        weights = { 'projected': 0.5, 'current': 0.5}
        def calculate_predicted_probabilities (signal, weights):
            prediction = { outcome : (weights['current'] * signal.iloc[round_num-1][outcome] ) / sum([(weights['current'] * signal.iloc[round_num-1][outcome] ) for outcome in outcomes]) for outcome in outcomes}
            return prediction
        
        belief = calculate_predicted_probabilities(signal, weights)
        belief = { outcome : (belief[outcome] + 0.01) / (1 + 0.01 * len(outcomes)) for outcome in outcomes }

        purchase = {}
        def calculate_shares(belief):
            for outcome in outcomes:
                if belief[outcome] > probabilities[round_num-1][outcome]:
                    if mechanism == 'logarithmic':
                        purchase[outcome] = math.log((sum([math.exp(shares[round_num-1][outcome] / liquidity) for outcome in outcomes]) * belief[outcome])/(1-belief[outcome]))   
                    elif mechanism == 'quadratic':
                        purchase[outcome] = math.sqrt((sum([math.exp(shares[round_num-1][outcome] / liquidity) for outcome in outcomes]) * belief[outcome])/(1-belief[outcome]))
                else:
                    purchase[outcome] = 0
            return purchase
        
        purchase = calculate_shares(belief)
        
        def calculate_weighted_purchase(purchase, round_num):
            weighted_purchase = { outcome : purchase[outcome] * round_num / (num_rounds) for outcome in outcomes }
            return weighted_purchase
        
        final_purchase = calculate_weighted_purchase(purchase, round_num)

        return final_purchase, belief
    
    
# Nerd5 performs linear regression on the score history, considers only the current slope, and does 1/(60-x).
class Nerd5(Agent):
    def __init__(self, id, name, balance):
        super().__init__(id, name, balance)
        self.type = 'nerd1'
        
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
        
        print("BELIEF PRE", belief)
        belief = { outcome : (belief[outcome] + 0.01) / (1 + 0.01 * len(outcomes)) for outcome in outcomes }
        # belief = { outcome : (belief_pre[outcome] + probabilities[outcome]) / 2 for outcome in outcomes }
        print("BELIEF", belief)

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
        
        return final_purchase, belief

# Nerd6 performs linear regression on the score history, considers only the current slope, and does x/60.
class Nerd6(Agent):
    def __init__(self, id, name, balance):
        super().__init__(id, name, balance)
        self.type = 'nerd2'
        
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
        
        belief = { outcome : (belief[outcome] + 0.01) / (1 + 0.01 * len(outcomes)) for outcome in outcomes }

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
        
        purchase = calculate_shares(belief)
        
        def calculate_weighted_purchase(purchase, round_num):
            weighted_purchase = { outcome : purchase[outcome] * round_num / (num_rounds) for outcome in outcomes }
            return weighted_purchase
        
        final_purchase = calculate_weighted_purchase(purchase, round_num)
        
        # if round_num == 60:
        #     plt.scatter(X, Y)
        #     plt.plot(X, Y_pred, color='red')
        #     plt.show()
        
        return final_purchase, belief
    
# Nerd5 just looks at the current slope as its prediction and does x/60
class Nerd5(Agent):
    def __init__(self, id, name, balance):
        super().__init__(id, name, balance)
        self.type = 'zero_intelligence'
        
    def purchase(self, mechanism, liquidity, outcomes, history, round_num, shares, probabilities, cost, signal, num_rounds):
        
        # print("SIGNAL", signal)
        print("PROBABILITIES", probabilities )
        linear_regression_data = defaultdict()
        slopes = defaultdict()
        for outcome in outcomes:
            X = signal['time_remaining'].values.reshape(-1, 1)  # values converts it into a numpy array
            Y = signal[outcome].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
            linear_regressor = LinearRegression()  # create object for the class
            model = linear_regressor.fit(X, Y)  # perform linear regression
            Y_pred = linear_regressor.predict(X)  # make predictions
            linear_regression_data[outcome] = {'intercept': model.intercept_, 'slope': model.coef_, 'confidence': model.score(X, Y)}
            print("ERROR", signal.iloc[round_num-1][outcome], float(model.coef_), signal.iloc[round_num-1]['time_remaining'])
            slopes[outcome] = float(model.coef_)
        print(linear_regression_data)
        
        def calculate_predicted_probabilities (slopes):
            prediction = { outcome : slopes[outcome] / sum([slopes[outcome] for outcome in outcomes]) for outcome in outcomes }
            return prediction
        
        belief = calculate_predicted_probabilities(slopes)
        belief = { outcome : (belief[outcome] + 0.01) / (1 + 0.01 * len(outcomes)) for outcome in outcomes }

        purchase = {}
        def calculate_shares(belief):
            for outcome in outcomes:
                if belief[outcome] > probabilities[round_num-1][outcome]:
                    if mechanism == 'logarithmic':
                        purchase[outcome] = math.log((sum([math.exp(shares[round_num-1][outcome] / liquidity) for outcome in outcomes]) * belief[outcome])/(1-belief[outcome]))   
                    elif mechanism == 'quadratic':
                        purchase[outcome] = math.sqrt((sum([math.exp(shares[round_num-1][outcome] / liquidity) for outcome in outcomes]) * belief[outcome])/(1-belief[outcome]))
                else:
                    purchase[outcome] = 0
            return purchase
        
        purchase = calculate_shares(belief)
        
        def calculate_weighted_purchase(purchase, round_num):
            weighted_purchase = { outcome : purchase[outcome] * 1 / (num_rounds + 1 - round_num) for outcome in outcomes }
            return weighted_purchase
        
        final_purchase = calculate_weighted_purchase(purchase, round_num)
        
        # if round_num == 60:
        #     plt.scatter(X, Y)
        #     plt.plot(X, Y_pred, color='red')
        #     plt.show()
        
        return final_purchase, belief

# Nerd6 just looks at the current slope as its prediction and does x/60
class Nerd6(Agent):
    def __init__(self, id, name, balance):
        super().__init__(id, name, balance)
        self.type = 'zero_intelligence'
        
    def purchase(self, mechanism, liquidity, outcomes, history, round_num, shares, probabilities, cost, signal, num_rounds):
        
        # print("SIGNAL", signal)
        print("PROBABILITIES", probabilities )
        linear_regression_data = defaultdict()
        slopes = defaultdict()
        for outcome in outcomes:
            X = signal['time_remaining'].values.reshape(-1, 1)  # values converts it into a numpy array
            Y = signal[outcome].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
            linear_regressor = LinearRegression()  # create object for the class
            model = linear_regressor.fit(X, Y)  # perform linear regression
            Y_pred = linear_regressor.predict(X)  # make predictions
            linear_regression_data[outcome] = {'intercept': model.intercept_, 'slope': model.coef_, 'confidence': model.score(X, Y)}
            print("ERROR", signal.iloc[round_num-1][outcome], float(model.coef_), signal.iloc[round_num-1]['time_remaining'])
            slopes[outcome] = float(model.coef_)
        print(linear_regression_data)
        
        def calculate_predicted_probabilities (slopes):
            prediction = { outcome : slopes[outcome] / sum([slopes[outcome] for outcome in outcomes]) for outcome in outcomes }
            return prediction
        
        belief = calculate_predicted_probabilities(slopes)
        belief = { outcome : (belief[outcome] + 0.01) / (1 + 0.01 * len(outcomes)) for outcome in outcomes }

        purchase = {}
        def calculate_shares(belief):
            for outcome in outcomes:
                if belief[outcome] > probabilities[round_num-1][outcome]:
                    if mechanism == 'logarithmic':
                        purchase[outcome] = math.log((sum([math.exp(shares[round_num-1][outcome] / liquidity) for outcome in outcomes]) * belief[outcome])/(1-belief[outcome]))   
                    elif mechanism == 'quadratic':
                        purchase[outcome] = math.sqrt((sum([math.exp(shares[round_num-1][outcome] / liquidity) for outcome in outcomes]) * belief[outcome])/(1-belief[outcome]))
                else:
                    purchase[outcome] = 0
            return purchase
        
        purchase = calculate_shares(belief)
        
        def calculate_weighted_purchase(purchase, round_num):
            weighted_purchase = { outcome : purchase[outcome] * round_num / (num_rounds) for outcome in outcomes }
            return weighted_purchase
        
        final_purchase = calculate_weighted_purchase(purchase, round_num)
        
        # if round_num == 60:
        #     plt.scatter(X, Y)
        #     plt.plot(X, Y_pred, color='red')
        #     plt.show()
        
        return final_purchase, belief