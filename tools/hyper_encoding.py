


class PhenotypeBuilder :

    def __init__(self):
        pass 

    def _query_cppn_weight(self, cppn, coordinate1, coordinate2, one_towards_two, max_weight, bias = 1.0) :
        if one_towards_two :
            inputs = [*coordinate1, *coordinate2, bias]
        else :
            inputs = [*coordinate2, *coordinate1, bias]

        output = cppn.activate(cppn, inputs)

        weight = output 

        if abs(weight) > 0.2 and abs(weight) < max_weight:
            return weight
        else :
            return 0.0
        

    def _query_cppn_bias(self, cppn, coordinate1, coordinate2 = [0, 0, 0, 0], bias = 1.0) :

        inputs = [*coordinate1, *coordinate2, bias]
        output = cppn.activate(cppn, inputs)

        bias = output 

        return bias
    
    def _connect_target_node_to_layer(self, cppn, target_node_coordinates, source_layer_coordinates, node_dict, one_towards_two, max_weight) : 
        incomming_connections = []
        for source_node_coordinate in source_layer_coordinates:
            weight = self._query_cppn_weight(cppn, source_node_coordinate, target_node_coordinates, one_towards_two, max_weight)
            incomming_connections.append((node_dict(tuple(source_node_coordinate)), weight ))
        bias = self._query_cppn_bias(cppn, target_node_coordinates)
        return incomming_connections, bias
    
    def create_phenotype_network(self, cppn, all_layers_coordinates, activation_function, out_activation_function, agg, response, max_weight) :
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
                incomming_connections, bias = self._connect_target_node_to_layer(cppn, hidden_node, source_layer, node_dict, one_towards_two, max_weight)
                act = out_activation_function if layer == all_layers_coordinates[-1] else activation_function
                node_evals.append(tuple( [node_dict[tuple(hidden_node)], act, agg, bias, response, incomming_connections] ))
            idx_current_source_layer += 1

        input_nodes = [node_dict[tuple(node_coor)] for node_coor in all_layers_coordinates[0]]
        output_nodes = [node_dict[tuple(node_coor)] for node_coor in all_layers_coordinates[-1]]

        return node_evals, input_nodes, output_nodes 



     


