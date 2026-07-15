import numpy as np 
import copy 

class GenomeOperator:

    def __init__(self, config):
        self.config = config 

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
    
    # [[11], [2, 2], [3, 3], [1, 1]]

    def nodes_by_layer_with_modu_regu(self, shape_of_cppn) :
        node = 0 
        nodes_by_layer = []
        for index_of_layer in range(len(shape_of_cppn)) :
            branches = len(shape_of_cppn[index_of_layer])
            nodes_on_layer = []
            for branch in range(branches) :
                nodes_on_branch = []
                for _ in range(shape_of_cppn[index_of_layer][branch]) :
                    nodes_on_branch.append(node)
                    node += 1
                nodes_on_layer.append(nodes_on_branch)
            nodes_by_layer.append(nodes_on_layer)
        return nodes_by_layer


    def generate_first_generation_of_genome(self, nodes_by_layer, functions_pool) :

        output_activation_function = lambda x : x

        connections1 = {}
        connections2 = {}
        bias1 = {}
        bias2 = {}
        activation_functions1 = {}
        activation_functions2 = {}
        dominance1 = {}
        dominance2 = {}

        list_of_keys = list(functions_pool.keys())

        for index_of_layer in range(len(nodes_by_layer)) :
            if index_of_layer == 0 :
                previous_layer = nodes_by_layer[index_of_layer]
                continue 
            for node in nodes_by_layer[index_of_layer] :
                for previous_node in previous_layer :
                    weight1 = self.config.range_weight * np.random.uniform(-1, 1)
                    weight2 = self.config.range_weight * np.random.uniform(-1, 1)
                    connections1[(previous_node, node)] = weight1
                    connections2[(previous_node, node)] = weight2
                d1 = np.random.randint(1, self.config.number_of_dominances + 1)
                d2 = np.random.randint(1, self.config.number_of_dominances + 1)
                b1 = self.config.range_bias * np.random.uniform(-1, 1)
                b2 = self.config.range_bias * np.random.uniform(-1, 1)
                c1 = np.random.randint(0, len(list_of_keys)) 
                c2 = np.random.randint(0, len(list_of_keys))

                act_function1 = functions_pool[list_of_keys[c1]]
                act_function2 = functions_pool[list_of_keys[c2]]
                bias1[node] = b1
                bias2[node] = b2 
                activation_functions1[node] = act_function1 if index_of_layer != len(nodes_by_layer) - 1 else output_activation_function 
                activation_functions2[node] = act_function2 if index_of_layer != len(nodes_by_layer) - 1 else output_activation_function 
                dominance1[node] = d1
                dominance2[node] = d2
            previous_layer = nodes_by_layer[index_of_layer]
        return connections1, connections2, bias1, bias2, activation_functions1, activation_functions2, dominance1, dominance2, nodes_by_layer

    def generate_first_generation_of_genome_with_modu_regu_0_init(self, nodes_by_layer, functions_pool) :
        output_activation_function = lambda x : x

        connections1 = {}
        connections2 = {}
        bias1 = {}
        bias2 = {}
        activation_functions1 = {}
        activation_functions2 = {}
        dominance1 = {}
        dominance2 = {}

        list_of_keys = list(functions_pool.keys())

        for index_of_layer in range(len(nodes_by_layer)) :
            if index_of_layer == 0 :
                previous_layer = nodes_by_layer[index_of_layer]
                continue 
            if len(previous_layer) == 1 and len(nodes_by_layer[index_of_layer]) == 1 : 
                for node in nodes_by_layer[index_of_layer][0] :
                    for previous_node in previous_layer[0] :
                        weight1 = self.config.range_weight * np.random.uniform(-1, 1)
                        weight2 = self.config.range_weight * np.random.uniform(-1, 1)
                        connections1[(previous_node, node)] = weight1
                        connections2[(previous_node, node)] = weight2
                    d1 = 1
                    d2 = 1
                    b1 = self.config.range_bias * np.random.uniform(-1, 1)
                    b2 = self.config.range_bias * np.random.uniform(-1, 1)
                    c1 = np.random.randint(0, len(list_of_keys)) 
                    c2 = np.random.randint(0, len(list_of_keys))
                    act_function1 = functions_pool[list_of_keys[c1]]        
                    act_function2 = functions_pool[list_of_keys[c2]]
                    bias1[node] = b1
                    bias2[node] = b2
                    activation_functions1[node] = act_function1 if index_of_layer != len(nodes_by_layer) - 1 else output_activation_function 
                    activation_functions2[node] = act_function2 if index_of_layer != len(nodes_by_layer) - 1 else output_activation_function
                    dominance1[node] = d1
                    dominance2[node] = d2
                previous_layer = nodes_by_layer[index_of_layer]
            elif len(previous_layer) == 1 and len(nodes_by_layer[index_of_layer]) > 1 :
                for branch in range(len(nodes_by_layer[index_of_layer])) :
                    for node in nodes_by_layer[index_of_layer][branch] :
                        for previous_node in previous_layer[0] :
                            weight1 = self.config.range_weight * np.random.uniform(-1, 1)
                            weight2 = self.config.range_weight * np.random.uniform(-1, 1)
                            connections1[(previous_node, node)] = weight1
                            connections2[(previous_node, node)] = weight2
                        d1 = 1
                        d2 = 1
                        b1 = self.config.range_bias * np.random.uniform(-1, 1)
                        b2 = self.config.range_bias * np.random.uniform(-1, 1)
                        c1 = np.random.randint(0, len(list_of_keys))
                        c2 = np.random.randint(0, len(list_of_keys))
                        act_function1 = functions_pool[list_of_keys[c1]]
                        act_function2 = functions_pool[list_of_keys[c2]]
                        bias1[node] = b1
                        bias2[node] = b2
                        activation_functions1[node] = act_function1 if index_of_layer != len(nodes_by_layer) - 1 else output_activation_function
                        activation_functions2[node] = act_function2 if index_of_layer != len(nodes_by_layer) - 1 else output_activation_function
                        dominance1[node] = d1
                        dominance2[node] = d2
                previous_layer = nodes_by_layer[index_of_layer]
            elif len(previous_layer) > 1 and len(nodes_by_layer[index_of_layer]) > 1 :
                for branch in range(len(nodes_by_layer[index_of_layer])) :
                    for node in nodes_by_layer[index_of_layer][branch] :
                        for previous_node in previous_layer[branch] :
                            weight1 = self.config.range_weight * np.random.uniform(-1, 1)
                            weight2 = self.config.range_weight * np.random.uniform(-1, 1)
                            connections1[(previous_node, node)] = weight1
                            connections2[(previous_node, node)] = weight2
                        d1 = 1
                        d2 = 1
                        b1 = self.config.range_bias * np.random.uniform(-1, 1)
                        b2 = self.config.range_bias * np.random.uniform(-1, 1)
                        c1 = np.random.randint(0, len(list_of_keys))
                        c2 = np.random.randint(0, len(list_of_keys))
                        act_function1 = functions_pool[list_of_keys[c1]]
                        act_function2 = functions_pool[list_of_keys[c2]]
                        bias1[node] = b1
                        bias2[node] = b2
                        activation_functions1[node] = act_function1 if index_of_layer != len(nodes_by_layer) - 1 else output_activation_function
                        activation_functions2[node] = act_function2 if index_of_layer != len(nodes_by_layer) - 1 else output_activation_function
                        dominance1[node] = d1
                        dominance2[node] = d2
                previous_layer = nodes_by_layer[index_of_layer]
        return connections1, connections2, bias1, bias2, activation_functions1, activation_functions2, dominance1, dominance2, nodes_by_layer

    def generate_first_generation_of_genome_with_modu_regu(self, nodes_by_layer, functions_pool) :
        output_activation_function = lambda x : x

        connections1 = {}
        connections2 = {}
        bias1 = {}
        bias2 = {}
        activation_functions1 = {}
        activation_functions2 = {}
        dominance1 = {}
        dominance2 = {}

        list_of_keys = list(functions_pool.keys())

        for index_of_layer in range(len(nodes_by_layer)) :
            if index_of_layer == 0 :
                previous_layer = nodes_by_layer[index_of_layer]
                continue 
            if len(previous_layer) == 1 and len(nodes_by_layer[index_of_layer]) == 1 : 
                for node in nodes_by_layer[index_of_layer][0] :
                    for previous_node in previous_layer[0] :
                        weight1 = self.config.range_weight * np.random.uniform(-1, 1)
                        weight2 = self.config.range_weight * np.random.uniform(-1, 1)
                        connections1[(previous_node, node)] = weight1
                        connections2[(previous_node, node)] = weight2
                    d1 = np.random.randint(1, self.config.number_of_dominances + 1)
                    d2 = np.random.randint(1, self.config.number_of_dominances + 1)
                    b1 = self.config.range_bias * np.random.uniform(-1, 1)
                    b2 = self.config.range_bias * np.random.uniform(-1, 1)
                    c1 = np.random.randint(0, len(list_of_keys)) 
                    c2 = np.random.randint(0, len(list_of_keys))
                    act_function1 = functions_pool[list_of_keys[c1]]        
                    act_function2 = functions_pool[list_of_keys[c2]]
                    bias1[node] = b1
                    bias2[node] = b2
                    activation_functions1[node] = act_function1 if index_of_layer != len(nodes_by_layer) - 1 else output_activation_function 
                    activation_functions2[node] = act_function2 if index_of_layer != len(nodes_by_layer) - 1 else output_activation_function
                    dominance1[node] = d1
                    dominance2[node] = d2
                previous_layer = nodes_by_layer[index_of_layer]
            elif len(previous_layer) == 1 and len(nodes_by_layer[index_of_layer]) > 1 :
                for branch in range(len(nodes_by_layer[index_of_layer])) :
                    for node in nodes_by_layer[index_of_layer][branch] :
                        for previous_node in previous_layer[0] :
                            weight1 = self.config.range_weight * np.random.uniform(-1, 1)
                            weight2 = self.config.range_weight * np.random.uniform(-1, 1)
                            connections1[(previous_node, node)] = weight1
                            connections2[(previous_node, node)] = weight2
                        d1 = np.random.randint(1, self.config.number_of_dominances + 1)
                        d2 = np.random.randint(1, self.config.number_of_dominances + 1)
                        b1 = self.config.range_bias * np.random.uniform(-1, 1)
                        b2 = self.config.range_bias * np.random.uniform(-1, 1)
                        c1 = np.random.randint(0, len(list_of_keys))
                        c2 = np.random.randint(0, len(list_of_keys))
                        act_function1 = functions_pool[list_of_keys[c1]]
                        act_function2 = functions_pool[list_of_keys[c2]]
                        bias1[node] = b1
                        bias2[node] = b2
                        activation_functions1[node] = act_function1 if index_of_layer != len(nodes_by_layer) - 1 else output_activation_function
                        activation_functions2[node] = act_function2 if index_of_layer != len(nodes_by_layer) - 1 else output_activation_function
                        dominance1[node] = d1
                        dominance2[node] = d2
                previous_layer = nodes_by_layer[index_of_layer]
            elif len(previous_layer) > 1 and len(nodes_by_layer[index_of_layer]) > 1 :
                for branch in range(len(nodes_by_layer[index_of_layer])) :
                    for node in nodes_by_layer[index_of_layer][branch] :
                        for previous_node in previous_layer[branch] :
                            weight1 = self.config.range_weight * np.random.uniform(-1, 1)
                            weight2 = self.config.range_weight * np.random.uniform(-1, 1)
                            connections1[(previous_node, node)] = weight1
                            connections2[(previous_node, node)] = weight2
                        d1 = np.random.randint(1, self.config.number_of_dominances + 1)
                        d2 = np.random.randint(1, self.config.number_of_dominances + 1)
                        b1 = self.config.range_bias * np.random.uniform(-1, 1)
                        b2 = self.config.range_bias * np.random.uniform(-1, 1)
                        c1 = np.random.randint(0, len(list_of_keys))
                        c2 = np.random.randint(0, len(list_of_keys))
                        act_function1 = functions_pool[list_of_keys[c1]]
                        act_function2 = functions_pool[list_of_keys[c2]]
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
                    
                if genome.dominances[0][node] > genome.dominances[1][node] :
                    bias[node] = genome.biases[0][node]
                    functions[node] = genome.functions[0][node]
                    for previous_node in previous_layer :
                        connections[(previous_node, node)] = genome.connections[0][(previous_node, node)]
                elif genome.dominances[0][node] < genome.dominances[1][node] :
                    bias[node] = genome.biases[1][node]
                    functions[node] = genome.functions[1][node]
                    for previous_node in previous_layer :
                        connections[(previous_node, node)] = genome.connections[1][(previous_node, node)]
                else :
                    choice = np.random.randint(0, 2)
                    bias[node] = genome.biases[choice][node]
                    functions[node] = genome.functions[choice][node]
                    for previous_node in previous_layer :
                        connections[(previous_node, node)] = genome.connections[choice][(previous_node, node)]

            previous_layer = genome.nodes[index_of_layer]

        return connections, bias, functions

    def _incoming_by_node(self, previous_layer, current_layer) :

        pairs = []
        if len(previous_layer) == 1 and len(current_layer) == 1 :
            for node in current_layer[0] :
                pairs.append((node, previous_layer[0]))
        elif len(previous_layer) == 1 and len(current_layer) > 1 :
            for branch in range(len(current_layer)) :
                for node in current_layer[branch] :
                    pairs.append((node, previous_layer[0]))
        elif len(previous_layer) > 1 and len(current_layer) > 1 :
            for branch in range(len(current_layer)) :
                for node in current_layer[branch] :
                    pairs.append((node, previous_layer[branch]))
        return pairs

    def dominance_with_modu_regu(self, genome) :

        connections = {}
        bias = {}
        functions = {}

        for index_of_layer in range(len(genome.nodes)) :
            if index_of_layer == 0 :
                previous_layer = genome.nodes[index_of_layer]
                continue

            current_layer = genome.nodes[index_of_layer]

            for node, previous_nodes in self._incoming_by_node(previous_layer, current_layer) :
                if genome.dominances[0][node] > genome.dominances[1][node] :
                    bias[node] = copy.deepcopy(genome.biases[0][node])
                    functions[node] = copy.deepcopy(genome.functions[0][node])
                    for previous_node in previous_nodes :
                        connections[(previous_node, node)] = copy.deepcopy(genome.connections[0][(previous_node, node)])
                elif genome.dominances[0][node] < genome.dominances[1][node] :
                    bias[node] = copy.deepcopy(genome.biases[1][node])
                    functions[node] = copy.deepcopy(genome.functions[1][node])
                    for previous_node in previous_nodes :
                        connections[(previous_node, node)] = copy.deepcopy(genome.connections[1][(previous_node, node)])
                else :
                    choice = np.random.randint(0, 2)
                    bias[node] = copy.deepcopy(genome.biases[choice][node])
                    functions[node] = copy.deepcopy(genome.functions[choice][node])
                    for previous_node in previous_nodes :
                        connections[(previous_node, node)] = copy.deepcopy(genome.connections[choice][(previous_node, node)])

            previous_layer = current_layer

        return connections, bias, functions

    def codominance(self, genome) :
        
        connections = {}
        bias = {}
        functions = {}

        for index_of_layer in range(len(genome.nodes)) :
            if index_of_layer == 0 :
                previous_layer = genome.nodes[index_of_layer]
                continue 

            for node in genome.nodes[index_of_layer] :
                    
                if genome.dominances[0][node] > genome.dominances[1][node] :
                    bias[node] = copy.deepcopy(genome.biases[0][node])
                    functions[node] = genome.functions[0][node]
                    for previous_node in previous_layer :
                        connections[(previous_node, node)] = genome.connections[0][(previous_node, node)]
                elif genome.dominances[0][node] < genome.dominances[1][node] :
                    bias[node] = genome.biases[1][node]
                    functions[node] = genome.functions[1][node]
                    for previous_node in previous_layer :
                        connections[(previous_node, node)] = genome.connections[1][(previous_node, node)]
                else :
                    choice = np.random.randint(0, 2)
                    bias[node] = (genome.biases[0][node] + genome.biases[1][node]) / 2
                    genome.biases[choice][node] = copy.deepcopy(bias[node])
                    functions[node] = genome.functions[choice][node]
                    for previous_node in previous_layer :
                        connections[(previous_node, node)] = (genome.connections[0][(previous_node, node)] + genome.connections[1][(previous_node, node)]) / 2
                        genome.connections[choice][(previous_node, node)] = copy.deepcopy(connections[(previous_node, node)])
            previous_layer = genome.nodes[index_of_layer]

        return connections, bias, functions

    def codominance_with_modu_regu(self, genome) :

        connections = {}
        bias = {}
        functions = {}

        for index_of_layer in range(len(genome.nodes)) :
            if index_of_layer == 0 :
                previous_layer = genome.nodes[index_of_layer]
                continue

            current_layer = genome.nodes[index_of_layer]

            for node, previous_nodes in self._incoming_by_node(previous_layer, current_layer) :
                if genome.dominances[0][node] > genome.dominances[1][node] :
                    bias[node] = genome.biases[0][node]
                    functions[node] = genome.functions[0][node]
                    for previous_node in previous_nodes :
                        connections[(previous_node, node)] = genome.connections[0][(previous_node, node)]
                elif genome.dominances[0][node] < genome.dominances[1][node] :
                    bias[node] = genome.biases[1][node]
                    functions[node] = genome.functions[1][node]
                    for previous_node in previous_nodes :
                        connections[(previous_node, node)] = genome.connections[1][(previous_node, node)]
                else :
                    choice = np.random.randint(0, 2)
                    bias[node] = (genome.biases[0][node] + genome.biases[1][node]) / 2
                    genome.biases[choice][node] = copy.deepcopy(bias[node])
                    functions[node] = genome.functions[choice][node]
                    for previous_node in previous_nodes :
                        connections[(previous_node, node)] = (genome.connections[0][(previous_node, node)] + genome.connections[1][(previous_node, node)]) / 2
                        genome.connections[choice][(previous_node, node)] = copy.deepcopy(connections[(previous_node, node)])

            previous_layer = current_layer

        return connections, bias, functions

    def crossover(self, genome1, genome2) :

        connections =[]
        bias = []
        functions = []
        dominances = []


        choice1 = np.random.randint(0, 2)
        connections_parent1 = copy.deepcopy(genome1.connections[choice1])
        bias_parent1 = copy.deepcopy(genome1.biases[choice1])
        functions_parent1 = copy.deepcopy(genome1.functions[choice1])
        dominances_parent1 = copy.deepcopy(genome1.dominances[choice1])
        choice2 = np.random.randint(0, 2)
        connections_parent2 = copy.deepcopy(genome2.connections[choice2])   
        bias_parent2 = copy.deepcopy(genome2.biases[choice2])
        functions_parent2 = copy.deepcopy(genome2.functions[choice2])
        dominances_parent2 = copy.deepcopy(genome2.dominances[choice2])

        connections.append(connections_parent1)
        connections.append(connections_parent2)
        bias.append(bias_parent1)
        bias.append(bias_parent2)
        functions.append(functions_parent1)
        functions.append(functions_parent2)
        dominances.append(dominances_parent1)
        dominances.append(dominances_parent2)

        nodes = copy.deepcopy(genome1.nodes)

        return connections, bias, functions, dominances, nodes, choice1, choice2
    
    def meiosis_crossover(self, genome1, genome2) :
        # first determine where to make the cut in the chromosome 
        nodes_by_layer = genome1.nodes
        first_nodes = nodes_by_layer[1][0]
        secondary_nodes = []
        for index in range(2, len(nodes_by_layer)) :
            if len(nodes_by_layer[index]) > 1 :
                for branch in range(len(nodes_by_layer[index])) :
                    secondary_nodes += [nodes_by_layer[index][branch][i] for i in range(len(nodes_by_layer[index][branch]))]
            if len(nodes_by_layer[index]) == 1 :
                secondary_nodes += [nodes_by_layer[index][0][i] for i in range(len(nodes_by_layer[index][0]))]

        connections = []
        bias = []
        functions = []
        dominances = []

        new_connections_parent1 = []
        new_bias_parent1 = []
        new_functions_parent1 = []
        new_dominances_parent1 = []

        new_connections_parent2 = []
        new_bias_parent2 = []
        new_functions_parent2 = []
        new_dominances_parent2 = []

        connections1 = {}
        bias1 = {}
        functions1 = {}
        dominances1 = {}

        connections2 = {}
        bias2 = {}
        functions2 = {}
        dominances2 = {} 


        for chromosome in range(len(genome1.connections)) :

            for (previous_node, node) in genome1.connections[chromosome].keys() : 
                if node in first_nodes and chromosome == 0 :
                    connections1[(previous_node, node)] = copy.deepcopy(genome1.connections[chromosome][(previous_node, node)])
                elif node in secondary_nodes and chromosome == 0 :
                    connections2[(previous_node, node)] = copy.deepcopy(genome1.connections[chromosome][(previous_node, node)])
                elif node in first_nodes and chromosome == 1 :
                    connections2[(previous_node, node)] = copy.deepcopy(genome1.connections[chromosome][(previous_node, node)])
                elif node in secondary_nodes and chromosome == 1 : 
                    connections1[(previous_node, node)] = copy.deepcopy(genome1.connections[chromosome][(previous_node, node)])    
            for node in genome1.biases[chromosome].keys() :
                if node in first_nodes and chromosome == 0 :
                    bias1[node] = copy.deepcopy(genome1.biases[chromosome][node])
                elif node in secondary_nodes and chromosome == 0 :
                    bias2[node] = copy.deepcopy(genome1.biases[chromosome][node])
                elif node in first_nodes and chromosome == 1 :
                    bias2[node] = copy.deepcopy(genome1.biases[chromosome][node])
                elif node in secondary_nodes and chromosome == 1 : 
                    bias1[node] = copy.deepcopy(genome1.biases[chromosome][node])
            for node in genome1.functions[chromosome].keys() :
                if node in first_nodes and chromosome == 0 :
                    functions1[node] = copy.deepcopy(genome1.functions[chromosome][node])
                elif node in secondary_nodes and chromosome == 0 :
                    functions2[node] = copy.deepcopy(genome1.functions[chromosome][node])
                elif node in first_nodes and chromosome == 1 :
                    functions2[node] = copy.deepcopy(genome1.functions[chromosome][node])
                elif node in secondary_nodes and chromosome == 1 : 
                    functions1[node] = copy.deepcopy(genome1.functions[chromosome][node])
            for node in genome1.dominances[chromosome].keys() :
                if node in first_nodes and chromosome == 0 :
                    dominances1[node] = copy.deepcopy(genome1.dominances[chromosome][node])
                elif node in secondary_nodes and chromosome == 0 :
                    dominances2[node] = copy.deepcopy(genome1.dominances[chromosome][node])
                elif node in first_nodes and chromosome == 1 :
                    dominances2[node] = copy.deepcopy(genome1.dominances[chromosome][node])
                elif node in secondary_nodes and chromosome == 1 :  
                    dominances1[node] = copy.deepcopy(genome1.dominances[chromosome][node])

        new_connections_parent1.append(copy.deepcopy(connections1))
        new_bias_parent1.append(copy.deepcopy(bias1))
        new_functions_parent1.append(copy.deepcopy(functions1))
        new_dominances_parent1.append(copy.deepcopy(dominances1))
        new_connections_parent1.append(copy.deepcopy(connections2))
        new_bias_parent1.append(copy.deepcopy(bias2))
        new_functions_parent1.append(copy.deepcopy(functions2))
        new_dominances_parent1.append(copy.deepcopy(dominances2))
        

        connections1.clear()
        bias1.clear()
        functions1.clear()
        dominances1.clear()
        connections2.clear()
        bias2.clear()
        functions2.clear()
        dominances2.clear()

        for chromosome in range(len(genome2.connections)) :

            for (previous_node, node) in genome2.connections[chromosome].keys() :
                if node in first_nodes and chromosome == 0 :
                    connections1[(previous_node, node)] = copy.deepcopy(genome2.connections[chromosome][(previous_node, node)])
                elif node in secondary_nodes and chromosome == 0 :
                    connections2[(previous_node, node)] = copy.deepcopy(genome2.connections[chromosome][(previous_node, node)])
                elif node in first_nodes and chromosome == 1 :
                    connections2[(previous_node, node)] = copy.deepcopy(genome2.connections[chromosome][(previous_node, node)])
                elif node in secondary_nodes and chromosome == 1 : 
                    connections1[(previous_node, node)] = copy.deepcopy(genome2.connections[chromosome][(previous_node, node)])   
            for node in genome2.biases[chromosome].keys() :
                if node in first_nodes and chromosome == 0 :
                    bias1[node] = copy.deepcopy(genome2.biases[chromosome][node])
                elif node in secondary_nodes and chromosome == 0 :
                    bias2[node] = copy.deepcopy(genome2.biases[chromosome][node])
                elif node in first_nodes and chromosome == 1 :
                    bias2[node] = copy.deepcopy(genome2.biases[chromosome][node])
                elif node in secondary_nodes and chromosome == 1 : 
                    bias1[node] = copy.deepcopy(genome2.biases[chromosome][node])
            for node in genome2.functions[chromosome].keys() :
                if node in first_nodes and chromosome == 0 :
                    functions1[node] = copy.deepcopy(genome2.functions[chromosome][node])
                elif node in secondary_nodes and chromosome == 0 :
                    functions2[node] = copy.deepcopy(genome2.functions[chromosome][node])
                elif node in first_nodes and chromosome == 1 :
                    functions2[node] = copy.deepcopy(genome2.functions[chromosome][node])
                elif node in secondary_nodes and chromosome == 1 : 
                    functions1[node] = copy.deepcopy(genome2.functions[chromosome][node])
            for node in genome2.dominances[chromosome].keys() :
                if node in first_nodes and chromosome == 0 :
                    dominances1[node] = copy.deepcopy(genome2.dominances[chromosome][node])
                elif node in secondary_nodes and chromosome == 0 :
                    dominances2[node] = copy.deepcopy(genome2.dominances[chromosome][node])
                elif node in first_nodes and chromosome == 1 :
                    dominances2[node] = copy.deepcopy(genome2.dominances[chromosome][node])
                elif node in secondary_nodes and chromosome == 1 : 
                    dominances1[node] = copy.deepcopy(genome2.dominances[chromosome][node])

        new_connections_parent2.append(copy.deepcopy(connections1))
        new_bias_parent2.append(copy.deepcopy(bias1))
        new_functions_parent2.append(copy.deepcopy(functions1))
        new_dominances_parent2.append(copy.deepcopy(dominances1))
        new_connections_parent2.append(copy.deepcopy(connections2))
        new_bias_parent2.append(copy.deepcopy(bias2))
        new_functions_parent2.append(copy.deepcopy(functions2))
        new_dominances_parent2.append(copy.deepcopy(dominances2))

        connections1.clear()
        bias1.clear()
        functions1.clear()
        dominances1.clear()
        connections2.clear()
        bias2.clear()
        functions2.clear()
        dominances2.clear()

        choice1 = np.random.randint(0, 2)
        connections_parent1 = copy.deepcopy(new_connections_parent1[choice1])
        bias_parent1 = copy.deepcopy(new_bias_parent1[choice1])
        functions_parent1 = copy.deepcopy(new_functions_parent1[choice1])   
        dominances_parent1 = copy.deepcopy(new_dominances_parent1[choice1])

        choice2 = np.random.randint(0, 2)
        connections_parent2 = copy.deepcopy(new_connections_parent2[choice2])
        bias_parent2 = copy.deepcopy(new_bias_parent2[choice2])
        functions_parent2 = copy.deepcopy(new_functions_parent2[choice2])
        dominances_parent2 = copy.deepcopy(new_dominances_parent2[choice2])


        connections = [connections_parent1, connections_parent2]
        bias = [bias_parent1, bias_parent2]
        functions = [functions_parent1, functions_parent2]
        dominances = [dominances_parent1, dominances_parent2]

        nodes = copy.deepcopy(genome1.nodes)

        return connections, bias, functions, dominances, nodes, choice1, choice2


    def mutate(self, genome, sigma_weight, sigma_bias, threshold_weight, threshold_bias, threshold_function, threshold_dominance, functions_pool) :
        for connections in genome.connections : # 2 ici 
            for connection in connections :
                if np.random.uniform() < threshold_weight :
                    connections[connection] += np.random.normal(loc = 0, scale = sigma_weight)
                    if abs(connections[connection]) > self.config.max_weight_cppn : 
                        connections[connection] = np.sign(connections[connection]) * self.config.max_weight_cppn 
                    # print('happened w')
        for biases in genome.biases :
            for node in biases :
                if np.random.uniform() < threshold_bias :
                    biases[node] += np.random.normal(loc = 0, scale = sigma_bias)
                    if abs(biases[node]) > self.config.max_bias_cppn :
                        biases[node] = np.sign(biases[node]) * self.config.max_bias_cppn
                    # print('happened b')
        list_of_keys = list(functions_pool.keys())
        for functions in genome.functions :
            for node in functions :
                if node in genome.nodes[-1] :
                    continue 
                if np.random.uniform() < threshold_function :
                    choice = np.random.randint(0, len(list_of_keys)) 
                    new_function = functions_pool[list_of_keys[choice]]
                    while functions[node] == new_function :
                        choice = np.random.randint(0, len(list_of_keys)) 
                        new_function = functions_pool[list_of_keys[choice]]
                    functions[node] = new_function
                    # print('happened f')
        for dominances in genome.dominances :
            for node in dominances :
                if np.random.uniform() < threshold_dominance :
                    choice = np.random.randint(1, self.config.number_of_dominances + 1)
                    while dominances[node] == choice :
                        choice = np.random.randint(1, self.config.number_of_dominances + 1)
                    dominances[node] = choice
                    # print('happened d')

        return genome

    def mutate_with_modu_regu(self, genome, sigma_weight, sigma_bias, threshold_weight, threshold_bias, threshold_function, threshold_dominance, functions_pool) :
        output_nodes = [node for branch in genome.nodes[-1] for node in branch]
        for connections in genome.connections : # 2 ici
            for connection in connections :
                if np.random.uniform() < threshold_weight :
                    connections[connection] += np.random.normal(loc = 0, scale = sigma_weight)
                    if abs(connections[connection]) > self.config.max_weight_cppn :
                        connections[connection] = np.sign(connections[connection]) * self.config.max_weight_cppn
        for biases in genome.biases :
            for node in biases :
                if np.random.uniform() < threshold_bias :
                    biases[node] += np.random.normal(loc = 0, scale = sigma_bias)
                    if abs(biases[node]) > self.config.max_bias_cppn :
                        biases[node] = np.sign(biases[node]) * self.config.max_bias_cppn
        list_of_keys = list(functions_pool.keys())
        for functions in genome.functions :
            for node in functions :
                if node in output_nodes :
                    continue
                if np.random.uniform() < threshold_function :
                    choice = np.random.randint(0, len(list_of_keys))
                    new_function = functions_pool[list_of_keys[choice]]
                    while functions[node] == new_function :
                        choice = np.random.randint(0, len(list_of_keys))
                        new_function = functions_pool[list_of_keys[choice]]
                    functions[node] = new_function
        for dominances in genome.dominances :
            for node in dominances :
                if np.random.uniform() < threshold_dominance :
                    choice = np.random.randint(1, self.config.number_of_dominances + 1)
                    while dominances[node] == choice :
                        choice = np.random.randint(1, self.config.number_of_dominances + 1)
                    dominances[node] = choice

        return genome


