


class BuildSystem :

    def __str__(self) :
        return "BuildSystem"
    
    def __init__(self, config, entity_manager, genome_operator, results_manager) :
        self.config = config
        self.entity_manager = entity_manager
        self.genome_operator = genome_operator
        self.results_manager = results_manager

    def process(self, registry) :

        nodes_by_layer = self.genome_operator.nodes_by_layer(self.config.shape_of_cppn)

        for _ in range(self.config.population) :
            entity_id = self.entity_manager.create_entity()
            connections1, connections2, bias1, bias2, activation_functions1, activation_functions2, dominance1, dominance2, nodes_by_layer = self.genome_operator.generate_first_generation_of_genome(nodes_by_layer)
            registry.add_genome(entity_id, connections1, connections2, bias1, bias2, activation_functions1, activation_functions2, dominance1, dominance2, nodes_by_layer)

        self.results_manager.starting(self.config)


        