# predict

## Decisions

### Notes on the liquidity parameter:
For small markets where there is likely to be less trading activity, a smaller b value is typically desirable. This will allow the prices (and corresponding probabilities) to change relatively easily to match real world probabilities. If you use a large b value for a small market, prices can get out of line, since traders may not have enough currency to move the price to match the underlying real-world probabilities. For large markets with a large number of traders, the opposite is typically true -- a large value of b tends to be preferable.

## References


[Microsoft - Introduction to Prediction Markets](https://docs.microsoft.com/en-us/archive/msdn-magazine/2016/june/test-run-introduction-to-prediction-markets#the-four-key-prediction-market-equations)
[Cultivate Labs - How does the Logarithmic Market Scoring Rule (LMSR) work?](https://www.cultivatelabs.com/prediction-markets-guide/how-does-logarithmic-market-scoring-rule-lmsr-work)

## Brain Dump

-cellular automata scoring rule / model for prediction markets
-