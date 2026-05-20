import numpy as np 

from evogym import is_connected, has_actuator, get_full_connectivity 

class RobotGenerator :

    TYPES_OF_VOXELS = ["empty", "rigid", "soft", "horizontal", "vertical"]

    def __init__(self) :
        pass

    def generate_robot_body_from_network(self, body_network, network_manager, body_shape) :
        body_outputs = network_manager.activate(body_network, [np.pi])
        formated = np.reshape(body_outputs, (body_shape[0], body_shape[1], len(self.TYPES_OF_VOXELS)))
        robot = np.argmax(formated, 2)
        return robot
    
    def is_valid_robot(self, robot) :
        return is_connected(robot) and has_actuator(robot)
    
    def get_full_connectivity(self, robot) :
        return get_full_connectivity(robot)