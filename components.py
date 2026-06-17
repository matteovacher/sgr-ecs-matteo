

class StatisticComponent :
    def __init__(self, generation, average, std, best, fitness, average_best, std_best) :
        self.generation = generation
        self.average = average
        self.std = std
        self.best = best
        self.average_best = average_best
        self.std_best = std_best
        self.fitness = fitness

class ParentsComponent :
    def __init__(self, parent1, parent2, choice1, choice2) :
        self.parents = [parent1, parent2]
        self.parents_choices = [choice1, choice2]
        # choice 1 means choice for parent 1 will be 0 or  0 means first chrom and 1 means the 2nd

class HaploidParentsComponent :
    def __init__(self, parent1, parent2) :
        self.parents = [parent1, parent2]

class AgeComponent :
    def __init__(self, age) :
        self.age = age

class GenerationComponent :
    def __init__(self, generation) :
        self.generation = generation

class TosaveComponent :
    def __init__(self, tosave) :
        self.tosave = tosave

class GenomeComponent : 

    def __init__(self, connections1, connections2, bias1, bias2, function1, function2, dominance1, dominance2, nodes) :
        self.connections = [connections1, connections2]
        self.biases = [bias1, bias2]
        self.functions = [function1, function2]
        self.dominances =[dominance1, dominance2]
        self.nodes = nodes 

class HaploidComponent :
    def __init__(self, connections, biases, functions, dominances, nodes) :
        self.connections = connections 
        self.biases = biases 
        self.functions = functions 
        self.dominances = dominances 
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

    def __init__(self, body, connections) :
        self.body = body 
        self.connections = connections 