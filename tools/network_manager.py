


class NetworkManager :
    def __init__(self, config) :
        self.config = config


    def create_network(self, nodes_by_layer, connections, bias, functions, agg, response) :
        node_evals = []
        for index_of_layer in range(len(nodes_by_layer)) :
            
            if index_of_layer ==  0 :
                input_nodes = []
                for input_node in nodes_by_layer[index_of_layer] :
                    input_nodes.append(input_node)
                previous_layer = nodes_by_layer[index_of_layer]
                continue 

            if index_of_layer == len(nodes_by_layer) - 1 :
                output_nodes = []
                for output_node in nodes_by_layer[index_of_layer] :
                    output_nodes.append(output_node)

            for node in nodes_by_layer[index_of_layer] :
                inputs_of_node = []
                for previous_node in previous_layer :
                    weight = connections[(previous_node, node)]
                    inputs_of_node.append((previous_node, weight))
                activation_function = functions[node]
                node_bias = bias[node]
                node_evals.append((node, activation_function, agg, node_bias, response, inputs_of_node))
            
            previous_layer = nodes_by_layer[index_of_layer]

        return node_evals, input_nodes, output_nodes


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


    def create_network_with_modu_regu(self, nodes_by_layer, connections, bias, functions, agg, response) :
        node_evals = []
        input_nodes = [node for node in nodes_by_layer[0][0]]
        output_nodes = [node for branch in nodes_by_layer[-1] for node in branch]

        for index_of_layer in range(len(nodes_by_layer)) :
            if index_of_layer == 0 :
                previous_layer = nodes_by_layer[index_of_layer]
                continue

            current_layer = nodes_by_layer[index_of_layer]
            for node, previous_nodes in self._incoming_by_node(previous_layer, current_layer) :
                inputs_of_node = []
                for previous_node in previous_nodes :
                    weight = connections[(previous_node, node)]
                    inputs_of_node.append((previous_node, weight))
                activation_function = functions[node]
                node_bias = bias[node]
                node_evals.append((node, activation_function, agg, node_bias, response, inputs_of_node))

            previous_layer = current_layer

        return node_evals, input_nodes, output_nodes




    def activate(self, network, inputs):
        values = {}
        for key, value in zip(network.input_nodes, inputs) : 
            values[key] = value
        
        for node, activation_function, agregation_function, bias, response, inputs_of_node in network.node_evals : 
            node_inputs = []
            for previous_node, weight in inputs_of_node : 
                node_inputs.append(values[previous_node] * weight)
            entering_node = agregation_function(node_inputs)
            values[node] = activation_function(bias + response * entering_node)
        return [values[node] for node in network.output_nodes]
    



    