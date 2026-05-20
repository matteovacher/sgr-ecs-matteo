


class GenomeComponent : 

    def __init__(self, connections1, connections2, bias1, bias2, function1, function2, dominance1, dominance2, nodes) :
        self.connections = [connections1, connections2]
        self.biases = [bias1, bias2]
        self.functions = [function1, function2]
        self.dominances =[dominance1, dominance2]
        self.nodes = nodes 

class Chromosome2Component:
    
    def __init__(self, sex1, sex2) :
        self.sexs = [sex1, sex2]


class FitnessComponent :

    def __init__(self, fitness, finished) :
        self.fitness = fitness 
        self.finished = finished

class CPPNComponent :

    def __init__(self, node_evals, input_nodes, output_nodes) :
        self.node_evals = node_evals
        self.input_nodes = input_nodes 
        self.output_nodes = output_nodes 

class ControllerNetworkComponent :

    def __init__(self, node_evals, input_nodes, output_nodes) :
        self.node_evals = node_evals
        self.input_nodes = input_nodes 
        self.output_nodes = output_nodes


class BodyNetworkComponent :

    def __init__(self, node_evals, input_nodes, output_nodes) :
        self.node_evals = node_evals
        self.input_nodes = input_nodes 
        self.output_nodes = output_nodes

class BodyComponent : 

    def __init__(self, body) :
        self.body = body 