import math 
import numpy as np

class PhenotypeSystem :

    def __str__(self) :
        return "PhenotypeSystem, build the phenotype from the genome"
    
    def __init__(self, config, entity_manager, genome_operator, network_manager, substrate_builder, phenotype_builder, function_pool, robot_generator, robot_simulator, results_manager) :
        self.generation = 1
        self.config = config 
        self.entity_manager = entity_manager 
        self.genome_operator = genome_operator 
        self.network_manager = network_manager
        self.substrate_builder = substrate_builder 
        self.phenotype_builder = phenotype_builder
        self.function_pool = function_pool
        self.robot_generator = robot_generator
        self.robot_simulator = robot_simulator
        self.results_manager = results_manager

    def process(self, registry) :

        self.results_manager.start_generation(self.generation, self.config)
        self.generation += 1

        entity_ids = [id for id in registry.get_all_id_with_genome() if self.entity_manager.is_alive(id) and registry.has_controller_network(id) == False]
        for entity_id in entity_ids : 
            genome = registry.get_genome(entity_id)
            connections, bias, functions = self.genome_operator.dominance(genome)
            node_evals, input_nodes, output_nodes = self.network_manager.create_network(genome.nodes, connections, bias, functions, sum, response = 1)
            registry.add_cppn(entity_id, node_evals, input_nodes, output_nodes)

            cppn = registry.get_cppn(entity_id)
            body_substrate_shape = self.substrate_builder.extract_body_network_shape(self.config)
            body_substrate = self.substrate_builder.shape_into_coordinates(body_substrate_shape)
            act_func = self.function_pool.pool["tanh"]
            out_act_func = lambda x : x
            node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network(cppn, self.network_manager, body_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias)

            registry.add_body_network(entity_id, node_evals, input_nodes, output_nodes)

            body_network = registry.get_body_network(entity_id)
            robot_grid = self.robot_generator.generate_robot_body_from_network(body_network, self.network_manager, self.config.body_shape)
            if not self.robot_generator.is_valid_robot(robot_grid) :
                fitness, finished  = -1000, True
                registry.add_fitness(entity_id, fitness, finished)
                continue 

            connections = self.robot_generator.get_full_connectivity(robot_grid)
            registry.add_body(entity_id, robot_grid, connections)

            observation_size = self.robot_simulator.get_observation_size(robot_grid)
            grid_input_size = math.ceil(math.sqrt(observation_size))
            controller_substrate_shape = self.substrate_builder.extract_controller_network_shape(grid_input_size, self.config)
            controller_substrate = self.substrate_builder.shape_into_coordinates(controller_substrate_shape)
            node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network(cppn, self.network_manager, controller_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias)
            registry.add_controller_network(entity_id, node_evals, input_nodes, output_nodes)


        # peut etre ici aussi un reporter 


class HaploidPhenotypeSystem : 

    def __str__(self) :
        return "HaploidPhenotypeSystem"
    
    def __init__(self, config, entity_manager, genome_operator, network_manager, substrate_builder, phenotype_builder, function_pool, robot_generator, robot_simulator, results_manager) :
        self.generation = 1
        self.config = config 
        self.entity_manager = entity_manager 
        self.genome_operator = genome_operator 
        self.network_manager = network_manager
        self.substrate_builder = substrate_builder 
        self.phenotype_builder = phenotype_builder
        self.function_pool = function_pool
        self.robot_generator = robot_generator
        self.robot_simulator = robot_simulator
        self.results_manager = results_manager

    def process(self, registry) :

        self.results_manager.start_generation(self.generation, self.config)
        self.generation += 1

        entity_ids = [id for id in registry.get_all_id_with_haploid() if self.entity_manager.is_alive(id) and registry.has_controller_network(id) == False]
        for entity_id in entity_ids : 
            haploid = registry.get_haploid(entity_id)
            node_evals, input_nodes, output_nodes = self.network_manager.create_network(haploid.nodes, haploid.connections, haploid.biases, haploid.functions, sum, response = 1)
            registry.add_cppn(entity_id, node_evals, input_nodes, output_nodes)

            cppn = registry.get_cppn(entity_id)
            body_substrate_shape = self.substrate_builder.extract_body_network_shape(self.config)
            body_substrate = self.substrate_builder.shape_into_coordinates(body_substrate_shape)
            act_func = self.function_pool.pool["tanh"]
            out_act_func = lambda x : x
            node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network(cppn, self.network_manager, body_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias)

            registry.add_body_network(entity_id, node_evals, input_nodes, output_nodes)

            body_network = registry.get_body_network(entity_id)
            robot_grid = self.robot_generator.generate_robot_body_from_network(body_network, self.network_manager, self.config.body_shape)
            if not self.robot_generator.is_valid_robot(robot_grid) :
                fitness, finished  = -1000, True
                registry.add_fitness(entity_id, fitness, finished)
                continue 

            connections = self.robot_generator.get_full_connectivity(robot_grid)
            registry.add_body(entity_id, robot_grid, connections)

            observation_size = self.robot_simulator.get_observation_size(robot_grid)
            grid_input_size = math.ceil(math.sqrt(observation_size))
            controller_substrate_shape = self.substrate_builder.extract_controller_network_shape(grid_input_size, self.config)
            controller_substrate = self.substrate_builder.shape_into_coordinates(controller_substrate_shape)
            node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network(cppn, self.network_manager, controller_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias)
            registry.add_controller_network(entity_id, node_evals, input_nodes, output_nodes)
            

