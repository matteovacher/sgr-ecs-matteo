import numpy as np

class SaveGenSystem :

    def __init__(self, config, results_manager) :
        self.config = config 
        self.results_manager = results_manager
        self.generation = 1

    def process(self, registry) :
        # forced to put it in list because it had killed the pointer and changed the size :(((((((
        keys_ind = list(registry.get_all_id_with_tosave())

        for name, component_registry in registry.__dict__.items() :
            if not component_registry :
                continue
            dict = {}
            if name == 'genome_registry' or name == 'fitness_registry' or name == 'controller_network_registry' or name == 'body_registry' or name == 'tosave_registry' or name == 'generation_registry' or name == 'age_registry' or name == 'parents_registry' or name == 'cppn_registry' :
                for key_ind in keys_ind :
                    dict[key_ind] = component_registry[key_ind]
                self.results_manager.save_generation_registry(dict, name, self.generation)
        for key_ind in keys_ind :
            gen, id = key_ind
            registry.clear_save_from_registry(gen, id)        

        self.generation += 1    


class HaploidSaveGenSystem :

    def __init__(self, config, results_manager) :
        self.config = config 
        self.results_manager = results_manager
        self.generation = 1

    def process(self, registry) :
        # forced to put it in list because it had killed the pointer and changed the size :(((((((
        keys_ind = list(registry.get_all_id_with_tosave())

        for name, component_registry in registry.__dict__.items() :
            if not component_registry :
                continue
            dict = {}
            if name == 'haploid_registry' or name == 'fitness_registry' or name == 'controller_network_registry' or name == 'body_registry' or name == 'tosave_registry' or name == 'generation_registry' or name == 'age_registry' or name == 'haploid_parents_registry' or name == 'cppn_registry' :
                for key_ind in keys_ind :
                    dict[key_ind] = component_registry[key_ind]
                self.results_manager.save_generation_registry(dict, name, self.generation)
        for key_ind in keys_ind :
            gen, id = key_ind
            registry.clear_save_from_registry(gen, id)        

        self.generation += 1    


class BothSaveGenSystem() :

    def __str__(self) :
        return "BothSaveGenSystem"

    def __init__(self, config, results_manager, type_genome) :
        self.config = config 
        self.results_manager = results_manager
        self.type_genome = type_genome
        self.generation = 1

    def process(self, registry) :

        if self.type_genome == 'diploid' :
            # forced to put it in list because it had killed the pointer and changed the size :(((((((
            keys_ind = list(registry.get_all_id_with_tosave())

            fitnesses = []
            for key_ind in keys_ind :
                fitnesses.append(registry.fitness_registry[key_ind].fitness)
            fitnesses = np.array(fitnesses)
            sorted_indexes = np.argsort(fitnesses)

            keys_controller = []
            number_to_keep = min(self.config.number_of_reported_individuals, len(keys_ind))
            for taken in range(number_to_keep) :
                index = sorted_indexes[len(keys_ind) - 1 - taken]
                keys_controller.append(keys_ind[index])

            for name, component_registry in registry.__dict__.items() :
                if not component_registry :
                    continue
                dict = {}
                if name == 'genome_registry' or name == 'fitness_registry' or name == 'controller_network_registry' or name == 'body_registry' or name == 'tosave_registry' or name == 'generation_registry' or name == 'age_registry' or name == 'parents_registry' or name == 'cppn_registry' :

                    if name == 'controller_network_registry' :
                        keys = keys_controller
                    else :
                        keys = keys_ind

                    for key_ind in keys :
                        dict[key_ind] = component_registry[key_ind]
                    self.results_manager.save_both_generation_registry(dict, name, self.generation, self.type_genome)
            for key_ind in keys_ind :
                gen, id = key_ind
                registry.clear_save_from_registry(gen, id)        

            self.generation += 1 

        elif self.type_genome == 'haploid' :   
            # forced to put it in list because it had killed the pointer and changed the size :(((((((
            keys_ind = list(registry.get_all_id_with_tosave())

            fitnesses = []
            for key_ind in keys_ind :
                fitnesses.append(registry.fitness_registry[key_ind].fitness)
            fitnesses = np.array(fitnesses)
            sorted_indexes = np.argsort(fitnesses)

            keys_controller = []
            number_to_keep = min(self.config.number_of_reported_individuals, len(keys_ind))
            for taken in range(number_to_keep) :
                index = sorted_indexes[len(keys_ind) - 1 - taken]
                keys_controller.append(keys_ind[index])

            for name, component_registry in registry.__dict__.items() :
                if not component_registry :
                    continue
                dict = {}
                if name == 'haploid_registry' or name == 'fitness_registry' or name == 'controller_network_registry' or name == 'body_registry' or name == 'tosave_registry' or name == 'generation_registry' or name == 'age_registry' or name == 'haploid_parents_registry' or name == 'cppn_registry' :

                    if name == 'controller_network_registry' :
                        keys = keys_controller
                    else :
                        keys = keys_ind

                    for key_ind in keys :
                        dict[key_ind] = component_registry[key_ind]
                    self.results_manager.save_both_generation_registry(dict, name, self.generation, self.type_genome)
            for key_ind in keys_ind :
                gen, id = key_ind
                registry.clear_save_from_registry(gen, id)        

            self.generation += 1    



