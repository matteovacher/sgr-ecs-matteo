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
        number_to_report = min(number_of_reported_individuals, len(entity_ids))
        for taken in range(number_to_report) : 
            id = arg_sorted_fitnesses[len(entity_ids) - 1 - taken]
            bests.append((ids[id], fitnesses[id]))
        
        invalid = self.config.population - len(entity_ids)

        self.results_manager.bests(bests)
        self.results_manager.average_ind(fitnesses)
        self.results_manager.deficient(invalid)

        # ici rajouter ensuite les individus qui sont invalide et faire les reports 


        
