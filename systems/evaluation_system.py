import numpy as np 


class EvaluationSystem :

    def __str__(self) :
        return "EvaluationSystem, evaluate all individuals"
    

    def __init__(self, config, robot_simulator, network_manager, parallel_tool, entity_manager, results_manager) :
        self.config = config 
        self.robot_simulator = robot_simulator 
        self.network_manager = network_manager 
        self.parallel_tool = parallel_tool 
        self.entity_manager = entity_manager 
        self.results_manager = results_manager 
        self.generation = 1


    def process(self, registry ) :
        
        
        entity_ids = [id for id in registry.get_all_id_with_genome() if self.entity_manager.is_alive(id) and registry.has_controller_network(id)]
        controllers = []
        bodies = []


        for entity_id in entity_ids :
            controller = registry.get_controller_network(entity_id)
            body = registry.get_body(entity_id)
            controllers.append(controller)
            bodies.append(body.body)

        n_steps_list = [self.config.n_steps for _ in range(len(entity_ids))]
        network_manager_list = [self.network_manager for _ in range(len(entity_ids))]
        function = self.robot_simulator.simulate

        chunk = list(zip(entity_ids, bodies, controllers, n_steps_list, network_manager_list))
        results = self.parallel_tool.run(function, chunk)

        tosave = True
        fitnesses = []
        ids = []
        ages = []
        for entity_id, fitness, finished in results :
            ids.append(entity_id)
            fitnesses.append(fitness)
            registry.add_fitness(entity_id, fitness, finished)
            ages.append(registry.get_age(entity_id).age)
            registry.add_tosave(self.generation, entity_id, tosave)
            registry.snapshot(self.generation, entity_id)



        fitnesses = np.array(fitnesses)
        arg_sorted_fitnesses = np.argsort(fitnesses)
        bests = []
        number_of_reported_individuals = self.config.number_of_reported_individuals
        number_to_report = min(number_of_reported_individuals, len(entity_ids))
        for taken in range(number_to_report) : 
            id = arg_sorted_fitnesses[len(entity_ids) - 1 - taken]
            bests.append((ids[id], fitnesses[id], ages[id]))
                  
        
        invalid = self.config.population - len(entity_ids)

        self.results_manager.bests(bests)
        average, sigma =self.results_manager.average_ind(fitnesses)
        best_id, fitness_best, average_best, sigma_best = self.results_manager.average_best(bests)
        self.results_manager.deficient(invalid)

        generation_id = self.entity_manager.create_entity()
        registry.add_statistic(generation_id, self.generation, average, sigma, best_id, fitness_best, average_best, sigma_best)
        

        self.generation += 1

        # ici rajouter ensuite les individus qui sont invalide et faire les reports 


