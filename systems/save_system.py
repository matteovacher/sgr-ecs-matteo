

class SaveSystem :
    def __init__(self, config, results_manager) :
        self.config = config 
        self.results_manager = results_manager
        

    def process(self, registry ) :
        keys_ind = registry.get_all_id_with_tosave()
        keys_stat = registry.get_all_id_with_statistic()
        other_ids = [id for id in registry.get_all_id_with_genome() if id not in keys_ind and id not in keys_stat]
        for id in other_ids : 
            registry.clear_ind_from_registry(id)
        if self.results_manager.save :
            self.results_manager.save_results(registry, self.config)

        

