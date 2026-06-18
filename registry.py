import copy
from components import *

class ComponentRegistry :
    def __init__(self) :
        self.genome_registry = {}
        self.chromosome2_registry = {}
        self.fitness_registry = {}
        self.cppn_registry = {}
        self.body_network_registry = {}
        self.controller_network_registry = {}
        self.body_registry = {}
        self.tosave_registry = {}
        self.generation_registry = {}
        self.age_registry = {}
        self.statistic_registry = {}
        self.parents_registry = {}
        self.haploid_registry = {}
        self.haploid_parents_registry = {}

    # ADDER METHODS 
    def add_genome(self, entity_id, connections1, connections2, bias1, bias2, function1, function2, dominance1, dominance2, nodes) :
        self.genome_registry[entity_id] = GenomeComponent(connections1, connections2, bias1, bias2, function1, function2, dominance1, dominance2, nodes)
        
    def add_haploid(self, entity_id, connections, biases, functions, dominances, nodes) : 
        self.haploid_registry[entity_id] = HaploidComponent(connections, biases, functions, dominances, nodes)

    def add_chromosome2(self, entity_id, sex1, sex2):
        self.chromosome2_registry[entity_id] = Chromosome2Component(sex1, sex2)      
        
    def add_fitness(self, entity_id, fitness, finished) :
        self.fitness_registry[entity_id] = FitnessComponent(fitness, finished)

    def add_cppn(self, entity_id, node_evals, input_nodes, output_nodes) :
        self.cppn_registry[entity_id] = CPPNComponent(node_evals, input_nodes, output_nodes)

    def add_controller_network(self, entity_id, node_evals, input_nodes, output_nodes) :
        self.controller_network_registry[entity_id] = ControllerNetworkComponent(node_evals, input_nodes, output_nodes)

    def add_body_network(self, entity_id, node_evals, input_nodes, output_nodes) :
        self.body_network_registry[entity_id] = BodyNetworkComponent(node_evals, input_nodes, output_nodes)

    def add_body(self, entity_id,  body, connections) :
        self.body_registry [entity_id] = BodyComponent(body, connections)

    def add_tosave(self, generation, entity_id, tosave ) :
        self.tosave_registry[(generation, entity_id)] = TosaveComponent(tosave)

    def add_generation(self, entity_id, generation) :
        self.generation_registry[entity_id] = GenerationComponent(generation)

    def add_age(self, entity_id, age) :
        self.age_registry[entity_id] = AgeComponent(age)

    def add_statistic(self, entity_id, generation, average, std, best, fitness, average_best, std_best) :
        self.statistic_registry[entity_id] = StatisticComponent(generation, average, std, best, fitness, average_best, std_best)

    def add_parents(self, entity_id, parent1, parent2, choice1, choice2) :
        self.parents_registry[entity_id] = ParentsComponent(parent1, parent2, choice1, choice2)

    def add_haploid_parents(self, entity_id, parent1, parent2) :
        self.haploid_parents_registry[entity_id] = HaploidParentsComponent(parent1, parent2)

    # GETTER METHODS 
    def get_genome(self, entity_id) :
        return self.genome_registry[entity_id]
    
    def get_haploid(self, entity_id) :
        return self.haploid_registry[entity_id]

    def get_chromosome2(self, entity_id):
        return self.chromosome2_registry[entity_id]
    
    def get_fitness(self, entity_id) :
        return self.fitness_registry[entity_id]
    
    def get_cppn(self, entity_id) :
        return self.cppn_registry[entity_id]
    
    def get_controller_network(self, entity_id) :
        return self.controller_network_registry[entity_id]
    
    def get_body_network(self, entity_id) :
        return self.body_network_registry[entity_id]
    
    def get_body(self, entity_id) :
        return self.body_registry[entity_id]
    
    def get_tosave(self, generation, entity_id) :
        return self.tosave_registry[(generation,entity_id)]
    
    def get_generation(self, entity_id) :
        return self.generation_registry[entity_id]
    
    def get_age(self, entity_id) :
        return self.age_registry[entity_id]

    def get_statistic(self, entity_id) :
        return self.statistic_registry[entity_id]
    
    def get_parents(self, entity_id) :
        return self.parents_registry[entity_id]

    def get_haploid_parents(self, entity_id) :
        return self.haploid_parents_registry[entity_id]


    # ADVANCED GETTER METHODS
    def get_all_id_with_genome(self) :
        return self.genome_registry.keys()

    def get_all_id_with_haploid(self) :
        return self.haploid_registry.keys()

    def get_all_id_with_chromosome2(self):
        return self.chromosome2_registry.keys()
    
    def get_all_id_with_fitness(self) :
        return self.fitness_registry.keys()
    
    def get_all_id_with_controller_network(self) :
        return self.controller_network_registry.keys()
    
    def get_all_id_with_body_network(self) :
        return self.body_network_registry.keys()
    
    def get_all_id_with_body(self) :
        return self.body_registry.keys()
    
    def get_all_id_with_tosave(self) :
        return self.tosave_registry.keys()
    
    def get_all_id_with_statistic(self) :
        return self.statistic_registry.keys()    
    # HAS METHODS
    def has_controller_network(self, entity_id) :
        return entity_id in self.controller_network_registry
    

    # CLEARER METHODS 
    def clear_all(self):
        for registry in self.__dict__.values() :
            registry.clear()

    def clear_ind_from_registry(self , entity_id) :
        for registry in self.__dict__.values() :
            registry.pop(entity_id, None)
    
    def clear_save_from_registry(self, generation, entity_id) :
        for registry in self.__dict__.values() :
            registry.pop((generation, entity_id), None)


    # MODIFYERS please give an object 
    def modify_genome(self, entity_id, other_genome):
        self.genome_registry[entity_id] = other_genome

    def modify_haploid(self, entity_id, other_haploid) :
        self.haploid_registry[entity_id] = other_haploid 

    def modify_age(self, entity_id, age) :
        self.age_registry[entity_id] = AgeComponent(age)


    # OTHER METHODS
    def snapshot(self, generation, entity_id) :
        key = (generation, entity_id)
        for registry in self.__dict__.values() :
            if entity_id in registry :
                registry[key] = copy.deepcopy(registry[entity_id])







