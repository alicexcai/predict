from .agent import Agent

# Meta-parameters describing the parameters
class MetaParams:

    def __init__(self, params_tested, params_const, results_primary, results_full):
        self.params_tested = params_tested
        self.params_const = params_const
        self.results_primary = results_primary
        self.results_full = results_full  # full list of outputs

# Parameters for a single run of the experiment
class Params:
    def __init__(self, params_all):
        for param in params_all:
            self.__dict__[param] = params_all[param]