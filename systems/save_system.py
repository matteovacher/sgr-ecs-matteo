

class SaveSystem :
    def __init__(self, config, results_manager) :
        self.config = config 
        self.results_manager = results_manager
        

    def process(self, registry ) :

        self.results_manager.save_results(registry, self.config)

        

