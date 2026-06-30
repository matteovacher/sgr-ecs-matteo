import numpy as np 
import random as rd 



class ReproductionSystem :

    def __str__(self) :
        return "ReproductionSystem, tournament is the selection process happening here"
    
    def __init__(self, config, genome_operator, entity_manager, function_pool, results_manager) :
        self.config = config 
        self.genome_operator = genome_operator
        self.entity_manager = entity_manager 
        self.function_pool = function_pool
        self.results_manager = results_manager

    def process(self, registry) : 
        entity_ids = [id for id in registry.get_all_id_with_fitness() if self.entity_manager.is_alive(id) and registry.has_controller_network(id)]

        # les individus sans corps ne se reproduisent pas / individuals without body cannot reproduce 

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
            elitism.append(entity_ids[id])

        for elite in elitism :
            children_entity_ids.append(elite)
            age = registry.get_age(elite).age 
            birthday = age + 1
            registry.add_parents(elite, elite, elite, 0, 0)
            registry.modify_age(elite, birthday)

        while len(children_entity_ids) < max_population : 
            
            if len(parents_ids) >= 2 : 
                age = 1
                parent1 = parents_ids.pop()
                parent2 = parents_ids.pop()
                genome_parent1 = registry.get_genome(parent1)
                genome_parent2 = registry.get_genome(parent2)
                connections, biases, functions, dominances, nodes, choice1, choice2  = self.genome_operator.crossover(genome_parent1, genome_parent2)
                child_id = self.entity_manager.create_entity()
                children_entity_ids.append(child_id)
                registry.add_parents(child_id, parent1, parent2, choice1, choice2)
                registry.add_genome(child_id, connections[0], connections[1], biases[0], biases[1], functions[0], functions[1], dominances[0], dominances[1], nodes)
                registry.add_age(child_id, age)

            tournament_ids = rd.sample(entity_ids, number_in_tournament)
            fitnesses = np.array([registry.get_fitness(id).fitness for id in tournament_ids])
            ids_of_sorted = np.argsort(fitnesses)
            taken = 0 
            
            for taken in range(number_of_winner) : 
                parents_ids.insert(0, tournament_ids[ids_of_sorted[number_in_tournament-1-taken]])
            
        for child_entity_id in children_entity_ids :
            if child_entity_id not in elitism :
                genome = registry.get_genome(child_entity_id)
                new_genome = self.genome_operator.mutate(genome, self.config.sigma_weight, self.config.sigma_bias, self.config.threshold_weight, self.config.threshold_bias, self.config.threshold_function, self.config.threshold_dominance, self.function_pool.pool)
                registry.add_genome(child_entity_id, new_genome.connections[0], new_genome.connections[1], new_genome.biases[0], new_genome.biases[1], new_genome.functions[0], new_genome.functions[1], new_genome.dominances[0], new_genome.dominances[1], new_genome.nodes)                                        
            

        
        all_alive_entity_ids = [id for id in registry.get_all_id_with_genome() if self.entity_manager.is_alive(id)]
        for entity_id in all_alive_entity_ids :
            if entity_id not in children_entity_ids:
                self.entity_manager.destroy_entity(entity_id)
                registry.clear_ind_from_registry(entity_id)


            

        self.results_manager.end_generation()
    

