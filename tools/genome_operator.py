import numpy as np 


class GenomeOperator:

    def __init__(self, config, robot_simulator):
        self.config = config 
        self.robot_simulator = robot_simulator



    def nodes_by_layer(self, shape_of_cppn) :
        node = 0 
        nodes_by_layer = []
        for index_of_layer in range(len(shape_of_cppn)) :
            nodes_on_layer = []
            for _ in range(shape_of_cppn[index_of_layer]) :
                nodes_on_layer.append(node)
                node += 1
            nodes_by_layer.append(nodes_on_layer)
        return nodes_by_layer

    def generate_first_generation_of_genome(self, nodes_by_layer) :

        output_activation_function = lambda x : x

        connections1 = {}
        connections2 = {}
        bias1 = {}
        bias2 = {}
        activation_functions1 = {}
        activation_functions2 = {}
        dominance1 = {}
        dominance2 = {}

        for index_of_layer in range(len(nodes_by_layer)) :
            if index_of_layer == 0 :
                previous_layer = nodes_by_layer[index_of_layer]
                continue 
            for node in nodes_by_layer[index_of_layer] :
                for previous_node in previous_layer :
                    weight1 = np.random.uniform(-1, 1)
                    weight2 = np.random.uniform(-1, 1)
                d1 = np.random.randint(0, 1)
                d2 = np.random.randint(0, 1)
                b1 = np.random.uniform(-1, 1)
                b2 = np.random.uniform(-1, 1)
                act_function1 = np.tanh()
                act_function2 = np.tanh()
                connections1[(previous_node, node)] = weight1
                connections2[(previous_node, node)] = weight2
                bias1[node] = b1
                bias2[node] = b2 
                activation_functions1[node] = act_function1 if index_of_layer != len(nodes_by_layer) - 1 else output_activation_function 
                activation_functions2[node] = act_function2 if index_of_layer != len(nodes_by_layer) - 1 else output_activation_function 
                dominance1[node] = d1
                dominance2[node] = d2
                previous_layer = nodes_by_layer[index_of_layer]
        return connections1, connections2, bias1, bias2, activation_functions1, activation_functions2, dominance1, dominance2, nodes_by_layer


    def dominance(self, genome) :
        connections = {}
        bias = {}
        functions = {}

        for index_of_layer in range(len(genome.nodes)) :
            if index_of_layer == 0 :
                previous_layer = genome.nodes[index_of_layer]
                continue 

            for node in genome.nodes[index_of_layer] :
                for previous_node in previous_layer :
                    if genome.dominances[0][node] > genome.dominances[1][node] :
                        connections[(previous_node, node)] = genome.connections[0][(previous_node, node)]
                        bias[node] = genome.biases[0][node]
                        functions[node] = genome.functions[0][node]
                    elif genome.dominances[0][node] < genome.dominances[1][node] :
                        connections[(previous_node, node)] = genome.connections[1][(previous_node, node)]
                        bias[node] = genome.biases[1][node]
                        functions[node] = genome.functions[1][node]
                    else :
                        choice = np.random.randint(0, 1)
                        connections[(previous_node, node)] = genome.connections[choice][(previous_node, node)]
                        bias[node] = genome.biases[choice][node]
                        functions[node] = genome.functions[choice][node]

                previous_layer = genome.nodes[index_of_layer]

        return connections, bias, functions

    def crossover(self, genome1, genome2) :

        connections =[]
        bias = []
        functions = []
        dominances = []


        choice1 = np.random.randint(0, 1)
        connections_parent1 = genome1.connections[choice1] 
        bias_parent1 = genome1.biases[choice1]
        functions_parent1 = genome1.functions[choice1]
        dominances_parent1 = genome1.dominances[choice1]
        choice2 = np.random.randint(0, 1)
        connections_parent2 = genome2.connections[choice2]
        bias_parent2 = genome2.biases[choice2]
        functions_parent2 = genome2.functions[choice2]
        dominances_parent2 = genome2.dominances[choice2]

        connections.append(connections_parent1)
        connections.append(connections_parent2)
        bias.append(bias_parent1)
        bias.append(bias_parent2)
        functions.append(functions_parent1)
        functions.append(functions_parent2)
        dominances.append(dominances_parent1)
        dominances.append(dominances_parent2)

        return connections, bias, functions, dominances, genome1.nodes



    def mutate(self, genome, sigma_weight, sigma_bias, threshold_weight, threshold_bias, threshold_function, threshold_dominance, functions_pool) :
        for connections in genome.connections : # 2 ici 
            for connection in connections :
                if np.random.uniform() > threshold_weight :
                    connections[connection] += np.random.normal(loc = 0, scale = sigma_weight)
        for biases in genome.biases :
            for node in biases :
                if np.random.uniform() > threshold_bias :
                    biases[node] += np.random.normal(loc = 0, scale = sigma_bias)
        list_of_keys = list(functions_pool.keys())
        for functions in genome.functions :
            for node in functions :
                if node in genome.nodes[-1] :
                    continue 
                if np.random.uniform() > threshold_function :
                    choice = np.random.randint(0, len(list_of_keys)-1) 
                    new_function = functions_pool[list_of_keys[choice]]
                    while functions[node] == new_function :
                        choice = np.random.randint(0, len(list_of_keys)) 
                        new_function = functions_pool[list_of_keys[choice]]
                    functions[node] = new_function
        for dominances in genome.dominances :
            for node in dominances :
                if np.random.uniform() > threshold_dominance :
                    dominances[node] = 0 if dominances[node] == 1 else 0
        
        return genome 
    



        




                






    
        