class BothPhenotypeSystem :

    def __str__(self) :
        return "BothPhenotypeSystem, build the phenotype from the genome"
    
    def __init__(self, config, entity_manager, genome_operator, network_manager, substrate_builder, phenotype_builder, function_pool, robot_generator, robot_simulator, results_manager, type_genome ) :
        self.generation = 1
        self.config = config 
        self.entity_manager = entity_manager 
        self.genome_operator = genome_operator 
        self.network_manager = network_manager
        self.substrate_builder = substrate_builder 
        self.phenotype_builder = phenotype_builder
        self.function_pool = function_pool
        self.robot_generator = robot_generator
        self.robot_simulator = robot_simulator
        self.results_manager = results_manager
        self.type_genome = type_genome 

    def process(self, registry) :

        if self.type_genome == 'diploid' :
            self.results_manager.start_both_generation(self.generation, self.config, self.type_genome)
            self.generation += 1

            entity_ids = [id for id in registry.get_all_id_with_genome() if self.entity_manager.is_alive(id) and registry.has_controller_network(id) == False]
            for entity_id in entity_ids : 
                genome = registry.get_genome(entity_id)
                connections, bias, functions = self.genome_operator.dominance(genome)
                node_evals, input_nodes, output_nodes = self.network_manager.create_network(genome.nodes, connections, bias, functions, sum, response = 1)
                registry.add_cppn(entity_id, node_evals, input_nodes, output_nodes)

                cppn = registry.get_cppn(entity_id)
                body_substrate_shape = self.substrate_builder.extract_body_network_shape(self.config)
                body_substrate = self.substrate_builder.shape_into_coordinates(body_substrate_shape)
                act_func = self.function_pool.pool["tanh"]
                out_act_func = lambda x : x
                node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network(cppn, self.network_manager, body_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias)

                registry.add_body_network(entity_id, node_evals, input_nodes, output_nodes)

                body_network = registry.get_body_network(entity_id)
                robot_grid = self.robot_generator.generate_robot_body_from_network(body_network, self.network_manager, self.config.body_shape)
                if not self.robot_generator.is_valid_robot(robot_grid) :
                    fitness, finished  = -1000, True
                    registry.add_fitness(entity_id, fitness, finished)
                    continue 

                connections = self.robot_generator.get_full_connectivity(robot_grid)
                registry.add_body(entity_id, robot_grid, connections)

                observation_size = self.robot_simulator.get_observation_size(robot_grid)
                grid_input_size = math.ceil(math.sqrt(observation_size))
                controller_substrate_shape = self.substrate_builder.extract_controller_network_shape(grid_input_size, self.config)
                controller_substrate = self.substrate_builder.shape_into_coordinates(controller_substrate_shape)
                node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network(cppn, self.network_manager, controller_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias)
                registry.add_controller_network(entity_id, node_evals, input_nodes, output_nodes)
        
        elif self.type_genome == 'haploid' :
            self.results_manager.start_both_generation(self.generation, self.config, self.type_genome )
            self.generation += 1

            entity_ids = [id for id in registry.get_all_id_with_haploid() if self.entity_manager.is_alive(id) and registry.has_controller_network(id) == False]
            for entity_id in entity_ids : 
                haploid = registry.get_haploid(entity_id)
                node_evals, input_nodes, output_nodes = self.network_manager.create_network(haploid.nodes, haploid.connections, haploid.biases, haploid.functions, sum, response = 1)
                registry.add_cppn(entity_id, node_evals, input_nodes, output_nodes)

                cppn = registry.get_cppn(entity_id)
                body_substrate_shape = self.substrate_builder.extract_body_network_shape(self.config)
                body_substrate = self.substrate_builder.shape_into_coordinates(body_substrate_shape)
                act_func = self.function_pool.pool["tanh"]
                out_act_func = lambda x : x
                node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network(cppn, self.network_manager, body_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias)

                registry.add_body_network(entity_id, node_evals, input_nodes, output_nodes)

                body_network = registry.get_body_network(entity_id)
                robot_grid = self.robot_generator.generate_robot_body_from_network(body_network, self.network_manager, self.config.body_shape)
                if not self.robot_generator.is_valid_robot(robot_grid) :
                    fitness, finished  = -1000, True
                    registry.add_fitness(entity_id, fitness, finished)
                    continue 

                connections = self.robot_generator.get_full_connectivity(robot_grid)
                registry.add_body(entity_id, robot_grid, connections)

                observation_size = self.robot_simulator.get_observation_size(robot_grid)
                grid_input_size = math.ceil(math.sqrt(observation_size))
                controller_substrate_shape = self.substrate_builder.extract_controller_network_shape(grid_input_size, self.config)
                controller_substrate = self.substrate_builder.shape_into_coordinates(controller_substrate_shape)
                node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network(cppn, self.network_manager, controller_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias)
                registry.add_controller_network(entity_id, node_evals, input_nodes, output_nodes)

        else :
            raise Exception('The type of genome is not valid')
        