class HaploidReproductionSystem :

    def __str__(self) :
        return "HaploidReproductionSystem, tournament is the selection process happening here"
    
    def __init__(self, config, genome_operator, entity_manager, function_pool, results_manager) :
        self.config = config 
        self.genome_operator = genome_operator
        self.entity_manager = entity_manager 
        self.function_pool = function_pool
        self.results_manager = results_manager

    def process(self, registry) : 
        entity_ids = [id for id in registry.get_all_id_with_fitness() if self.entity_manager.is_alive(id) and registry.has_controller_network(id)]

        # les individus sans corps ne se reproduisent pas / individuals without body cannot reproduce 

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
            elitism.append(entity_ids[id])

        for elite in elitism :
            children_entity_ids.append(elite)
            age = registry.get_age(elite).age 
            birthday = age + 1
            registry.add_haploid_parents(elite, elite, elite)
            registry.modify_age(elite, birthday)

        while len(children_entity_ids) < max_population : 
            
            if len(parents_ids) >= 2 : 
                age = 1
                parent1 = parents_ids.pop()
                parent2 = parents_ids.pop()
                haploid_parent1 = registry.get_haploid(parent1)
                haploid_parent2 = registry.get_haploid(parent2)
                connections, biases, functions, dominances, nodes = self.genome_operator.crossover(haploid_parent1, haploid_parent2)
                child_id = self.entity_manager.create_entity()
                children_entity_ids.append(child_id)
                registry.add_haploid_parents(child_id, parent1, parent2)
                registry.add_haploid(child_id, connections, biases, functions, dominances, nodes)
                registry.add_age(child_id, age)

            tournament_ids = rd.sample(entity_ids, number_in_tournament)
            fitnesses = np.array([registry.get_fitness(id).fitness for id in tournament_ids])
            ids_of_sorted = np.argsort(fitnesses)
            taken = 0 
            
            for taken in range(number_of_winner) : 
                parents_ids.insert(0, tournament_ids[ids_of_sorted[number_in_tournament-1-taken]])
            
        for child_entity_id in children_entity_ids :
            if child_entity_id not in elitism :
                haploid = registry.get_haploid(child_entity_id)
                new_haploid = self.genome_operator.mutate(haploid, self.config.sigma_weight, self.config.sigma_bias, self.config.threshold_weight, self.config.threshold_bias, self.config.threshold_function, self.config.threshold_dominance, self.function_pool.pool)
                registry.add_haploid(child_entity_id, new_haploid.connections, new_haploid.biases, new_haploid.functions, new_haploid.dominances, new_haploid.nodes)                                        
            

        
        all_alive_entity_ids = [id for id in registry.get_all_id_with_haploid() if self.entity_manager.is_alive(id)]
        for entity_id in all_alive_entity_ids :
            if entity_id not in children_entity_ids:
                self.entity_manager.destroy_entity(entity_id)
                registry.clear_ind_from_registry(entity_id)
                # clear for RAM purposes

        self.results_manager.end_generation()