class HaploidEvaluationSystem :

    def __str__(self) :
        return "HaploidEvaluationSystem, evaluate all individuals"
    
    def __init__(self, config, robot_simulator, network_manager, parallel_tool, entity_manager, results_manager) :
        self.config = config 
        self.robot_simulator = robot_simulator 
        self.network_manager = network_manager 
        self.parallel_tool = parallel_tool 
        self.entity_manager = entity_manager 
        self.results_manager = results_manager 
        self.generation = 1
        
    def process(self, registry ) :
        
        
        entity_ids = [id for id in registry.get_all_id_with_haploid() if self.entity_manager.is_alive(id) and registry.has_controller_network(id)]
        controllers = []
        bodies = []


        for entity_id in entity_ids :
            controller = registry.get_controller_network(entity_id)
            body = registry.get_body(entity_id)
            controllers.append(controller)
            bodies.append(body.body)

        n_steps_list = [self.config.n_steps for _ in range(len(entity_ids))]
        network_manager_list = [self.network_manager for _ in range(len(entity_ids))]
        function = self.robot_simulator.simulate

        chunk = list(zip(entity_ids, bodies, controllers, n_steps_list, network_manager_list))
        results = self.parallel_tool.run(function, chunk)

        tosave = True
        fitnesses = []
        ids = []
        ages = []
        for entity_id, fitness, finished in results :
            ids.append(entity_id)
            fitnesses.append(fitness)
            registry.add_fitness(entity_id, fitness, finished)
            ages.append(registry.get_age(entity_id).age)
            registry.add_tosave(self.generation, entity_id, tosave)
            registry.snapshot(self.generation, entity_id)



        fitnesses = np.array(fitnesses)
        arg_sorted_fitnesses = np.argsort(fitnesses)
        bests = []
        number_of_reported_individuals = self.config.number_of_reported_individuals
        number_to_report = min(number_of_reported_individuals, len(entity_ids))
        for taken in range(number_to_report) : 
            id = arg_sorted_fitnesses[len(entity_ids) - 1 - taken]
            bests.append((ids[id], fitnesses[id], ages[id]))
                  
        
        invalid = self.config.population - len(entity_ids)

        self.results_manager.bests(bests)
        average, sigma =self.results_manager.average_ind(fitnesses)
        best_id, fitness_best, average_best, sigma_best = self.results_manager.average_best(bests)
        self.results_manager.deficient(invalid)

        generation_id = self.entity_manager.create_entity()
        registry.add_statistic(generation_id, self.generation, average, sigma, best_id, fitness_best, average_best, sigma_best)
        
        self.generation += 1   

    
