# PREDICT

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

## Features to Implement
* agent bidding methodologies 
* signals input
* pypet DOE suite
  * stats
* Dash visualization

## Parameters

**Notes on the liquidity parameter:**
For small markets where there is likely to be less trading activity, a smaller b value is typically desirable. This will allow the prices (and corresponding probabilities) to change relatively easily to match real world probabilities. If you use a large b value for a small market, prices can get out of line, since traders may not have enough currency to move the price to match the underlying real-world probabilities. For large markets with a large number of traders, the opposite is typically true -- a large value of b tends to be preferable.

## References
1. [Microsoft - Introduction to Prediction Markets](https://docs.microsoft.com/en-us/archive/msdn-magazine/2016/june/test-run-introduction-to-prediction-markets#the-four-key-prediction-market-equations)
2. [Cultivate Labs - How does the Logarithmic Market Scoring Rule (LMSR) work?](https://www.cultivatelabs.com/prediction-markets-guide/how-does-logarithmic-market-scoring-rule-lmsr-work)

----------
## Brain Dump

* Should we use simpy? live signals of changing scores
* cellular automata scoring rule / model for prediction markets
* AI generated videos to do human subject experimentation? randomly generated simple shape / info movements?