# Pulled from https://docs.microsoft.com/en-us/archive/msdn-magazine/2016/june/test-run-introduction-to-prediction-markets#the-four-key-prediction-market-equations
# Translated from C to Python using Codex

import math

''' 
Simulation components:
-main simulation
-agents
-mechanisms (start with LMSR AMM, potentially do other scoring rules, CDA, call, etc.)
-UI
-Codex-generated agent code

'''

# Functions:
# Cost Function
# Cost of Transaction
# Marginal Price aka probability

# Classes:
# Agents 
# Bids
# Markets

# Meta:
# history (round)
# parameters 

# Relational Database:

def Probabilities(outstanding, liq):
    result = [0.0, 0.0]
    denom = 0.0
    for i in range(2):
        denom += math.exp(outstanding[i] / liq)
    for i in range(2):
        result[i] = math.exp(outstanding[i] / liq) / denom
    return result

def Cost(outstanding, liq):
    sum = 0.0
    for i in range(2):
        sum += math.exp(outstanding[i] / liq)
    return liq * math.log(sum)

def CostOfTrans(outstanding, idx, nShares, liq):
    after = [0, 0]
    after[:] = outstanding
    after[idx] += nShares
    return Cost(after, liq) - Cost(outstanding, liq)

def CostForOneShare(outstanding, liq):
    result = [0.0, 0.0]
    result[0] = CostOfTrans(outstanding, 0, 1, liq)
    result[1] = CostOfTrans(outstanding, 1, 1, liq)
    return result

def ShowVector3(vector, dec, pre):
    for i in range(len(vector)):
        print(pre + str(vector[i]) + " ", end="")
    print("\n")

def ShowVector(vector):
    for i in range(len(vector)):
        print(vector[i], end=" ")
    print("\n")

def main():
    print("Begin prediction market demo...")
    print("Goal is to predict winner of Harvard Yale game")
    liq = 100.0
    print("Setting liquidity parameter = " +
          str(liq))
    outstanding = [0, 0]
    print("Initial number of shares owned are:")
    ShowVector(outstanding)
    probs = Probabilities(outstanding, liq)
    print("Initial probabilities of winning:")
    ShowVector3(probs, 4, " ")
    print("=================================")
    costPerShare = CostForOneShare(outstanding, liq)
    print("Current costs for one share are: ")
    ShowVector3(costPerShare, 4, " $")
    print("Update: expert [01] buys 20 shares of team [0]")
    costTrans = CostOfTrans(outstanding, 0, 20, liq)
    print("Cost of transaction to expert was: $" +
          str(costTrans))
    outstanding = [20, 0]
    print("New number of shares owned are: ")
    ShowVector(outstanding)
    probs = Probabilities(outstanding, liq)
    print("New inferred probs of winning:")
    ShowVector3(probs, 4, " ")
    print("=================================")
    costPerShare = CostForOneShare(outstanding, liq)
    print("Current costs for one share are: ")
    ShowVector3(costPerShare, 4, " $")
    print("Update: expert [02] buys 20 shares of team [1]")
    costTrans = CostOfTrans(outstanding, 1, 20, liq)
    print("Cost of transaction to expert was: $" +
          str(costTrans))
    outstanding = [20, 20]
    print("New number of shares owned are: ")
    ShowVector(outstanding)
    probs = Probabilities(outstanding, liq)
    print("New inferred probs of winning:")
    ShowVector3(probs, 4, " ")
    print("=================================")
    costPerShare = CostForOneShare(outstanding, liq)
    print("Current costs for one share are: ")
    ShowVector3(costPerShare, 4, " $")
    print("Update: expert [03] buys 60 shares of team [0]")
    costTrans = CostOfTrans(outstanding, 0, 60, liq)
    print("Cost of transaction to expert was: $" +
          str(costTrans))
    outstanding = [80, 20]
    print("New number of shares owned are: ")
    ShowVector(outstanding)
    probs = Probabilities(outstanding, liq)
    print("New inferred probs of winning:")
    ShowVector3(probs, 4, " ")
    print("=================================")
    print("Update: Market Closed")
    print("\nEnd prediction market demo \n")

if __name__ == "__main__":
    main()