class BothReproductionSystem : 

    def __str__(self) :
        return "BothReproductionSystem, tournament is the selection process happening here"
    
    def __init__(self, config, genome_operator, entity_manager, function_pool, results_manager, type_genome) :
        self.config = config 
        self.genome_operator = genome_operator
        self.entity_manager = entity_manager 
        self.function_pool = function_pool
        self.results_manager = results_manager
        self.type_genome = type_genome

    def process(self, registry) : 

        if self.type_genome == 'diploid' :

            entity_ids = [id for id in registry.get_all_id_with_fitness() if self.entity_manager.is_alive(id) and registry.has_controller_network(id)]

            # les individus sans corps ne se reproduisent pas / individuals without body cannot reproduce 

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
                elitism.append(entity_ids[id])

            for elite in elitism :
                children_entity_ids.append(elite)
                age = registry.get_age(elite).age 
                birthday = age + 1
                registry.add_parents(elite, elite, elite, 0, 0)
                registry.modify_age(elite, birthday)

            while len(children_entity_ids) < max_population : 
                
                if len(parents_ids) >= 2 : 
                    age = 1
                    parent1 = parents_ids.pop()
                    parent2 = parents_ids.pop()
                    genome_parent1 = registry.get_genome(parent1)
                    genome_parent2 = registry.get_genome(parent2)
                    connections, biases, functions, dominances, nodes, choice1, choice2  = self.genome_operator.crossover(genome_parent1, genome_parent2)
                    child_id = self.entity_manager.create_entity()
                    children_entity_ids.append(child_id)
                    registry.add_parents(child_id, parent1, parent2, choice1, choice2)
                    registry.add_genome(child_id, connections[0], connections[1], biases[0], biases[1], functions[0], functions[1], dominances[0], dominances[1], nodes)
                    registry.add_age(child_id, age)

                tournament_ids = rd.sample(entity_ids, number_in_tournament)
                fitnesses = np.array([registry.get_fitness(id).fitness for id in tournament_ids])
                ids_of_sorted = np.argsort(fitnesses)
                taken = 0 
                
                for taken in range(number_of_winner) : 
                    parents_ids.insert(0, tournament_ids[ids_of_sorted[number_in_tournament-1-taken]])
                
            for child_entity_id in children_entity_ids :
                if child_entity_id not in elitism :
                    genome = registry.get_genome(child_entity_id)
                    new_genome = self.genome_operator.mutate(genome, self.config.sigma_weight, self.config.sigma_bias, self.config.threshold_weight, self.config.threshold_bias, self.config.threshold_function, self.config.threshold_dominance, self.function_pool.pool)
                    registry.add_genome(child_entity_id, new_genome.connections[0], new_genome.connections[1], new_genome.biases[0], new_genome.biases[1], new_genome.functions[0], new_genome.functions[1], new_genome.dominances[0], new_genome.dominances[1], new_genome.nodes)                                        
                

            
            all_alive_entity_ids = [id for id in registry.get_all_id_with_genome() if self.entity_manager.is_alive(id)]
            for entity_id in all_alive_entity_ids :
                if entity_id not in children_entity_ids:
                    self.entity_manager.destroy_entity(entity_id)
                    registry.clear_ind_from_registry(entity_id)

            self.results_manager.end_both_generation(self.type_genome)
    
        elif self.type_genome == 'haploid' : 

            entity_ids = [id for id in registry.get_all_id_with_fitness() if self.entity_manager.is_alive(id) and registry.has_controller_network(id)]

            # les individus sans corps ne se reproduisent pas / individuals without body cannot reproduce 

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
                elitism.append(entity_ids[id])

            for elite in elitism :
                children_entity_ids.append(elite)
                age = registry.get_age(elite).age 
                birthday = age + 1
                registry.add_haploid_parents(elite, elite, elite)
                registry.modify_age(elite, birthday)

            while len(children_entity_ids) < max_population : 
                
                if len(parents_ids) >= 2 : 
                    age = 1
                    parent1 = parents_ids.pop()
                    parent2 = parents_ids.pop()
                    haploid_parent1 = registry.get_haploid(parent1)
                    haploid_parent2 = registry.get_haploid(parent2)
                    connections, biases, functions, dominances, nodes = self.genome_operator.crossover(haploid_parent1, haploid_parent2)
                    child_id = self.entity_manager.create_entity()
                    children_entity_ids.append(child_id)
                    registry.add_haploid_parents(child_id, parent1, parent2)
                    registry.add_haploid(child_id, connections, biases, functions, dominances, nodes)
                    registry.add_age(child_id, age)

                tournament_ids = rd.sample(entity_ids, number_in_tournament)
                fitnesses = np.array([registry.get_fitness(id).fitness for id in tournament_ids])
                ids_of_sorted = np.argsort(fitnesses)
                taken = 0 
                
                for taken in range(number_of_winner) : 
                    parents_ids.insert(0, tournament_ids[ids_of_sorted[number_in_tournament-1-taken]])
                
            for child_entity_id in children_entity_ids :
                if child_entity_id not in elitism :
                    haploid = registry.get_haploid(child_entity_id)
                    new_haploid = self.genome_operator.mutate(haploid, self.config.sigma_weight, self.config.sigma_bias, self.config.threshold_weight, self.config.threshold_bias, self.config.threshold_function, self.config.threshold_dominance, self.function_pool.pool)
                    registry.add_haploid(child_entity_id, new_haploid.connections, new_haploid.biases, new_haploid.functions, new_haploid.dominances, new_haploid.nodes)                                        
                

            
            all_alive_entity_ids = [id for id in registry.get_all_id_with_haploid() if self.entity_manager.is_alive(id)]
            for entity_id in all_alive_entity_ids :
                if entity_id not in children_entity_ids:
                    self.entity_manager.destroy_entity(entity_id)
                    registry.clear_ind_from_registry(entity_id)
                    # clear for RAM purposes

            self.results_manager.end_both_generation(self.type_genome)

            
