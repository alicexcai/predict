# Prediction Market

## Directory Structure
```
OFFICIAL
├── components
│   ├── __init__.py
│   ├── agent.py
│   ├── history.py
│   ├── params.py
│   └── ripbudget.py
├── data - a bunch of game data
├── doe.py - RUN THIS FILE TO EXPERIMENT WITH THE SIMULATION
├── market.py - simulates market
├── requirements.txt
└── visualize
    ├── main.py - RUN THIS FILE TO LAUNCH THE DATAVIZ DASHBOARD
    ├── multipage.py
    ├── output_data - a bunch of output data
    └── pages
        ├── example_data.csv
        ├── experiment.py
        └── visualize.py
```

# Usage Guide

1. Clone this repository onto your local device.
2. cd into the OFFICIAL directory.
``` cd OFFICIAL```
3. Install the dependencies:
``` pip install -r requirements.txt ```
4. Change the parameters in doe.py as desired. Remember that you can only test out factorial designs of numerical parameters, i.e. all parameters in params_tested must be floats or ints. 
```
params_tested = build.full_fact(
    {'liquidity': [100.0, 200.0],
    'num_rounds': [60.0, 120.0]}
)
params_const = {
    'outcomes': ['Harvard', 'Yale'],
    'agents_list': ['Nerd(1, \'first\', 1000)', 'Nerd(2, \'second\', 1000)', 'Nerd(3, \'third\', 1000)'],
    'mechanism': 'logarithmic',
    'i_shares': {'Harvard': 0.0, 'Yale': 0.0 },
                }
```
5. You can change which dataset to simulate the market for in market.py by changing the data file path.
```
data = pd.read_csv('./data/data.csv')
```
6. You can create or change Agent types in agents.py. Agents should inheret from the Agent() base class.
7. To visualize your data, cd into visualize and run the visualizer dashboard:
```
cd visualize
streamlit run visualizer.py
```

## Features

### Agent Types

Four different basic agent types were implemented, with two different time-weighting purchase strategies for each agent type.

Time-Weighting Strategies
* "Steady Better" - calculates purchase based on linear time weighting - multiply purchases by round number / total number of rounds
* "Wait 'n See" - calculates purchase based on an inverse time weighting - multiply purchases by 1 / number of rounds remaining

Base agent types:
* Myopic Agent
    * Calculates belief based on current score signal - outcome score / total score sum
    * Calculates purchase based on different time-weighting strategies
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

### Implementation Details

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

## Data Visualization
Using our browser-based data visualization dashboard (visualize/main.py), users can easily graph and analyze data. Users can choose a data source directory, select the number of graphs they want to work with, and visualize a number of different datasets at once. The software automatically reads the dataset and allows users to select x and y axes for data visualization, as well as linear regression types, including Ordinary Least Squares, Rolling Moving Averages, Exponential Moving Averages, and more. Users can also view their raw data in collapsible sections of the UI. 

## References
1. [Microsoft - Introduction to Prediction Markets](https://docs.microsoft.com/en-us/archive/msdn-magazine/2016/june/test-run-introduction-to-prediction-markets#the-four-key-prediction-market-equations)
2. [Cultivate Labs - How does the Logarithmic Market Scoring Rule (LMSR) work?](https://www.cultivatelabs.com/prediction-markets-guide/how-does-logarithmic-market-scoring-rule-lmsr-work)
