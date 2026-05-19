import numpy as np 


class GenomeOperator:

    def __init__(self, config, robot_simulator):
        self.config = config 
        self.robot_simulator = robot_simulator


    def generate_first_generation_of_genome(self, shape_of_cppn) :

        node = 0 
        nodes_by_layer = []
        connections = {}
        for index_of_layer in range(len(shape_of_cppn)) :
            nodes_on_layer = []
            for _ in range(shape_of_cppn[index_of_layer]) :
                nodes_on_layer.append(node)
                node += 1
            nodes_by_layer.append(nodes_on_layer)

        for index_of_layer in range(len(nodes_by_layer)) :
            if index_of_layer == 0 :
                previous_layer = nodes_by_layer[index_of_layer]
                continue 
            for node in nodes_by_layer[index_of_layer] :
                for previous_node in previous_layer :
                    weight1 = np.random.uniform(-1, 1)
                    weight2 = np.random.uniform(-1, 1)
                    dominance1
                    dominance2



    
        