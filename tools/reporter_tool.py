import numpy as np 

from evogym import is_connected, has_actuator, get_full_connectivity 

class RobotGenerator :

    TYPES_OF_VOXELS = ["empty", "rigid", "soft", "horizontal", "vertical"]

    def __init__(self, )