class BothCoPhenotypeSystem :

    def __str__(self) :
        return "BothPhenotypeSystem, build the phenotype from the genome with co dominance "
    
    def __init__(self, config, entity_manager, genome_operator, network_manager, substrate_builder, phenotype_builder, function_pool, robot_generator, robot_simulator, results_manager, type_genome ) :
        self.generation = 1
        self.config = config 
        self.entity_manager = entity_manager 
        self.genome_operator = genome_operator 
        self.network_manager = network_manager
        self.substrate_builder = substrate_builder 
        self.phenotype_builder = phenotype_builder
        self.function_pool = function_pool
        self.robot_generator = robot_generator
        self.robot_simulator = robot_simulator
        self.results_manager = results_manager
        self.type_genome = type_genome 

    def process(self, registry) :

        if self.type_genome == 'diploid' :
            self.results_manager.start_both_generation(self.generation, self.config, self.type_genome)
            self.generation += 1

            entity_ids = [id for id in registry.get_all_id_with_genome() if self.entity_manager.is_alive(id) and registry.has_controller_network(id) == False]
            for entity_id in entity_ids : 
                genome = registry.get_genome(entity_id)
                connections, bias, functions = self.genome_operator.codominance(genome)
                node_evals, input_nodes, output_nodes = self.network_manager.create_network(genome.nodes, connections, bias, functions, sum, response = 1)
                registry.add_cppn(entity_id, node_evals, input_nodes, output_nodes)

                cppn = registry.get_cppn(entity_id)
                body_substrate_shape = self.substrate_builder.extract_body_network_shape(self.config)
                body_substrate = self.substrate_builder.shape_into_coordinates(body_substrate_shape)
                act_func = self.function_pool.pool["tanh"]
                out_act_func = lambda x : x
                node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network(cppn, self.network_manager, body_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias)

                registry.add_body_network(entity_id, node_evals, input_nodes, output_nodes)

                body_network = registry.get_body_network(entity_id)
                robot_grid = self.robot_generator.generate_robot_body_from_network(body_network, self.network_manager, self.config.body_shape)
                if not self.robot_generator.is_valid_robot(robot_grid) :
                    fitness, finished  = -1000, True
                    registry.add_fitness(entity_id, fitness, finished)
                    continue 

                connections = self.robot_generator.get_full_connectivity(robot_grid)
                registry.add_body(entity_id, robot_grid, connections)

                observation_size = self.robot_simulator.get_observation_size(robot_grid)
                grid_input_size = math.ceil(math.sqrt(observation_size))
                controller_substrate_shape = self.substrate_builder.extract_controller_network_shape(grid_input_size, self.config)
                controller_substrate = self.substrate_builder.shape_into_coordinates(controller_substrate_shape)
                node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network(cppn, self.network_manager, controller_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias)
                registry.add_controller_network(entity_id, node_evals, input_nodes, output_nodes)
        
        elif self.type_genome == 'haploid' :
            self.results_manager.start_both_generation(self.generation, self.config, self.type_genome )
            self.generation += 1

            entity_ids = [id for id in registry.get_all_id_with_haploid() if self.entity_manager.is_alive(id) and registry.has_controller_network(id) == False]
            for entity_id in entity_ids : 
                haploid = registry.get_haploid(entity_id)
                node_evals, input_nodes, output_nodes = self.network_manager.create_network(haploid.nodes, haploid.connections, haploid.biases, haploid.functions, sum, response = 1)
                registry.add_cppn(entity_id, node_evals, input_nodes, output_nodes)

                cppn = registry.get_cppn(entity_id)
                body_substrate_shape = self.substrate_builder.extract_body_network_shape(self.config)
                body_substrate = self.substrate_builder.shape_into_coordinates(body_substrate_shape)
                act_func = self.function_pool.pool["tanh"]
                out_act_func = lambda x : x
                node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network(cppn, self.network_manager, body_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias)

                registry.add_body_network(entity_id, node_evals, input_nodes, output_nodes)

                body_network = registry.get_body_network(entity_id)
                robot_grid = self.robot_generator.generate_robot_body_from_network(body_network, self.network_manager, self.config.body_shape)
                if not self.robot_generator.is_valid_robot(robot_grid) :
                    fitness, finished  = -1000, True
                    registry.add_fitness(entity_id, fitness, finished)
                    continue 

                connections = self.robot_generator.get_full_connectivity(robot_grid)
                registry.add_body(entity_id, robot_grid, connections)

                observation_size = self.robot_simulator.get_observation_size(robot_grid)
                grid_input_size = math.ceil(math.sqrt(observation_size))
                controller_substrate_shape = self.substrate_builder.extract_controller_network_shape(grid_input_size, self.config)
                controller_substrate = self.substrate_builder.shape_into_coordinates(controller_substrate_shape)
                node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network(cppn, self.network_manager, controller_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias)
                registry.add_controller_network(entity_id, node_evals, input_nodes, output_nodes)

        else :
            raise Exception('The type of genome is not valid')
        