class BothEvaluationSystem :

    def __str__(self) :
        return "BothEvaluationSystem, evaluate all individuals"
    
    def __init__(self, config, robot_simulator, network_manager, parallel_tool, entity_manager, results_manager, type_genome) :
        self.config = config 
        self.robot_simulator = robot_simulator 
        self.network_manager = network_manager 
        self.parallel_tool = parallel_tool 
        self.entity_manager = entity_manager 
        self.results_manager = results_manager 
        self.type_genome = type_genome
        self.generation = 1
    
    def process(self, registry) :
        if self.type_genome == 'diploid' : 
            entity_ids = [id for id in registry.get_all_id_with_genome() if self.entity_manager.is_alive(id) and registry.has_controller_network(id)]
            controllers = []
            bodies = []


            for entity_id in entity_ids :
                controller = registry.get_controller_network(entity_id)
                body = registry.get_body(entity_id)
                controllers.append(controller)
                bodies.append(body.body)

            n_steps_list = [self.config.n_steps for _ in range(len(entity_ids))]
            network_manager_list = [self.network_manager for _ in range(len(entity_ids))]
            function = self.robot_simulator.simulate

            chunk = list(zip(entity_ids, bodies, controllers, n_steps_list, network_manager_list))
            results = self.parallel_tool.run(function, chunk)

            tosave = True
            fitnesses = []
            ids = []
            ages = []
            for entity_id, fitness, finished in results :
                ids.append(entity_id)
                fitnesses.append(fitness)
                registry.add_fitness(entity_id, fitness, finished)
                ages.append(registry.get_age(entity_id).age)
                registry.add_tosave(self.generation, entity_id, tosave)
                registry.snapshot(self.generation, entity_id)



            fitnesses = np.array(fitnesses)
            arg_sorted_fitnesses = np.argsort(fitnesses)
            bests = []
            number_of_reported_individuals = self.config.number_of_reported_individuals
            number_to_report = min(number_of_reported_individuals, len(entity_ids))
            for taken in range(number_to_report) : 
                id = arg_sorted_fitnesses[len(entity_ids) - 1 - taken]
                bests.append((ids[id], fitnesses[id], ages[id]))
                    
            
            invalid = self.config.population - len(entity_ids)

            self.results_manager.both_bests(bests, self.type_genome)
            average, sigma = self.results_manager.both_average_ind(fitnesses, self.type_genome)
            best_id, fitness_best, average_best, sigma_best = self.results_manager.both_average_best(bests, self.type_genome)
            self.results_manager.both_deficient(invalid, self.type_genome)

            generation_id = self.entity_manager.create_entity()
            registry.add_statistic(generation_id, self.generation, average, sigma, best_id, fitness_best, average_best, sigma_best)
            

            self.generation += 1
        
        elif self.type_genome == 'haploid' :
            entity_ids = [id for id in registry.get_all_id_with_haploid() if self.entity_manager.is_alive(id) and registry.has_controller_network(id)]
            controllers = []
            bodies = []


            for entity_id in entity_ids :
                controller = registry.get_controller_network(entity_id)
                body = registry.get_body(entity_id)
                controllers.append(controller)
                bodies.append(body.body)

            n_steps_list = [self.config.n_steps for _ in range(len(entity_ids))]
            network_manager_list = [self.network_manager for _ in range(len(entity_ids))]
            function = self.robot_simulator.simulate

            chunk = list(zip(entity_ids, bodies, controllers, n_steps_list, network_manager_list))
            results = self.parallel_tool.run(function, chunk)

            tosave = True
            fitnesses = []
            ids = []
            ages = []
            for entity_id, fitness, finished in results :
                ids.append(entity_id)
                fitnesses.append(fitness)
                registry.add_fitness(entity_id, fitness, finished)
                ages.append(registry.get_age(entity_id).age)
                registry.add_tosave(self.generation, entity_id, tosave)
                registry.snapshot(self.generation, entity_id)



            fitnesses = np.array(fitnesses)
            arg_sorted_fitnesses = np.argsort(fitnesses)
            bests = []
            number_of_reported_individuals = self.config.number_of_reported_individuals
            number_to_report = min(number_of_reported_individuals, len(entity_ids))
            for taken in range(number_to_report) : 
                id = arg_sorted_fitnesses[len(entity_ids) - 1 - taken]
                bests.append((ids[id], fitnesses[id], ages[id]))
                    
            
            invalid = self.config.population - len(entity_ids)

            self.results_manager.both_bests(bests, self.type_genome)
            average, sigma =self.results_manager.both_average_ind(fitnesses, self.type_genome)
            best_id, fitness_best, average_best, sigma_best = self.results_manager.both_average_best(bests, self.type_genome)
            self.results_manager.both_deficient(invalid, self.type_genome)

            generation_id = self.entity_manager.create_entity()
            registry.add_statistic(generation_id, self.generation, average, sigma, best_id, fitness_best, average_best, sigma_best)
            
            self.generation += 1   
        
        else : 
            raise Exception('The type of genome is not supported... Problem with type_genome')