class BothCoReproductionSystem : 

    def __str__(self) :
        return "BothReproductionSystem, tournament is the selection process happening here with co dominance for haploid "
    
    def __init__(self, config, genome_operator, entity_manager, function_pool, results_manager, type_genome) :
        self.config = config 
        self.genome_operator = genome_operator
        self.entity_manager = entity_manager 
        self.function_pool = function_pool
        self.results_manager = results_manager
        self.type_genome = type_genome

    def process(self, registry) : 

        if self.type_genome == 'diploid' :

            entity_ids = [id for id in registry.get_all_id_with_fitness() if self.entity_manager.is_alive(id) and registry.has_controller_network(id)]

            # les individus sans corps ne se reproduisent pas / individuals without body cannot reproduce 

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
                elitism.append(entity_ids[id])

            for elite in elitism :
                children_entity_ids.append(elite)
                age = registry.get_age(elite).age 
                birthday = age + 1
                registry.add_parents(elite, elite, elite, 0, 0)
                registry.modify_age(elite, birthday)

            while len(children_entity_ids) < max_population : 
                
                if len(parents_ids) >= 2 : 
                    age = 1
                    parent1 = parents_ids.pop()
                    parent2 = parents_ids.pop()
                    genome_parent1 = registry.get_genome(parent1)
                    genome_parent2 = registry.get_genome(parent2)
                    connections, biases, functions, dominances, nodes, choice1, choice2  = self.genome_operator.crossover(genome_parent1, genome_parent2)
                    child_id = self.entity_manager.create_entity()
                    children_entity_ids.append(child_id)
                    registry.add_parents(child_id, parent1, parent2, choice1, choice2)
                    registry.add_genome(child_id, connections[0], connections[1], biases[0], biases[1], functions[0], functions[1], dominances[0], dominances[1], nodes)
                    registry.add_age(child_id, age)

                tournament_ids = rd.sample(entity_ids, number_in_tournament)
                fitnesses = np.array([registry.get_fitness(id).fitness for id in tournament_ids])
                ids_of_sorted = np.argsort(fitnesses)
                taken = 0 
                
                for taken in range(number_of_winner) : 
                    parents_ids.insert(0, tournament_ids[ids_of_sorted[number_in_tournament-1-taken]])
                
            for child_entity_id in children_entity_ids :
                if child_entity_id not in elitism :
                    genome = registry.get_genome(child_entity_id)
                    new_genome = self.genome_operator.mutate(genome, self.config.sigma_weight, self.config.sigma_bias, self.config.threshold_weight, self.config.threshold_bias, self.config.threshold_function, self.config.threshold_dominance, self.function_pool.pool)
                    registry.add_genome(child_entity_id, new_genome.connections[0], new_genome.connections[1], new_genome.biases[0], new_genome.biases[1], new_genome.functions[0], new_genome.functions[1], new_genome.dominances[0], new_genome.dominances[1], new_genome.nodes)                                        
                

            
            all_alive_entity_ids = [id for id in registry.get_all_id_with_genome() if self.entity_manager.is_alive(id)]
            for entity_id in all_alive_entity_ids :
                if entity_id not in children_entity_ids:
                    self.entity_manager.destroy_entity(entity_id)
                    registry.clear_ind_from_registry(entity_id)

            self.results_manager.end_both_generation(self.type_genome)
    
        elif self.type_genome == 'haploid' : 

            entity_ids = [id for id in registry.get_all_id_with_fitness() if self.entity_manager.is_alive(id) and registry.has_controller_network(id)]

            # les individus sans corps ne se reproduisent pas / individuals without body cannot reproduce 

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
                elitism.append(entity_ids[id])

            for elite in elitism :
                children_entity_ids.append(elite)
                age = registry.get_age(elite).age 
                birthday = age + 1
                registry.add_haploid_parents(elite, elite, elite)
                registry.modify_age(elite, birthday)

            while len(children_entity_ids) < max_population : 
                
                if len(parents_ids) >= 2 : 
                    age = 1
                    parent1 = parents_ids.pop()
                    parent2 = parents_ids.pop()
                    haploid_parent1 = registry.get_haploid(parent1)
                    haploid_parent2 = registry.get_haploid(parent2)
                    connections, biases, functions, dominances, nodes = self.genome_operator.cocrossover(haploid_parent1, haploid_parent2)
                    child_id = self.entity_manager.create_entity()
                    children_entity_ids.append(child_id)
                    registry.add_haploid_parents(child_id, parent1, parent2)
                    registry.add_haploid(child_id, connections, biases, functions, dominances, nodes)
                    registry.add_age(child_id, age)

                tournament_ids = rd.sample(entity_ids, number_in_tournament)
                fitnesses = np.array([registry.get_fitness(id).fitness for id in tournament_ids])
                ids_of_sorted = np.argsort(fitnesses)
                taken = 0 
                
                for taken in range(number_of_winner) : 
                    parents_ids.insert(0, tournament_ids[ids_of_sorted[number_in_tournament-1-taken]])
                
            for child_entity_id in children_entity_ids :
                if child_entity_id not in elitism :
                    haploid = registry.get_haploid(child_entity_id)
                    new_haploid = self.genome_operator.mutate(haploid, self.config.sigma_weight, self.config.sigma_bias, self.config.threshold_weight, self.config.threshold_bias, self.config.threshold_function, self.config.threshold_dominance, self.function_pool.pool)
                    registry.add_haploid(child_entity_id, new_haploid.connections, new_haploid.biases, new_haploid.functions, new_haploid.dominances, new_haploid.nodes)                                        
                

            
            all_alive_entity_ids = [id for id in registry.get_all_id_with_haploid() if self.entity_manager.is_alive(id)]
            for entity_id in all_alive_entity_ids :
                if entity_id not in children_entity_ids:
                    self.entity_manager.destroy_entity(entity_id)
                    registry.clear_ind_from_registry(entity_id)
                    # clear for RAM purposes

            self.results_manager.end_both_generation(self.type_genome)



