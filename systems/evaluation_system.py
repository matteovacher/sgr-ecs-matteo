import numpy as np 


class EvaluationSystem :

    def __str__(self) :
        return "EvaluationSystem, evaluate all individuals"
    

    def __init__(self, config, robot_simulator, network_manager, parallel_tool) :
        self.generation = 1
        self.config = config 
        self.robot_simulator = robot_simulator 
        self.network_manager = network_manager 
        self.parallel_tool = parallel_tool 


    def process(self, registry ) :
        
        self.generation += 1

        entity_ids = [id for id in registry.get_all_id_with_genome() if self.entity_manager.is_alive(id) and registry.get_controller(id) is not None]
        controllers = []
        bodies = []


        for entity_id in entity_ids :
            controller = registry.get_controller(entity_id)
            body = registry.get_body(entity_id)
            controllers.append(controller)
            bodies.append(body)
            controllers.append(controller)
        
        function = self.robot_simulator.simulate

        chunk = list(zip(entity_ids, bodies, controllers, self.config.n_steps, self.network_manager))
        results = self.parallel_tool.run(function, chunk)

        fitnesses = []
        ids = []
        for entity_id, fitness, finished in results :
            ids.append(entity_id)
            fitnesses.append(fitness)
            registry.add_fitness(entity_id, fitness, finished)


        fitnesses = np.array(fitnesses)
        arg_sorted_fitnesses = np.argsort(fitnesses)
        bests = []
        number_of_reported_individuals = self.config.number_of_reported_individuals
        for taken in range(number_of_reported_individuals) : 
            id = arg_sorted_fitnesses[len(entity_ids) - 1 - taken]
            bests.append((ids[id], fitnesses[id]))
        
        invalid = self.config.population - len(entity_ids)

        # ici rajouter ensuite les individus qui sont invalide et faire les reports 


        