class BothEnvPhenotypeSystem() :

    def __str__(self) :
        return "BothEnvPhenotypeSystem, build the phenotype from the genome, depending on the environment"

    def __init__(self, config, entity_manager, genome_operator, network_manager, substrate_builder, phenotype_builder, function_pool, robot_generator, robot_simulator, results_manager, type_genome, type_env) :
        self.generation = 1
        self.config = config 
        self.entity_manager = entity_manager 
        self.genome_operator = genome_operator 
        self.network_manager = network_manager
        self.substrate_builder = substrate_builder 
        self.phenotype_builder = phenotype_builder
        self.function_pool = function_pool
        self.robot_generator = robot_generator
        self.robot_simulator = robot_simulator
        self.results_manager = results_manager
        self.type_genome = type_genome
        self.type_env = type_env # is 0 or 1 to access config.env_name
        self.switched = False 

    def process(self, registry) :

        
        if self.type_genome == 'diploid' :
            self.results_manager.start_both_env_generation(self.generation, self.config, self.type_genome, self.type_env)
            self.generation += 1

            if self.switched : 
                entity_ids = [id for id in registry.get_all_id_with_genome() if self.entity_manager.is_alive(id)]
            else : 
                entity_ids = [id for id in registry.get_all_id_with_genome() if self.entity_manager.is_alive(id) and registry.has_controller_network(id) == False]

            for entity_id in entity_ids : 
                genome = registry.get_genome(entity_id)
                connections, bias, functions = self.genome_operator.dominance(genome)
                node_evals, input_nodes, output_nodes = self.network_manager.create_network(genome.nodes, connections, bias, functions, sum, response = 1)
                registry.add_cppn(entity_id, node_evals, input_nodes, output_nodes)

                cppn = registry.get_cppn(entity_id)
                body_substrate_shape = self.substrate_builder.extract_body_network_shape(self.config)
                body_substrate = self.substrate_builder.shape_into_coordinates(body_substrate_shape)
                act_func = self.function_pool.pool["tanh"]
                out_act_func = lambda x : x
                node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network(cppn, self.network_manager, body_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias)

                registry.add_body_network(entity_id, node_evals, input_nodes, output_nodes)

                body_network = registry.get_body_network(entity_id)
                robot_grid = self.robot_generator.generate_robot_body_from_network_and_env(body_network, self.network_manager, self.config.body_shape, self.type_env)
                if not self.robot_generator.is_valid_robot(robot_grid) :
                    fitness, finished  = -1000, True
                    registry.add_fitness(entity_id, fitness, finished)
                    if registry.has_controller_network(entity_id) :
                        registry.controller_network_registry.pop(entity_id)
                    continue 

                connections = self.robot_generator.get_full_connectivity(robot_grid)
                registry.add_body(entity_id, robot_grid, connections)

                observation_size = self.robot_simulator.get_observation_size_mode_env(robot_grid, self.type_env)
                grid_input_size = math.ceil(math.sqrt(observation_size))
                controller_substrate_shape = self.substrate_builder.extract_controller_network_shape(grid_input_size, self.config)
                controller_substrate = self.substrate_builder.shape_into_coordinates(controller_substrate_shape)
                node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network(cppn, self.network_manager, controller_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias)
                registry.add_controller_network(entity_id, node_evals, input_nodes, output_nodes)
        
        elif self.type_genome == 'haploid' :
            self.results_manager.start_both_env_generation(self.generation, self.config, self.type_genome, self.type_env) 
            self.generation += 1

            if self.switched : 
                entity_ids = [id for id in registry.get_all_id_with_haploid() if self.entity_manager.is_alive(id)]
            else : 
                entity_ids = [id for id in registry.get_all_id_with_haploid() if self.entity_manager.is_alive(id) and registry.has_controller_network(id) == False]

            for entity_id in entity_ids : 
                haploid = registry.get_haploid(entity_id)
                node_evals, input_nodes, output_nodes = self.network_manager.create_network(haploid.nodes, haploid.connections, haploid.biases, haploid.functions, sum, response = 1)
                registry.add_cppn(entity_id, node_evals, input_nodes, output_nodes)

                cppn = registry.get_cppn(entity_id)
                body_substrate_shape = self.substrate_builder.extract_body_network_shape(self.config)
                body_substrate = self.substrate_builder.shape_into_coordinates(body_substrate_shape)
                act_func = self.function_pool.pool["tanh"]
                out_act_func = lambda x : x
                node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network(cppn, self.network_manager, body_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias)

                registry.add_body_network(entity_id, node_evals, input_nodes, output_nodes)

                body_network = registry.get_body_network(entity_id)
                robot_grid = self.robot_generator.generate_robot_body_from_network_and_env(body_network, self.network_manager, self.config.body_shape, self.type_env)
                if not self.robot_generator.is_valid_robot(robot_grid) :
                    fitness, finished  = -1000, True
                    registry.add_fitness(entity_id, fitness, finished)
                    if registry.has_controller_network(entity_id) :
                        registry.controller_network_registry.pop(entity_id)
                    continue 

                connections = self.robot_generator.get_full_connectivity(robot_grid)
                registry.add_body(entity_id, robot_grid, connections)

                observation_size = self.robot_simulator.get_observation_size_mode_env(robot_grid, self.type_env)
                grid_input_size = math.ceil(math.sqrt(observation_size))
                controller_substrate_shape = self.substrate_builder.extract_controller_network_shape(grid_input_size, self.config)
                controller_substrate = self.substrate_builder.shape_into_coordinates(controller_substrate_shape)
                node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network(cppn, self.network_manager, controller_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias)
                registry.add_controller_network(entity_id, node_evals, input_nodes, output_nodes)

        else :
            raise Exception('The type of genome is not valid')
        


