import numpy as np 

from evogym import is_connected, has_actuator, get_full_connectivity 

class RobotGenerator :

    TYPES_OF_VOXELS = ["empty", "rigid", "soft", "horizontal", "vertical"]

    def __init__(self) :
        pass

    def generate_robot_body_from_network(self, body_network, network_manager, body_shape) :
        robot = np.zeros((body_shape[0], body_shape[1]))
        horizontal = np.linspace(-1, 1, body_shape[0])
        vertical = np.linspace(-1, 1, body_shape[1])
        bias = 0.5
        for i in range(body_shape[0]) :
            for j in range(body_shape[1]) :
                inputs = [horizontal[i], bias, vertical[j]]
                outputs = network_manager.activate(body_network, inputs)
                robot[i, j] = np.argmax(outputs)
        return robot

    def generate_former_robot_body_from_network(self, body_network, network_manager, body_shape) :
        bias = 0.5
        body_outputs = network_manager.activate(body_network, [bias])
        formated = np.reshape(body_outputs, (body_shape[0], body_shape[1], len(self.TYPES_OF_VOXELS)))
        robot = np.argmax(formated, 2)
        return robot
    
    def is_valid_robot(self, robot) :
        return (is_connected(robot)and has_actuator(robot)and np.count_nonzero(robot) >= 4)
    
    def get_full_connectivity(self, robot) :
        return get_full_connectivity(robot)
    
    # def generate_robot_body_from_network_and_env(self, body_network, network_manager, body_shape, type_env) :
    #     if type_env == 0 : 
    #         body_outputs = network_manager.activate(body_network, [- np.pi])
    #     elif type_env == 1 : 
    #         body_outputs = network_manager.activate(body_network, [np.pi])
    #     else : 
    #         raise Exception("type_env must be 0 or 1")
    #     formated = np.reshape(body_outputs, (body_shape[0], body_shape[1], len(self.TYPES_OF_VOXELS)))
    #     robot = np.argmax(formated, 2)
    #     return robot

    def generate_robot_body_from_network_and_env(self, body_network, network_manager, body_shape, type_env) :
        bias = 0.5
        if type_env == 0 : 
            robot = np.zeros((body_shape[0], body_shape[1]))
            horizontal = np.linspace(-1, 1, body_shape[0])
            vertical = np.linspace(-1, 1, body_shape[1])
            for i in range(body_shape[0]) :
                for j in range(body_shape[1]) :
                    inputs = [horizontal[i], bias, vertical[j]]
                    outputs = network_manager.activate(body_network, inputs)
                    robot[i, j] = np.argmax(outputs)
        elif type_env == 1 :
            robot = np.zeros((body_shape[0], body_shape[1]))
            horizontal = np.linspace(-1, 1, body_shape[0])
            vertical = np.linspace(-1, 1, body_shape[1])
            for i in range(body_shape[0]) :
                for j in range(body_shape[1]) :
                    inputs = [horizontal[i], - bias, vertical[j]]
                    outputs = network_manager.activate(body_network, inputs)
                    robot[i, j] = np.argmax(outputs)
        return robot
    
    def generate_former_robot_body_from_network_and_env(self, body_network, network_manager, body_shape, type_env) :
        bias = 0.5
        if type_env == 0 : 
            body_outputs = network_manager.activate(body_network, [bias])
            formated = np.reshape(body_outputs, (body_shape[0], body_shape[1], len(self.TYPES_OF_VOXELS)))
            robot = np.argmax(formated, 2)
        elif type_env == 1 :
            body_outputs = network_manager.activate(body_network, [- bias])
            formated = np.reshape(body_outputs, (body_shape[0], body_shape[1], len(self.TYPES_OF_VOXELS)))
            robot = np.argmax(formated, 2)
        return robot