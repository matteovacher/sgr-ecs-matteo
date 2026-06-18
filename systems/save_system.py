

class SaveSystem :
    def __init__(self, config, results_manager) :
        self.config = config 
        self.results_manager = results_manager
        

    def process(self, registry ) :

        self.results_manager.save_results(registry, self.config)


class BothSaveSystem :
    def __init__(self, config, results_manager, type_genome) :
        self.config = config 
        self.results_manager = results_manager
        self.type_genome = type_genome

    def process(self, registry ) :

        self.results_manager.save_both_results(registry, self.config, self.type_genome)


        

