import numpy as np


class PhenotypeBuilder :

    def __init__(self):
        pass 

    def _query_cppn_weight(self, cppn, network_manager, coordinate1, coordinate2, one_towards_two, max_weight) :
        if one_towards_two :
            inputs = [*coordinate1, *coordinate2]
        else :
            inputs = [*coordinate2, *coordinate1]

        output = network_manager.activate(cppn, inputs)

        weight = output 

        if abs(weight[0]) > 0.2 and abs(weight[0]) < max_weight:
            return weight[0]
        elif abs(weight[0]) >= max_weight :
            return max_weight if weight[0] > 0 else -max_weight
        else :
            return 0.0
        
    def _distance(self, coordinate1, coordinate2) :
        array1 = np.array(coordinate1)
        array2 = np.array(coordinate2)
        return np.linalg.norm(array1 - array2)


    def _query_cppn_weight_2_outputs(self, cppn, network_manager, coordinate1, coordinate2, one_towards_two, max_weight, type_output) :

        distance = self._distance(coordinate1, coordinate2)

        if one_towards_two :
            inputs = [*coordinate1, *coordinate2, distance]
        else :
            inputs = [*coordinate2, *coordinate1, distance]

        # if one_towards_two :
        #     inputs = [*coordinate1, *coordinate2]
        # else :
        #     inputs = [*coordinate2, *coordinate1]

        output = network_manager.activate(cppn, inputs)

        weight = output[type_output]

        if abs(weight) > 0.1 and abs(weight) < max_weight:
            return weight
        elif abs(weight) >= max_weight :
            return max_weight if weight > 0 else -max_weight
        else :
            return 0.0
        

    def _query_cppn_bias(self, cppn, network_manager, coordinate1, max_bias, coordinate2 = [0, 0, 0, 0, 0]) :
        inputs = [*coordinate1, *coordinate2]
        output = network_manager.activate(cppn, inputs)

        bias = output 
        if abs(bias[0]) > max_bias :
            bias = max_bias if bias[0] > 0 else -max_bias
            return bias
        return bias[0]
    
    def _connect_target_node_to_layer(self, cppn, network_manager, target_node_coordinates, source_layer_coordinates, node_dict, one_towards_two, max_weight, max_bias) : 
        incomming_connections = []
        for source_node_coordinate in source_layer_coordinates:
            weight = self._query_cppn_weight(cppn, network_manager, source_node_coordinate, target_node_coordinates, one_towards_two, max_weight)
            incomming_connections.append((node_dict[tuple(source_node_coordinate)], weight))
        bias = self._query_cppn_bias(cppn, network_manager, target_node_coordinates, max_bias)
        return incomming_connections, bias
    
    def _connect_target_node_to_layer_without_bias_2_outputs(self, cppn, network_manager, target_node_coordinates, source_layer_coordinates, node_dict, one_towards_two, max_weight, max_bias, type_output) : 
        incomming_connections = []
        for source_node_coordinate in source_layer_coordinates:
            weight = self._query_cppn_weight_2_outputs(cppn, network_manager, source_node_coordinate, target_node_coordinates, one_towards_two, max_weight, type_output)
            incomming_connections.append((node_dict[tuple(source_node_coordinate)], weight))
        bias = 0
        return incomming_connections, bias

    
    def create_phenotype_network(self, cppn, network_manager, all_layers_coordinates, activation_function, out_activation_function, agg, response, max_weight, max_bias) :
        node_dict = {}
        idx = 0
        for layer in all_layers_coordinates :
            for node in layer :
                node_dict[tuple(node)] = idx 
                idx += 1

        node_evals = []
        idx_current_source_layer = 0 
        for layer in all_layers_coordinates[1:] :
            source_layer = all_layers_coordinates[idx_current_source_layer]
            for hidden_node in layer :
                one_towards_two = True 
                incomming_connections, bias = self._connect_target_node_to_layer(cppn, network_manager, hidden_node, source_layer, node_dict, one_towards_two, max_weight, max_bias)
                act = out_activation_function if layer == all_layers_coordinates[-1] else activation_function
                node_evals.append(tuple( [node_dict[tuple(hidden_node)], act, agg, bias, response, incomming_connections] ))
            idx_current_source_layer += 1

        input_nodes = [node_dict[tuple(node_coor)] for node_coor in all_layers_coordinates[0]]
        output_nodes = [node_dict[tuple(node_coor)] for node_coor in all_layers_coordinates[-1]]

        return node_evals, input_nodes, output_nodes 
    
    


    def create_phenotype_network_without_bias_2_outputs(self, cppn, network_manager, all_layers_coordinates, activation_function, out_activation_function, agg, response, max_weight, max_bias, type_output) :
        
        node_dict = {}
        idx = 0
        for layer in all_layers_coordinates :
            for node in layer :
                node_dict[tuple(node)] = idx 
                idx += 1

        node_evals = []
        idx_current_source_layer = 0 
        for layer in all_layers_coordinates[1:] :
            source_layer = all_layers_coordinates[idx_current_source_layer]
            for hidden_node in layer :
                one_towards_two = True 
                incomming_connections, bias = self._connect_target_node_to_layer_without_bias_2_outputs(cppn, network_manager, hidden_node, source_layer, node_dict, one_towards_two, max_weight, max_bias, type_output)
                act = out_activation_function if layer == all_layers_coordinates[-1] else activation_function
                node_evals.append(tuple( [node_dict[tuple(hidden_node)], act, agg, bias, response, incomming_connections] ))
            idx_current_source_layer += 1

        input_nodes = [node_dict[tuple(node_coor)] for node_coor in all_layers_coordinates[0]]
        output_nodes = [node_dict[tuple(node_coor)] for node_coor in all_layers_coordinates[-1]]

        return node_evals, input_nodes, output_nodes 
     