class BothEnvEvaluationSystem() :

    def __str__(self) :
        return "BothEnvEvaluationSystem, evaluate all individuals, with diff env"
    
    def __init__(self, config, robot_simulator, network_manager, parallel_tool, entity_manager, results_manager, type_genome, type_env) :
        self.config = config 
        self.robot_simulator = robot_simulator 
        self.network_manager = network_manager 
        self.parallel_tool = parallel_tool 
        self.entity_manager = entity_manager 
        self.results_manager = results_manager 
        self.type_genome = type_genome
        self.generation = 1
        self.type_env = type_env

    def process(self, registry) :
        if self.type_genome == 'diploid' : 
            entity_ids = [id for id in registry.get_all_id_with_genome() if self.entity_manager.is_alive(id) and registry.has_controller_network(id)]
            controllers = []
            bodies = []


            for entity_id in entity_ids :
                controller = registry.get_controller_network(entity_id)
                body = registry.get_body(entity_id)
                controllers.append(controller)
                bodies.append(body.body)

            n_steps_list = [self.config.n_steps for _ in range(len(entity_ids))]
            network_manager_list = [self.network_manager for _ in range(len(entity_ids))]
            function = self.robot_simulator.simulate_mode_env

            chunk = list(zip(entity_ids, bodies, controllers, n_steps_list, network_manager_list))
            results = self.parallel_tool.run(function, chunk)

            tosave = True
            fitnesses = []
            ids = []
            ages = []
            for entity_id, fitness, finished in results :
                ids.append(entity_id)
                fitnesses.append(fitness)
                registry.add_fitness(entity_id, fitness, finished)
                ages.append(registry.get_age(entity_id).age)
                registry.add_tosave(self.generation, entity_id, tosave)
                registry.snapshot(self.generation, entity_id)



            fitnesses = np.array(fitnesses)
            arg_sorted_fitnesses = np.argsort(fitnesses)
            bests = []
            number_of_reported_individuals = self.config.number_of_reported_individuals
            number_to_report = min(number_of_reported_individuals, len(entity_ids))
            for taken in range(number_to_report) : 
                id = arg_sorted_fitnesses[len(entity_ids) - 1 - taken]
                bests.append((ids[id], fitnesses[id], ages[id]))
                    
            
            invalid = self.config.population - len(entity_ids)

            self.results_manager.both_bests(bests, self.type_genome)
            average, sigma = self.results_manager.both_average_ind(fitnesses, self.type_genome)
            best_id, fitness_best, average_best, sigma_best = self.results_manager.both_average_best(bests, self.type_genome)
            self.results_manager.both_deficient(invalid, self.type_genome)

            generation_id = self.entity_manager.create_entity()
            registry.add_statistic(generation_id, self.generation, average, sigma, best_id, fitness_best, average_best, sigma_best)
            

            self.generation += 1
        
        elif self.type_genome == 'haploid' :
            entity_ids = [id for id in registry.get_all_id_with_haploid() if self.entity_manager.is_alive(id) and registry.has_controller_network(id)]
            controllers = []
            bodies = []


            for entity_id in entity_ids :
                controller = registry.get_controller_network(entity_id)
                body = registry.get_body(entity_id)
                controllers.append(controller)
                bodies.append(body.body)

            n_steps_list = [self.config.n_steps for _ in range(len(entity_ids))]
            network_manager_list = [self.network_manager for _ in range(len(entity_ids))]
            function = self.robot_simulator.simulate_mode_env

            chunk = list(zip(entity_ids, bodies, controllers, n_steps_list, network_manager_list))
            results = self.parallel_tool.run(function, chunk)

            tosave = True
            fitnesses = []
            ids = []
            ages = []
            for entity_id, fitness, finished in results :
                ids.append(entity_id)
                fitnesses.append(fitness)
                registry.add_fitness(entity_id, fitness, finished)
                ages.append(registry.get_age(entity_id).age)
                registry.add_tosave(self.generation, entity_id, tosave)
                registry.snapshot(self.generation, entity_id)



            fitnesses = np.array(fitnesses)
            arg_sorted_fitnesses = np.argsort(fitnesses)
            bests = []
            number_of_reported_individuals = self.config.number_of_reported_individuals
            number_to_report = min(number_of_reported_individuals, len(entity_ids))
            for taken in range(number_to_report) : 
                id = arg_sorted_fitnesses[len(entity_ids) - 1 - taken]
                bests.append((ids[id], fitnesses[id], ages[id]))
                    
            
            invalid = self.config.population - len(entity_ids)

            self.results_manager.both_bests(bests, self.type_genome)
            average, sigma =self.results_manager.both_average_ind(fitnesses, self.type_genome)
            best_id, fitness_best, average_best, sigma_best = self.results_manager.both_average_best(bests, self.type_genome)
            self.results_manager.both_deficient(invalid, self.type_genome)

            generation_id = self.entity_manager.create_entity()
            registry.add_statistic(generation_id, self.generation, average, sigma, best_id, fitness_best, average_best, sigma_best)
            
            self.generation += 1   
        
        else : 
            raise Exception('The type of genome is not supported... Problem with type_genome')