class HaploidOperator :

    def __init__(self, config) :
        self.config = config 

    def nodes_by_layer(self, shape_of_cppn) : 
        node = 0 
        nodes_by_layer = []
        for index_of_layer in range(len(shape_of_cppn)) :
            nodes_on_layer = []
            for _ in range (shape_of_cppn[index_of_layer]) :
                nodes_on_layer.append(node)
                node += 1
            nodes_by_layer.append(nodes_on_layer)
        return nodes_by_layer
    
    def generate_first_generation_of_genome(self, nodes_by_layer, functions_pool) :

        output_activation_function = lambda x : x

        connections = {}
        biases = {}
        activation_functions = {}
        dominances = {}


        list_of_keys = list(functions_pool.keys())

        for index_of_layer in range(len(nodes_by_layer)) :
            if index_of_layer == 0 :
                previous_layer = nodes_by_layer[index_of_layer]
                continue 
            for node in nodes_by_layer[index_of_layer] :
                for previous_node in previous_layer :
                    weight = self.config.range_weight * np.random.uniform(-1, 1)
                    connections[(previous_node, node)] = weight
                d = np.random.randint(1, self.config.number_of_dominances + 1)
                b = self.config.range_bias * np.random.uniform(-1, 1)
                c = np.random.randint(0, len(list_of_keys)) 
                act_function = functions_pool[list_of_keys[c]]
                biases[node] = b
                activation_functions[node] = act_function if index_of_layer != len(nodes_by_layer) - 1 else output_activation_function 
                dominances[node] = d
            previous_layer = nodes_by_layer[index_of_layer]
        return connections, biases, activation_functions, dominances, nodes_by_layer

    def crossover(self, haploid, other_haploid) :
        
        connections = {}
        biases = {}
        functions = {}
        dominances = {}

        for index_of_layer in range(len(haploid.nodes)) :
            if index_of_layer == 0 :
                previous_layer = haploid.nodes[index_of_layer]
                continue 

            for node in haploid.nodes[index_of_layer] :

                if haploid.dominances[node] > other_haploid.dominances[node] :
                    biases[node] = copy.deepcopy(haploid.biases[node])
                    functions[node] = copy.deepcopy(haploid.functions[node])
                    dominances[node] = copy.deepcopy(haploid.dominances[node])
                    for previous_node in previous_layer :
                        connections[(previous_node, node)] = copy.deepcopy(haploid.connections[(previous_node, node)])
                elif haploid.dominances[node] < other_haploid.dominances[node] :
                    biases[node] = copy.deepcopy(other_haploid.biases[node])
                    functions[node] = copy.deepcopy(other_haploid.functions[node])  
                    dominances[node] = copy.deepcopy(other_haploid.dominances[node])
                    for previous_node in previous_layer :
                        connections[(previous_node, node)] = copy.deepcopy(other_haploid.connections[(previous_node, node)])
                else :
                    choice = np.random.randint(0, 2)
                    if choice == 0 : 
                        biases[node] = copy.deepcopy(haploid.biases[node])
                        functions[node] = copy.deepcopy(haploid.functions[node])  
                        dominances[node] = copy.deepcopy(haploid.dominances[node])
                        for previous_node in previous_layer :
                            connections[(previous_node, node)] = copy.deepcopy(haploid.connections[(previous_node, node)])
                    else : 
                        biases[node] = copy.deepcopy(other_haploid.biases[node])
                        functions[node] = copy.deepcopy(other_haploid.functions[node])  
                        dominances[node] = copy.deepcopy(other_haploid.dominances[node])
                        for previous_node in previous_layer :    
                            connections[(previous_node, node)] = copy.deepcopy(other_haploid.connections[(previous_node, node)])                                

            previous_layer = haploid.nodes[index_of_layer]
        
        nodes = copy.deepcopy(haploid.nodes)

        return connections, biases, functions, dominances, nodes 

    
    
    def cocrossover(self, haploid, other_haploid) :
        connections = {}
        biases = {}
        functions = {}
        dominances = {}

        for index_of_layer in range(len(haploid.nodes)) :
            if index_of_layer == 0 :
                previous_layer = haploid.nodes[index_of_layer]
                continue 

            for node in haploid.nodes[index_of_layer] :

                if haploid.dominances[node] > other_haploid.dominances[node] :
                    biases[node] = copy.deepcopy(haploid.biases[node])
                    functions[node] = copy.deepcopy(haploid.functions[node])
                    dominances[node] = copy.deepcopy(haploid.dominances[node])
                    for previous_node in previous_layer :
                        connections[(previous_node, node)] = copy.deepcopy(haploid.connections[(previous_node, node)])
                elif haploid.dominances[node] < other_haploid.dominances[node] :
                    biases[node] = copy.deepcopy(other_haploid.biases[node])
                    functions[node] = copy.deepcopy(other_haploid.functions[node])  
                    dominances[node] = copy.deepcopy(other_haploid.dominances[node])
                    for previous_node in previous_layer :
                        connections[(previous_node, node)] = copy.deepcopy(other_haploid.connections[(previous_node, node)])
                else :
                    choice = np.random.randint(0, 2)
                    if choice == 0 : 
                        functions[node] = copy.deepcopy(haploid.functions[node])  
                        dominances[node] = copy.deepcopy(haploid.dominances[node])
                    else : 
                        functions[node] = copy.deepcopy(other_haploid.functions[node])  
                        dominances[node] = copy.deepcopy(other_haploid.dominances[node])
                        
                    biases[node] = (copy.deepcopy(haploid.biases[node]) + copy.deepcopy(other_haploid.biases[node])) / 2
                    for previous_node in previous_layer :
                        connections[(previous_node, node)] = (copy.deepcopy(haploid.connections[(previous_node, node)]) + copy.deepcopy(other_haploid.connections[(previous_node, node)])) / 2
            
            previous_layer = haploid.nodes[index_of_layer]
        
        nodes = copy.deepcopy(haploid.nodes)

        return connections, biases, functions, dominances, nodes 
    

    def mutate(self, genome, sigma_weight, sigma_bias, threshold_weight, threshold_bias, threshold_function, threshold_dominance, functions_pool) : 

        for node in genome.connections :
            if np.random.uniform() < threshold_weight  :
                genome.connections[node] += np.random.normal(loc = 0, scale = sigma_weight )
                if abs(genome.connections[node]) > self.config.max_weight_cppn :
                    genome.connections[node] = np.sign(genome.connections[node]) * self.config.max_weight_cppn
    
        for node in genome.biases :
            if np.random.uniform() < threshold_bias :
                genome.biases[node] += np.random.normal(loc = 0, scale = sigma_bias)
                if abs(genome.biases[node]) > self.config.max_bias_cppn :
                    genome.biases[node] = np.sign(genome.biases[node]) * self.config.max_bias_cppn

        list_of_keys = list(functions_pool.keys())
        for node in genome.functions :
            if node in genome.nodes[-1] :
                continue 
            if np.random.uniform() < threshold_function :
                choice = np.random.randint(0, len(list_of_keys))
                new_function = functions_pool[list_of_keys[choice]]
                while genome.functions[node] == new_function :
                    choice = np.random.randint(0, len(list_of_keys))
                    new_function = functions_pool[list_of_keys[choice]]
                genome.functions[node] = new_function

        for node in genome.dominances :
            if np.random.uniform() < threshold_dominance :
                choice = np.random.randint(1, self.config.number_of_dominances + 1)                     
                while genome.dominances[node] == choice :
                    choice = np.random.randint(1, self.config.number_of_dominances + 1)
                genome.dominances[node] = choice

        return genome

    def _incoming_by_node(self, previous_layer, current_layer) :
        pairs = []
        if len(previous_layer) == 1 and len(current_layer) == 1 :
            for node in current_layer[0] :
                pairs.append((node, previous_layer[0]))
        elif len(previous_layer) == 1 and len(current_layer) > 1 :
            for branch in range(len(current_layer)) :
                for node in current_layer[branch] :
                    pairs.append((node, previous_layer[0]))
        elif len(previous_layer) > 1 and len(current_layer) > 1 :
            for branch in range(len(current_layer)) :
                for node in current_layer[branch] :
                    pairs.append((node, previous_layer[branch]))
        return pairs

    def nodes_by_layer_with_modu_regu(self, shape_of_cppn) :
        node = 0
        nodes_by_layer = []
        for index_of_layer in range(len(shape_of_cppn)) :
            branches = len(shape_of_cppn[index_of_layer])
            nodes_on_layer = []
            for branch in range(branches) :
                nodes_on_branch = []
                for _ in range(shape_of_cppn[index_of_layer][branch]) :
                    nodes_on_branch.append(node)
                    node += 1
                nodes_on_layer.append(nodes_on_branch)
            nodes_by_layer.append(nodes_on_layer)
        return nodes_by_layer

    def generate_first_generation_of_genome_with_modu_regu(self, nodes_by_layer, functions_pool) :
        output_activation_function = lambda x : x

        connections = {}
        biases = {}
        activation_functions = {}
        dominances = {}

        list_of_keys = list(functions_pool.keys())

        for index_of_layer in range(len(nodes_by_layer)) :
            if index_of_layer == 0 :
                previous_layer = nodes_by_layer[index_of_layer]
                continue
            current_layer = nodes_by_layer[index_of_layer]
            for node, previous_nodes in self._incoming_by_node(previous_layer, current_layer) :
                for previous_node in previous_nodes :
                    weight = self.config.range_weight * np.random.uniform(-1, 1)
                    connections[(previous_node, node)] = weight
                d = np.random.randint(1, self.config.number_of_dominances + 1)
                b = self.config.range_bias * np.random.uniform(-1, 1)
                c = np.random.randint(0, len(list_of_keys))
                act_function = functions_pool[list_of_keys[c]]
                biases[node] = b
                activation_functions[node] = act_function if index_of_layer != len(nodes_by_layer) - 1 else output_activation_function
                dominances[node] = d
            previous_layer = current_layer
        return connections, biases, activation_functions, dominances, nodes_by_layer


    def generate_first_generation_of_genome_with_modu_regu_0_init(self, nodes_by_layer, functions_pool) :
        output_activation_function = lambda x : x

        connections = {}
        biases = {}
        activation_functions = {}
        dominances = {}

        list_of_keys = list(functions_pool.keys())

        for index_of_layer in range(len(nodes_by_layer)) :
            if index_of_layer == 0 :
                previous_layer = nodes_by_layer[index_of_layer]
                continue
            current_layer = nodes_by_layer[index_of_layer]
            for node, previous_nodes in self._incoming_by_node(previous_layer, current_layer) :
                for previous_node in previous_nodes :
                    weight = self.config.range_weight * np.random.uniform(-1, 1)
                    connections[(previous_node, node)] = weight
                d = 1
                b = self.config.range_bias * np.random.uniform(-1, 1)
                c = np.random.randint(0, len(list_of_keys))
                act_function = functions_pool[list_of_keys[c]]
                biases[node] = b
                activation_functions[node] = act_function if index_of_layer != len(nodes_by_layer) - 1 else output_activation_function
                dominances[node] = d
            previous_layer = current_layer
        return connections, biases, activation_functions, dominances, nodes_by_layer

    def crossover_with_modu_regu(self, haploid, other_haploid) :

        connections = {}
        biases = {}
        functions = {}
        dominances = {}

        for index_of_layer in range(len(haploid.nodes)) :
            if index_of_layer == 0 :
                previous_layer = haploid.nodes[index_of_layer]
                continue

            current_layer = haploid.nodes[index_of_layer]

            for node, previous_nodes in self._incoming_by_node(previous_layer, current_layer) :
                if haploid.dominances[node] > other_haploid.dominances[node] :
                    biases[node] = copy.deepcopy(haploid.biases[node])
                    functions[node] = copy.deepcopy(haploid.functions[node])
                    dominances[node] = copy.deepcopy(haploid.dominances[node])
                    for previous_node in previous_nodes :
                        connections[(previous_node, node)] = copy.deepcopy(haploid.connections[(previous_node, node)])
                elif haploid.dominances[node] < other_haploid.dominances[node] :
                    biases[node] = copy.deepcopy(other_haploid.biases[node])
                    functions[node] = copy.deepcopy(other_haploid.functions[node])
                    dominances[node] = copy.deepcopy(other_haploid.dominances[node])
                    for previous_node in previous_nodes :
                        connections[(previous_node, node)] = copy.deepcopy(other_haploid.connections[(previous_node, node)])
                else :
                    choice = np.random.randint(0, 2)
                    if choice == 0 :
                        biases[node] = copy.deepcopy(haploid.biases[node])
                        functions[node] = copy.deepcopy(haploid.functions[node])
                        dominances[node] = copy.deepcopy(haploid.dominances[node])
                        for previous_node in previous_nodes :
                            connections[(previous_node, node)] = copy.deepcopy(haploid.connections[(previous_node, node)])
                    else :
                        biases[node] = copy.deepcopy(other_haploid.biases[node])
                        functions[node] = copy.deepcopy(other_haploid.functions[node])
                        dominances[node] = copy.deepcopy(other_haploid.dominances[node])
                        for previous_node in previous_nodes :
                            connections[(previous_node, node)] = copy.deepcopy(other_haploid.connections[(previous_node, node)])

            previous_layer = current_layer

        nodes = copy.deepcopy(haploid.nodes)

        return connections, biases, functions, dominances, nodes

    def cocrossover_with_modu_regu(self, haploid, other_haploid) :

        connections = {}
        biases = {}
        functions = {}
        dominances = {}

        for index_of_layer in range(len(haploid.nodes)) :
            if index_of_layer == 0 :
                previous_layer = haploid.nodes[index_of_layer]
                continue

            current_layer = haploid.nodes[index_of_layer]

            for node, previous_nodes in self._incoming_by_node(previous_layer, current_layer) :
                if haploid.dominances[node] > other_haploid.dominances[node] :
                    biases[node] = copy.deepcopy(haploid.biases[node])
                    functions[node] = copy.deepcopy(haploid.functions[node])
                    dominances[node] = copy.deepcopy(haploid.dominances[node])
                    for previous_node in previous_nodes :
                        connections[(previous_node, node)] = copy.deepcopy(haploid.connections[(previous_node, node)])
                elif haploid.dominances[node] < other_haploid.dominances[node] :
                    biases[node] = copy.deepcopy(other_haploid.biases[node])
                    functions[node] = copy.deepcopy(other_haploid.functions[node])
                    dominances[node] = copy.deepcopy(other_haploid.dominances[node])
                    for previous_node in previous_nodes :
                        connections[(previous_node, node)] = copy.deepcopy(other_haploid.connections[(previous_node, node)])
                else :
                    choice = np.random.randint(0, 2)
                    if choice == 0 :
                        functions[node] = copy.deepcopy(haploid.functions[node])
                        dominances[node] = copy.deepcopy(haploid.dominances[node])
                    else :
                        functions[node] = copy.deepcopy(other_haploid.functions[node])
                        dominances[node] = copy.deepcopy(other_haploid.dominances[node])

                    biases[node] = (copy.deepcopy(haploid.biases[node]) + copy.deepcopy(other_haploid.biases[node])) / 2
                    for previous_node in previous_nodes :
                        connections[(previous_node, node)] = (copy.deepcopy(haploid.connections[(previous_node, node)]) + copy.deepcopy(other_haploid.connections[(previous_node, node)])) / 2

            previous_layer = current_layer

        nodes = copy.deepcopy(haploid.nodes)

        return connections, biases, functions, dominances, nodes

    def mutate_with_modu_regu(self, genome, sigma_weight, sigma_bias, threshold_weight, threshold_bias, threshold_function, threshold_dominance, functions_pool) :
        output_nodes = [node for branch in genome.nodes[-1] for node in branch]

        for node in genome.connections :
            if np.random.uniform() < threshold_weight :
                genome.connections[node] += np.random.normal(loc = 0, scale = sigma_weight)
                if abs(genome.connections[node]) > self.config.max_weight_cppn :
                    genome.connections[node] = np.sign(genome.connections[node]) * self.config.max_weight_cppn

        for node in genome.biases :
            if np.random.uniform() < threshold_bias :
                genome.biases[node] += np.random.normal(loc = 0, scale = sigma_bias)
                if abs(genome.biases[node]) > self.config.max_bias_cppn :
                    genome.biases[node] = np.sign(genome.biases[node]) * self.config.max_bias_cppn

        list_of_keys = list(functions_pool.keys())
        for node in genome.functions :
            if node in output_nodes :
                continue
            if np.random.uniform() < threshold_function :
                choice = np.random.randint(0, len(list_of_keys))
                new_function = functions_pool[list_of_keys[choice]]
                while genome.functions[node] == new_function :
                    choice = np.random.randint(0, len(list_of_keys))
                    new_function = functions_pool[list_of_keys[choice]]
                genome.functions[node] = new_function

        for node in genome.dominances :
            if np.random.uniform() < threshold_dominance :
                choice = np.random.randint(1, self.config.number_of_dominances + 1)
                while genome.dominances[node] == choice :
                    choice = np.random.randint(1, self.config.number_of_dominances + 1)
                genome.dominances[node] = choice

        return genome







                


