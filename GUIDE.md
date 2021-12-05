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
5. You can create or change Agent types in agents.py. 
6. To visualize your data, run the visualizer dashboard:
```
streamlit run visualizer.py
```
7. Remember to update imports when necessary.
