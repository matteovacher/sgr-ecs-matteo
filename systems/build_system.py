


class BuildSystem :

    def __str__(self) :
        return "BuildSystem"
    
    def __init__(self, config, entity_manager, genome_operator, results_manager, function_pool) :
        self.config = config
        self.entity_manager = entity_manager
        self.genome_operator = genome_operator
        self.results_manager = results_manager
        self.function_pool = function_pool

    def process(self, registry) :

        nodes_by_layer = self.genome_operator.nodes_by_layer(self.config.shape_of_cppn)

        for _ in range(self.config.population) :
            entity_id = self.entity_manager.create_entity()
            connections1, connections2, bias1, bias2, activation_functions1, activation_functions2, dominance1, dominance2, nodes_by_layer = self.genome_operator.generate_first_generation_of_genome(nodes_by_layer, self.function_pool.pool)
            registry.add_genome(entity_id, connections1, connections2, bias1, bias2, activation_functions1, activation_functions2, dominance1, dominance2, nodes_by_layer)
            registry.add_age(entity_id, 1)
        self.results_manager.starting(self.config)

class HaploidBuildSystem() :
    
    def __str__(self) :
        return "BuildHaploidSystem"
    
    def __init__(self, config, entity_manager, genome_operator, results_manager, function_pool) :
        self.config = config
        self.entity_manager = entity_manager
        self.genome_operator = genome_operator
        self.results_manager = results_manager
        self.function_pool = function_pool

    def process(self, registry) :
        nodes_by_layer = self.genome_operator.nodes_by_layer(self.config.shape_of_cppn)

        for _ in range(self.config.population) :
            entity_id = self.entity_manager.create_entity()
            connections, biases, activation_functions, dominances, nodes_by_layer = self.genome_operator.generate_first_generation_of_genome(nodes_by_layer, self.function_pool.pool) 
            registry.add_haploid(entity_id, connections, biases, activation_functions, dominances, nodes_by_layer)
            registry.add_age(entity_id, 1)
        self.results_manager.starting(self.config)


class BothBuildSystem() :
    def __str__(self) :
        return "BuildBothSystem"
    
    def __init__(self, config, entity_manager, genome_operator, results_manager, function_pool, type_genome) :
        self.config = config
        self.entity_manager = entity_manager
        self.genome_operator = genome_operator  
        self.results_manager = results_manager
        self.function_pool = function_pool
        self.type_genome = type_genome

    def process(self, registry) :
        if self.type_genome == 'diploid' :
            nodes_by_layer = self.genome_operator.nodes_by_layer(self.config.shape_of_cppn)

            for _ in range(self.config.population) :
                entity_id = self.entity_manager.create_entity()
                connections1, connections2, bias1, bias2, activation_functions1, activation_functions2, dominance1, dominance2, nodes_by_layer = self.genome_operator.generate_first_generation_of_genome(nodes_by_layer, self.function_pool.pool)
                registry.add_genome(entity_id, connections1, connections2, bias1, bias2, activation_functions1, activation_functions2, dominance1, dominance2, nodes_by_layer)
                registry.add_age(entity_id, 1)
            self.results_manager.starting_both(self.config, self.type_genome)

        elif self.type_genome == 'haploid' :
            nodes_by_layer = self.genome_operator.nodes_by_layer(self.config.shape_of_cppn)

            for _ in range(self.config.population) :
                entity_id = self.entity_manager.create_entity()
                connections, biases, activation_functions, dominances, nodes_by_layer = self.genome_operator.generate_first_generation_of_genome(nodes_by_layer, self.function_pool.pool) 
                registry.add_haploid(entity_id, connections, biases, activation_functions, dominances, nodes_by_layer)
                registry.add_age(entity_id, 1)
            self.results_manager.starting_both(self.config, self.type_genome)
        
        else :
            raise Exception("The type of genome is not valid")
        
    
class BothModularBuildSystem() :
    def __str__(self) :
        return "modular both build system" 
    
    def __init__(self, config, entity_manager, genome_operator, results_manager, function_pool, type_genome) :
        self.config = config
        self.entity_manager = entity_manager
        self.genome_operator = genome_operator  
        self.results_manager = results_manager
        self.function_pool = function_pool
        self.type_genome = type_genome

    def process(self, registry) :
        if self.type_genome == 'diploid' :
            nodes_by_layer = self.genome_operator.nodes_by_layer_with_modu_regu(self.config.shape_of_cppn)

            for _ in range(self.config.population) :
                entity_id = self.entity_manager.create_entity()
                connections1, connections2, bias1, bias2, activation_functions1, activation_functions2, dominance1, dominance2, nodes_by_layer = self.genome_operator.generate_first_generation_of_genome_with_modu_regu(nodes_by_layer, self.function_pool.pool)
                registry.add_genome(entity_id, connections1, connections2, bias1, bias2, activation_functions1, activation_functions2, dominance1, dominance2, nodes_by_layer)
                registry.add_age(entity_id, 1)
            self.results_manager.starting_both(self.config, self.type_genome)

        elif self.type_genome == 'haploid' :
            nodes_by_layer = self.genome_operator.nodes_by_layer_with_modu_regu(self.config.shape_of_cppn)

            for _ in range(self.config.population) :
                entity_id = self.entity_manager.create_entity()
                connections, biases, activation_functions, dominances, nodes_by_layer = self.genome_operator.generate_first_generation_of_genome_with_modu_regu(nodes_by_layer, self.function_pool.pool) 
                registry.add_haploid(entity_id, connections, biases, activation_functions, dominances, nodes_by_layer)
                registry.add_age(entity_id, 1)
            self.results_manager.starting_both(self.config, self.type_genome)
        
        else :
            raise Exception("The type of genome is not valid")