class BothCoEnvPhenotypeSystem() :

    def __str__(self) :
        return "BothEnvPhenotypeSystem, build the phenotype from the genome, depending on the environment with co dominance"

    def __init__(self, config, entity_manager, genome_operator, network_manager, substrate_builder, phenotype_builder, function_pool, robot_generator, robot_simulator, results_manager, type_genome, type_env) :
        self.generation = 1
        self.config = config 
        self.entity_manager = entity_manager 
        self.genome_operator = genome_operator 
        self.network_manager = network_manager
        self.substrate_builder = substrate_builder 
        self.phenotype_builder = phenotype_builder
        self.function_pool = function_pool
        self.robot_generator = robot_generator
        self.robot_simulator = robot_simulator
        self.results_manager = results_manager
        self.type_genome = type_genome
        self.type_env = type_env # is 0 or 1 to access config.env_name
        self.switched = False 

    def process(self, registry) :

        
        if self.type_genome == 'diploid' :
            self.results_manager.start_both_env_generation(self.generation, self.config, self.type_genome, self.type_env)
            self.generation += 1

            if self.switched : 
                entity_ids = [id for id in registry.get_all_id_with_genome() if self.entity_manager.is_alive(id)]
            else : 
                entity_ids = [id for id in registry.get_all_id_with_genome() if self.entity_manager.is_alive(id) and registry.has_controller_network(id) == False]

            for entity_id in entity_ids : 
                genome = registry.get_genome(entity_id)
                connections, bias, functions = self.genome_operator.codominance(genome)
                node_evals, input_nodes, output_nodes = self.network_manager.create_network(genome.nodes, connections, bias, functions, sum, response = 1)
                registry.add_cppn(entity_id, node_evals, input_nodes, output_nodes)

                cppn = registry.get_cppn(entity_id)
                body_substrate_shape = self.substrate_builder.extract_body_network_shape(self.config)
                body_substrate = self.substrate_builder.shape_into_coordinates(body_substrate_shape)
                act_func = self.function_pool.pool["tanh"]
                out_act_func = lambda x : x
                node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network(cppn, self.network_manager, body_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias)

                registry.add_body_network(entity_id, node_evals, input_nodes, output_nodes)

                body_network = registry.get_body_network(entity_id)
                robot_grid = self.robot_generator.generate_robot_body_from_network_and_env(body_network, self.network_manager, self.config.body_shape, self.type_env)
                if not self.robot_generator.is_valid_robot(robot_grid) :
                    fitness, finished  = -1000, True
                    registry.add_fitness(entity_id, fitness, finished)
                    if registry.has_controller_network(entity_id) :
                        registry.controller_network_registry.pop(entity_id)
                    continue 

                connections = self.robot_generator.get_full_connectivity(robot_grid)
                registry.add_body(entity_id, robot_grid, connections)

                observation_size = self.robot_simulator.get_observation_size_mode_env(robot_grid, self.type_env)
                grid_input_size = math.ceil(math.sqrt(observation_size))
                controller_substrate_shape = self.substrate_builder.extract_controller_network_shape(grid_input_size, self.config)
                controller_substrate = self.substrate_builder.shape_into_coordinates(controller_substrate_shape)
                node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network(cppn, self.network_manager, controller_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias)
                registry.add_controller_network(entity_id, node_evals, input_nodes, output_nodes)
        
        elif self.type_genome == 'haploid' :
            self.results_manager.start_both_env_generation(self.generation, self.config, self.type_genome, self.type_env) 
            self.generation += 1

            if self.switched : 
                entity_ids = [id for id in registry.get_all_id_with_haploid() if self.entity_manager.is_alive(id)]
            else : 
                entity_ids = [id for id in registry.get_all_id_with_haploid() if self.entity_manager.is_alive(id) and registry.has_controller_network(id) == False]

            for entity_id in entity_ids : 
                haploid = registry.get_haploid(entity_id)
                node_evals, input_nodes, output_nodes = self.network_manager.create_network(haploid.nodes, haploid.connections, haploid.biases, haploid.functions, sum, response = 1)
                registry.add_cppn(entity_id, node_evals, input_nodes, output_nodes)

                cppn = registry.get_cppn(entity_id)
                body_substrate_shape = self.substrate_builder.extract_body_network_shape(self.config)
                body_substrate = self.substrate_builder.shape_into_coordinates(body_substrate_shape)
                act_func = self.function_pool.pool["tanh"]
                out_act_func = lambda x : x
                node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network(cppn, self.network_manager, body_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias)

                registry.add_body_network(entity_id, node_evals, input_nodes, output_nodes)

                body_network = registry.get_body_network(entity_id)
                robot_grid = self.robot_generator.generate_robot_body_from_network_and_env(body_network, self.network_manager, self.config.body_shape, self.type_env)
                if not self.robot_generator.is_valid_robot(robot_grid) :
                    fitness, finished  = -1000, True
                    registry.add_fitness(entity_id, fitness, finished)
                    if registry.has_controller_network(entity_id) :
                        registry.controller_network_registry.pop(entity_id)
                    continue 

                connections = self.robot_generator.get_full_connectivity(robot_grid)
                registry.add_body(entity_id, robot_grid, connections)

                observation_size = self.robot_simulator.get_observation_size_mode_env(robot_grid, self.type_env)
                grid_input_size = math.ceil(math.sqrt(observation_size))
                controller_substrate_shape = self.substrate_builder.extract_controller_network_shape(grid_input_size, self.config)
                controller_substrate = self.substrate_builder.shape_into_coordinates(controller_substrate_shape)
                node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network(cppn, self.network_manager, controller_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias)
                registry.add_controller_network(entity_id, node_evals, input_nodes, output_nodes)

        else :
            raise Exception('The type of genome is not valid')
        


