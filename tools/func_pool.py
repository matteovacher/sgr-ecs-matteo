import numpy as np 


class FunctionPool :

    def __init__(self, config ) :
        self.config = config 
        self.pool = self._create_pool()
        self.list_pool = [func for _, func in self.pool.items()]

    def _create_pool(self) :
        pool = {}
        if "gaussian" in self.config.function_pool :
            pool["gaussian"] = lambda x : np.exp(- x**2)
        if "sin" in self.config.function_pool :
            pool["sin"] = lambda x : np.sin(x)
        if "abs" in self.config.function_pool :
            pool["abs"] = lambda x : abs(x)
        if "tanh" in self.config.function_pool :
            pool["tanh"] = lambda x : np.tanh(x)
        if "minus gaussian" in self.config.function_pool :
            pool["minus gaussian"] = lambda x : -np.exp(- x**2)
        return pool
