import numpy as np 



class DistanceTool : 

    def __init__(self, config) :
        self.config = config 

    def phenotypic_body_distance(self, body1, body2) :
        distance = 0
        for i in range(len(body1)) :
            for j in range(len(body1[0])) : 
                if body1[i][j] == body2[i][j] :
                    diff = 0
                elif (body1[i][j] == 0 and body2[i][j] != body1[i][j]) or (body2[i][j] == 0 and body2[i][j] != body1[i][j]) :
                    diff = 1
                else :
                    diff = 0.5 
                distance += diff 
        return distance, distance/(len(body1)*len(body1[0]))

    def gravity_center_pos(self, positions) :
        mean = positions.mean(axis = 0)
        return mean 
    # return the vector [xmean, ymean]

    
    def velocity(self, velocities) :
        velocity = velocities.mean(axis=0)
        return velocity

    def velocity_orientations(self, orientations) :
        velocity_orientation = [0]
        for i in range(1, len(orientations)) :
            velocity_orientation.append(orientations[i] - orientations[i-1])
        return np.array(velocity_orientation)

    def phenotypic_behavior_distance(self, mean_positions1, mean_velocities1, velocity_orientations1, mean_positions2, mean_velocities2, velocity_orientations2) :
        distance_pos = 0 
        for i in range(len(mean_positions1)) :
            distance_pos += np.linalg.norm(mean_positions1[i] - mean_positions2[i])
        distance_vel = 0
        for i in range(len(mean_velocities1)) :
            distance_vel += np.linalg.norm(mean_velocities1[i] - mean_velocities2[i])
        distance_vel_ori = 0
        for i in range(len(velocity_orientations1)) :
            distance_vel_ori += np.linalg.norm(velocity_orientations1[i] - velocity_orientations2[i])
        return distance_pos, distance_vel, distance_vel_ori
    
    def distance_expressed_genome(self, node_evals1, node_evals2) :
        act_functions_distance = 0 
        weight_distance = 0 
        bias_distance = 0

        count_weight = 0 
        count_bias = 0 
        weight_distance = 0


        for node_eval1, node_eval2 in zip(node_evals1, node_evals2) :
            node1, activation_function1, agregation_function1, bias1, response1, inputs_of_node1 = node_eval1
            node2, activation_function2, agregation_function2, bias2, response2, inputs_of_node2 = node_eval2
            list_of_weight1 = [weight for previous_node, weight in inputs_of_node1]
            list_of_weight2 = [weight for previous_node, weight in inputs_of_node2]
            
            for weight1, weight2 in zip(list_of_weight1, list_of_weight2) :
                weight_distance += np.linalg.norm(np.array(weight1) - np.array(weight2))

            count_weight += len(list_of_weight1)
            count_bias += 1

            bias_distance += np.linalg.norm(np.array(bias1) - np.array(bias2))
            act_functions_distance += 0 if activation_function1 is activation_function2 else 1


        number_of_nodes = sum(self.config.shape_of_cppn[1:])

        normnalized_act_functions_distance = act_functions_distance / number_of_nodes
        normalized_weight_distance = weight_distance / (count_weight * 2 * self.config.range_weight)
        normalized_bias_distance = bias_distance / (count_bias * 2 * self.config.range_bias)

        

    
        return act_functions_distance, weight_distance, bias_distance, normnalized_act_functions_distance, normalized_weight_distance, normalized_bias_distance


            
                