class BothCo2WiBiPhenotypeSystem :

    def __str__(self) :
        return "BothPhenotypeSystem, build the phenotype from the genome with co dominance, with 2 outputs, without biases and with other logical rules "
    
    def __init__(self, config, entity_manager, genome_operator, network_manager, substrate_builder, phenotype_builder, function_pool, robot_generator, robot_simulator, results_manager, type_genome ) :
        self.generation = 1
        self.config = config 
        self.entity_manager = entity_manager 
        self.genome_operator = genome_operator 
        self.network_manager = network_manager
        self.substrate_builder = substrate_builder 
        self.phenotype_builder = phenotype_builder
        self.function_pool = function_pool
        self.robot_generator = robot_generator
        self.robot_simulator = robot_simulator
        self.results_manager = results_manager
        self.type_genome = type_genome 

    def process(self, registry) :

        if self.type_genome == 'diploid' :
            self.results_manager.start_both_generation(self.generation, self.config, self.type_genome)
            self.generation += 1

            entity_ids = [id for id in registry.get_all_id_with_genome() if self.entity_manager.is_alive(id) and registry.has_controller_network(id) == False]
            for entity_id in entity_ids : 
                genome = registry.get_genome(entity_id)
                connections, bias, functions = self.genome_operator.codominance(genome)
                node_evals, input_nodes, output_nodes = self.network_manager.create_network(genome.nodes, connections, bias, functions, sum, response = 1)
                registry.add_cppn(entity_id, node_evals, input_nodes, output_nodes)

                cppn = registry.get_cppn(entity_id)
                body_substrate_shape = self.substrate_builder.extract_body_network_shape(self.config)
                body_substrate = self.substrate_builder.shape_into_coordinates(body_substrate_shape)
                act_func = self.function_pool.pool["tanh"]
                out_act_func = lambda x : x
                node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network_without_bias_2_outputs(cppn, self.network_manager, body_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias, type_output = 0)

                registry.add_body_network(entity_id, node_evals, input_nodes, output_nodes)

                body_network = registry.get_body_network(entity_id)
                robot_grid = self.robot_generator.generate_robot_body_from_network(body_network, self.network_manager, self.config.body_shape)
                if not self.robot_generator.is_valid_robot(robot_grid) :
                    fitness, finished  = -1000, True
                    registry.add_fitness(entity_id, fitness, finished)
                    continue 

                connections = self.robot_generator.get_full_connectivity(robot_grid)
                registry.add_body(entity_id, robot_grid, connections)

                observation_size = self.robot_simulator.get_observation_size(robot_grid)
                grid_input_size = math.ceil(math.sqrt(observation_size))
                controller_substrate_shape = self.substrate_builder.extract_controller_network_shape(grid_input_size, self.config)
                controller_substrate = self.substrate_builder.shape_into_coordinates(controller_substrate_shape)
                node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network_without_bias_2_outputs(cppn, self.network_manager, controller_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias, type_output = 1)
                registry.add_controller_network(entity_id, node_evals, input_nodes, output_nodes)
        
        elif self.type_genome == 'haploid' :
            self.results_manager.start_both_generation(self.generation, self.config, self.type_genome )
            self.generation += 1

            entity_ids = [id for id in registry.get_all_id_with_haploid() if self.entity_manager.is_alive(id) and registry.has_controller_network(id) == False]
            for entity_id in entity_ids : 
                haploid = registry.get_haploid(entity_id)
                node_evals, input_nodes, output_nodes = self.network_manager.create_network(haploid.nodes, haploid.connections, haploid.biases, haploid.functions, sum, response = 1)
                registry.add_cppn(entity_id, node_evals, input_nodes, output_nodes)

                cppn = registry.get_cppn(entity_id)
                body_substrate_shape = self.substrate_builder.extract_body_network_shape(self.config)
                body_substrate = self.substrate_builder.shape_into_coordinates(body_substrate_shape)
                act_func = self.function_pool.pool["tanh"]
                out_act_func = lambda x : x
                node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network_without_bias_2_outputs(cppn, self.network_manager, body_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias, type_output = 0)

                registry.add_body_network(entity_id, node_evals, input_nodes, output_nodes)

                body_network = registry.get_body_network(entity_id)
                robot_grid = self.robot_generator.generate_robot_body_from_network(body_network, self.network_manager, self.config.body_shape)
                if not self.robot_generator.is_valid_robot(robot_grid) :
                    fitness, finished  = -1000, True
                    registry.add_fitness(entity_id, fitness, finished)
                    continue 

                connections = self.robot_generator.get_full_connectivity(robot_grid)
                registry.add_body(entity_id, robot_grid, connections)

                observation_size = self.robot_simulator.get_observation_size(robot_grid)
                grid_input_size = math.ceil(math.sqrt(observation_size))
                controller_substrate_shape = self.substrate_builder.extract_controller_network_shape(grid_input_size, self.config)
                controller_substrate = self.substrate_builder.shape_into_coordinates(controller_substrate_shape)
                node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network_without_bias_2_outputs(cppn, self.network_manager, controller_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias, type_output = 1)
                registry.add_controller_network(entity_id, node_evals, input_nodes, output_nodes)

        else :
            raise Exception('The type of genome is not valid')
        