class BothModularCoReproductionSystem : 

    def __str__(self) :
        return "Modular BothReproductionSystem, tournament is the selection process happening here with co dominance for haploid "
    
    def __init__(self, config, genome_operator, entity_manager, function_pool, results_manager, type_genome) :
        self.config = config 
        self.genome_operator = genome_operator
        self.entity_manager = entity_manager 
        self.function_pool = function_pool
        self.results_manager = results_manager
        self.type_genome = type_genome

    def process(self, registry) : 

        if self.type_genome == 'diploid' :

            entity_ids = [id for id in registry.get_all_id_with_fitness() if self.entity_manager.is_alive(id) and registry.has_controller_network(id)]

            # les individus sans corps ne se reproduisent pas / individuals without body cannot reproduce 

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
                elitism.append(entity_ids[id])

            for elite in elitism :
                children_entity_ids.append(elite)
                age = registry.get_age(elite).age 
                birthday = age + 1
                registry.add_parents(elite, elite, elite, 0, 0)
                registry.modify_age(elite, birthday)

            while len(children_entity_ids) < max_population : 
                
                if len(parents_ids) >= 2 : 
                    age = 1
                    parent1 = parents_ids.pop()
                    parent2 = parents_ids.pop()
                    genome_parent1 = registry.get_genome(parent1)
                    genome_parent2 = registry.get_genome(parent2)
                    connections, biases, functions, dominances, nodes, choice1, choice2  = self.genome_operator.crossover_with_modu_regu(genome_parent1, genome_parent2)
                    child_id = self.entity_manager.create_entity()
                    children_entity_ids.append(child_id)
                    registry.add_parents(child_id, parent1, parent2, choice1, choice2)
                    registry.add_genome(child_id, connections[0], connections[1], biases[0], biases[1], functions[0], functions[1], dominances[0], dominances[1], nodes)
                    registry.add_age(child_id, age)

                tournament_ids = rd.sample(entity_ids, number_in_tournament)
                fitnesses = np.array([registry.get_fitness(id).fitness for id in tournament_ids])
                ids_of_sorted = np.argsort(fitnesses)
                taken = 0 
                
                for taken in range(number_of_winner) : 
                    parents_ids.insert(0, tournament_ids[ids_of_sorted[number_in_tournament-1-taken]])
                
            for child_entity_id in children_entity_ids :
                if child_entity_id not in elitism :
                    genome = registry.get_genome(child_entity_id)
                    new_genome = self.genome_operator.mutate_with_modu_regu(genome, self.config.sigma_weight, self.config.sigma_bias, self.config.threshold_weight, self.config.threshold_bias, self.config.threshold_function, self.config.threshold_dominance, self.function_pool.pool)
                    registry.add_genome(child_entity_id, new_genome.connections[0], new_genome.connections[1], new_genome.biases[0], new_genome.biases[1], new_genome.functions[0], new_genome.functions[1], new_genome.dominances[0], new_genome.dominances[1], new_genome.nodes)                                        
                

            
            all_alive_entity_ids = [id for id in registry.get_all_id_with_genome() if self.entity_manager.is_alive(id)]
            for entity_id in all_alive_entity_ids :
                if entity_id not in children_entity_ids:
                    self.entity_manager.destroy_entity(entity_id)
                    registry.clear_ind_from_registry(entity_id)

            self.results_manager.end_both_generation(self.type_genome)
    
        elif self.type_genome == 'haploid' : 

            entity_ids = [id for id in registry.get_all_id_with_fitness() if self.entity_manager.is_alive(id) and registry.has_controller_network(id)]

            # les individus sans corps ne se reproduisent pas / individuals without body cannot reproduce 

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
                elitism.append(entity_ids[id])

            for elite in elitism :
                children_entity_ids.append(elite)
                age = registry.get_age(elite).age 
                birthday = age + 1
                registry.add_haploid_parents(elite, elite, elite)
                registry.modify_age(elite, birthday)

            while len(children_entity_ids) < max_population : 
                
                if len(parents_ids) >= 2 : 
                    age = 1
                    parent1 = parents_ids.pop()
                    parent2 = parents_ids.pop()
                    haploid_parent1 = registry.get_haploid(parent1)
                    haploid_parent2 = registry.get_haploid(parent2)
                    connections, biases, functions, dominances, nodes = self.genome_operator.cocrossover_woth_modu_regu(haploid_parent1, haploid_parent2)
                    child_id = self.entity_manager.create_entity()
                    children_entity_ids.append(child_id)
                    registry.add_haploid_parents(child_id, parent1, parent2)
                    registry.add_haploid(child_id, connections, biases, functions, dominances, nodes)
                    registry.add_age(child_id, age)

                tournament_ids = rd.sample(entity_ids, number_in_tournament)
                fitnesses = np.array([registry.get_fitness(id).fitness for id in tournament_ids])
                ids_of_sorted = np.argsort(fitnesses)
                taken = 0 
                
                for taken in range(number_of_winner) : 
                    parents_ids.insert(0, tournament_ids[ids_of_sorted[number_in_tournament-1-taken]])
                
            for child_entity_id in children_entity_ids :
                if child_entity_id not in elitism :
                    haploid = registry.get_haploid(child_entity_id)
                    new_haploid = self.genome_operator.mutate_with_modu_regu(haploid, self.config.sigma_weight, self.config.sigma_bias, self.config.threshold_weight, self.config.threshold_bias, self.config.threshold_function, self.config.threshold_dominance, self.function_pool.pool)
                    registry.add_haploid(child_entity_id, new_haploid.connections, new_haploid.biases, new_haploid.functions, new_haploid.dominances, new_haploid.nodes)                                        
                

            
            all_alive_entity_ids = [id for id in registry.get_all_id_with_haploid() if self.entity_manager.is_alive(id)]
            for entity_id in all_alive_entity_ids :
                if entity_id not in children_entity_ids:
                    self.entity_manager.destroy_entity(entity_id)
                    registry.clear_ind_from_registry(entity_id)
                    # clear for RAM purposes

            self.results_manager.end_both_generation(self.type_genome)


