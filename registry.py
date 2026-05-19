
from components import *

class ComponentRegistry :
    def __init__(self) :
        self.chromosome1_registry = {}
        self.chromosome2_registry = {}
        self.fitness_registry = {}
        self.cppn_registry = {}
        self.body_network_registry = {}
        self.controller_network_registry = {}
        self.body_registry = {}


    # ADDER METHODS 
    def add_chromosome1(self, entity_id, connections1, connections2, nodes) :
        self.chromosome1_registry[entity_id] = Chromosome1Component(connections1, connections2, nodes)

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


    def add_body(self, entity_id,  body) :
        self.body_registry [entity_id] = BodyComponent(body)

    # GETTER METHODS 
    def get_chromosome1(self, entity_id) :
        return self.chromosome1_registry[entity_id]
    
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
    
    # ADVANCED GETTER METHODS
    def get_all_id_with_chromosome1(self) :
        return self.chromosome1_registry.keys()
    
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
    
    # CLEARER METHODS 
    def clear_all(self) :
        for key, _  in self.__dict__.items():
            self[key].clear()

    # MODIFYERS please give an object 
    def modify_chromosome1(self, entity_id, other_chromosome1):
        self.chromosome1_registry[entity_id] = other_chromosome1









