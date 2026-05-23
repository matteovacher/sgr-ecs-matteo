import numpy as np 
import rqndom as rd 



class ReproductionSystem :

    def __str__(self) :
        return "ReproductionSystem, tournament is the selection process happening here"
    
    def __init__(self, config, genome_operator, entity_manager, function_pool) :
        self.config = config 
        self.genome_operator = genome_operator
        self.entity_manager = entity_manager 
        self.function_pool = function_pool

    def process(self, registry) : 
        entity_ids = [id for id in registry.get_all_id_with_fitness() if self.entity_manager.is_alive(id) and registry.has_controller_network(id)]

        # les individus sans corps ne se reproduisent pas / individuals without body cannot reproduce 

        new_pop_counter = 0
        number_of_winner = self.config.number_of_winner
        number_in_tournament = self.config.number_in_tournament 
        max_population = self.config.population 
        number_of_elites = self.config.number_of_elites 

        parents_ids = []
        children_entity_ids = []
        elitism = []

        if len(entity_ids) < number_in_tournament :
            raise RuntimeError('not enough valid individual to fit in the tournament. Please change HyperParameters or just the program.')

        fitnesses = np.array([registry.get_fitness(id).fitness for id in entity_ids])
        ids_of_sorted = np.argsort(fitnesses)
        for taken in range(number_of_elites) : 
            id = ids_of_sorted[len(entity_ids) - 1 - taken]
            elitism.append(id)

        for elite in elitism :
            children_entity_ids.append(elite)

        while len(children_entity_ids) < max_population : 
            
            if len(parents_ids) >= 2 : 
                parent1 = parents_ids.pop()
                parent2 = parents_ids.pop()
                genome_parent1 = registry.get_genome(parent1)
                genome_parent2 = registry.get_genome(parent2)
                connections, biases, functions, dominances, nodes  = self.genome_operator.crossover(genome_parent1, genome_parent2)
                child_id = self.entity_manager.create_entity()
                children_entity_ids.append(child_id)
                registry.add_genome(connections[0], connections[1], biases[0], biases[1], functions[0], functions[1], dominances[0], dominances[1], nodes)

            tournament_ids = rd.sample(entity_ids, number_in_tournament)
            fitnesses = np.array([registry.get_fitness(id).fitness for id in tournament_ids])
            ids_of_sorted = np.argsort(fitnesses)
            taken = 0 
            
            for taken in range(number_of_winner) : 
                parents_ids.insert(0, ids_of_sorted[number_in_tournament-1-taken])
            
            for child_entity_id in children_entity_ids :
                genome = registry.get_genome(child_entity_id)
                new_genome = self.genome_operator.mutate(genome, self.config.sigma_weight, self.config.sigma_bias, self.config.threshold_weight, self.config.threshold_bias, self.config.threshold_function, self.config.threshold_dominance, self.function_pool.pool)
                
                if child_entity_id not in elitism :
                    registry.add_genome(child_entity_id, new_genome.connections[0], new_genome.connections[1], new_genome.biases[0], new_genome.biases[1], new_genome.functions[0], new_genome.functions[1], new_genome.dominances[0], new_genome.dominances[1], new_genome.nodes)                                        
                else :
                    registry.modify_genome(child_entity_id, new_genome)

        for entity_id in entity_ids :
            if entity_id not in elitism :
                self.entity_manager.destroy_entity(entity_id)

        # n ajoute le reporter ici aussi      