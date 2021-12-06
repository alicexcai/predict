# Prediction Market

## Directory Structure

```
/predict
├── LICENSE
├── README.md
├── archive - a bunch of backups and scrapped code
├── sim_mvp
│   └── sim_mvp.py - very basic simulation
└── simulation
    ├── assets - images for documentation
    ├── components
    │   ├── __init__.py
    │   ├── agent.py - agent class
    │   ├── history.py - history class
    │   ├── params.py - parameter config class
    │   └── stats.py - stats class
    ├── docs.md
    └── market.py - main simulation file
```

## Features

## Agent Types

Four different base agent types were implemented, with two different time-weighting purchase strategies for each agent type.

Time-Weighting Strategies
* "Steady Better" - calculates purchase based on linear time weighting - multiply purchases by round number / total number of rounds
* "Wait 'n See" - calculates purchase based on an inverse time weighting - multiply purchases by 1 / number of rounds remaining

Base agent types:
* Myopic Agent
    * Calculates belief based on current score signal - outcome score / total score sum
    * Calculates purchase based on different time-weighting strategies
        * an inverse time weighting - multiply purchases by 1 / number of rounds remaining
* SuperSmart Agent
    * Runs linear regression on history of scores to project predicted end score for both teams
    * Calculates belief based on weighted average of current and predicted end scores
    * Calculates purchase based on different time-weighting strategies
* Superfan Agent
    * Biased toward a particular team, multiplies belief in their chosen team by a weight randomly selected from a skewed normal distribution
    * Calculates purchase based on different time-weighting strategies
* ZeroInt Agent
    * Calculates belief based on random selection from ~[0,1] for outcomes
    * Calculates purchase based on different time-weighting strategies

## Implementation Details

Market Methods:
* Cost - calculates the current cost in the market
* Probabilities - calculates the current outcome probabilities based on the current market shares
* CostOfTrans - calculates the cost of making a particular transaction, comprising { outcome : requested # of shares, ... }
* process_data - transforms timestamps-score pairs into round-based data signals for agents
* run_round - runs one round of the prediction market, sending score signals to agents, collecting and processing requested purchases, updating balances, updating cost, probabilities, and other data

Agent Attributes:
* self.id - an id by which agents are indexed
* self.name - an alias for the agent
* self.balance - available budget to trade using
* self.team (for superfans) - team of choice

Agent Methods:
* __init__ - instantiate an agent
* get_history - get agent purchase history
* purchase - calculate purchase based on incoming signal
* __repr__ - print attributes of agent

## Design of Experiment
A design of experiment abstraction layer was implemented to automate parameter space exploration for different simulation parameters. This script works with **any function**, and can be used by others in the future to quickly conduct parameter exploration and manage outputted data. The doe.py script works as follows:
* Users input a list of parameters, including the parameter space they want to explore as well as the parameters they want to hold constant for an experiment
* For functions with more complex outputs such as simulations, users input which outputs they consider to be their primary results and full results
* The script creates a design of experiment based on the desired DOE model (full factorial, fractional factorial, etc.)
* The script creates a sqlite database with a main experiment table, where primary results and corresponding parameters are stored.
* The script outputs full run data (for each set of tested parameters) in a separate table autolabeled with parameter details.

## External Libraries and Dependencies
External libraries and frameworks were used to help implement and analyze the simulation.

## Parameters

**Notes on the liquidity parameter:**
For small markets where there is likely to be less trading activity, a smaller b value is typically desirable. This will allow the prices (and corresponding probabilities) to change relatively easily to match real world probabilities. If you use a large b value for a small market, prices can get out of line, since traders may not have enough currency to move the price to match the underlying real-world probabilities. For large markets with a large number of traders, the opposite is typically true -- a large value of b tends to be preferable.

## References
1. [Microsoft - Introduction to Prediction Markets](https://docs.microsoft.com/en-us/archive/msdn-magazine/2016/june/test-run-introduction-to-prediction-markets#the-four-key-prediction-market-equations)
2. [Cultivate Labs - How does the Logarithmic Market Scoring Rule (LMSR) work?](https://www.cultivatelabs.com/prediction-markets-guide/how-does-logarithmic-market-scoring-rule-lmsr-work)