class BothModularCo2WiBiPhenotypeSystem :

    def __str__(self) :
        return "Modular BothPhenotypeSystem, build the phenotype from the genome with co dominance, with 2 outputs, without biases and with other logical rules "
    
    def __init__(self, config, entity_manager, genome_operator, network_manager, substrate_builder, phenotype_builder, function_pool, robot_generator, robot_simulator, results_manager, type_genome ) :
        self.generation = 1
        self.config = config 
        self.entity_manager = entity_manager 
        self.genome_operator = genome_operator 
        self.network_manager = network_manager
        self.substrate_builder = substrate_builder 
        self.phenotype_builder = phenotype_builder
        self.function_pool = function_pool
        self.robot_generator = robot_generator
        self.robot_simulator = robot_simulator
        self.results_manager = results_manager
        self.type_genome = type_genome 

    def process(self, registry) :

        if self.type_genome == 'diploid' :
            self.results_manager.start_both_generation(self.generation, self.config, self.type_genome)
            self.generation += 1

            entity_ids = [id for id in registry.get_all_id_with_genome() if self.entity_manager.is_alive(id) and registry.has_controller_network(id) == False]
            for entity_id in entity_ids : 
                genome = registry.get_genome(entity_id)
                connections, bias, functions = self.genome_operator.codominance_with_modu_regu(genome)
                node_evals, input_nodes, output_nodes = self.network_manager.create_network_with_modu_regu(genome.nodes, connections, bias, functions, sum, response = 1)
                registry.add_cppn(entity_id, node_evals, input_nodes, output_nodes)

                cppn = registry.get_cppn(entity_id)
                body_substrate_shape = self.substrate_builder.extract_body_network_shape(self.config)
                body_substrate = self.substrate_builder.shape_into_coordinates(body_substrate_shape)
                act_func = np.tanh
                out_act_func = np.tanh
                node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network_without_bias_2_outputs(cppn, self.network_manager, body_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias, type_output = 0)

                registry.add_body_network(entity_id, node_evals, input_nodes, output_nodes)

                body_network = registry.get_body_network(entity_id)
                robot_grid = self.robot_generator.generate_robot_body_from_network(body_network, self.network_manager, self.config.body_shape)
                if not self.robot_generator.is_valid_robot(robot_grid) :
                    fitness, finished  = -1000, True
                    registry.add_fitness(entity_id, fitness, finished)
                    continue 

                connections = self.robot_generator.get_full_connectivity(robot_grid)
                registry.add_body(entity_id, robot_grid, connections)

                out_act_func = lambda x : 0.5*np.tanh(x) + 1.1
                observation_size = self.robot_simulator.get_observation_size(robot_grid)
                grid_input_size = math.ceil(math.sqrt(observation_size))
                controller_substrate_shape = self.substrate_builder.extract_controller_network_shape(grid_input_size, self.config)
                controller_substrate = self.substrate_builder.shape_into_coordinates(controller_substrate_shape)
                node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network_without_bias_2_outputs(cppn, self.network_manager, controller_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias, type_output = 1)
                registry.add_controller_network(entity_id, node_evals, input_nodes, output_nodes)
        
        elif self.type_genome == 'haploid' :
            self.results_manager.start_both_generation(self.generation, self.config, self.type_genome )
            self.generation += 1

            entity_ids = [id for id in registry.get_all_id_with_haploid() if self.entity_manager.is_alive(id) and registry.has_controller_network(id) == False]
            for entity_id in entity_ids : 
                haploid = registry.get_haploid(entity_id)
                node_evals, input_nodes, output_nodes = self.network_manager.create_network_with_modu_regu(haploid.nodes, haploid.connections, haploid.biases, haploid.functions, sum, response = 1)
                registry.add_cppn(entity_id, node_evals, input_nodes, output_nodes)

                cppn = registry.get_cppn(entity_id)
                body_substrate_shape = self.substrate_builder.extract_body_network_shape(self.config)
                body_substrate = self.substrate_builder.shape_into_coordinates(body_substrate_shape)
                act_func = np.tanh
                out_act_func = np.tanh
                node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network_without_bias_2_outputs(cppn, self.network_manager, body_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias, type_output = 0)

                registry.add_body_network(entity_id, node_evals, input_nodes, output_nodes)

                body_network = registry.get_body_network(entity_id)
                robot_grid = self.robot_generator.generate_robot_body_from_network(body_network, self.network_manager, self.config.body_shape)
                if not self.robot_generator.is_valid_robot(robot_grid) :
                    fitness, finished  = -1000, True
                    registry.add_fitness(entity_id, fitness, finished)
                    continue 

                connections = self.robot_generator.get_full_connectivity(robot_grid)
                registry.add_body(entity_id, robot_grid, connections)

                out_act_func = lambda x : 0.5*np.tanh(x) + 1.1
                observation_size = self.robot_simulator.get_observation_size(robot_grid)
                grid_input_size = math.ceil(math.sqrt(observation_size))
                controller_substrate_shape = self.substrate_builder.extract_controller_network_shape(grid_input_size, self.config)
                controller_substrate = self.substrate_builder.shape_into_coordinates(controller_substrate_shape)
                node_evals, input_nodes, output_nodes = self.phenotype_builder.create_phenotype_network_without_bias_2_outputs(cppn, self.network_manager, controller_substrate, act_func, out_act_func, sum, self.config.response, self.config.max_weight, self.config.max_bias, type_output = 1)
                registry.add_controller_network(entity_id, node_evals, input_nodes, output_nodes)

        else :
            raise Exception('The type of genome is not valid')