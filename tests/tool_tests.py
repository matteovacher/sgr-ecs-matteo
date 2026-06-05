import os 
import json
import numpy as np 
from config import Config

from tools.distance import DistanceTool
from tools.substrate import SubstrateBuilder


config_path = "tests/config.json"
local_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path_final = os.path.join(local_dir, "configs", config_path)
with open(config_path_final, 'r') as f : 
    config = json.load(f)


config = Config(config)


def test_substrate_builder(config):
    substrate_builder = SubstrateBuilder(config)
    shape = substrate_builder.extract_body_network_shape_test(config)

    substrate = substrate_builder.shape_into_coordinates(shape)
    print(substrate)
    print(len(substrate))
    for layer in substrate :
        print(len(layer))
    shape = substrate_builder.extract_controller_network_shape(3, config)

    substrate = substrate_builder.shape_into_coordinates(shape)
    

    shape = substrate_builder.extract_controller_network_shape(2, config)
    substrate = substrate_builder.shape_into_coordinates(shape)
    print(substrate)
    print(len(substrate))
    for layer in substrate :
        print(len(layer))

def test_grav(config) :
    distance_tool = DistanceTool(config)
    positions = np.array([[0,0], [1,3], [2,1], [3,4], [4,2], [5,3]])
    gravity_center = distance_tool.gravity_center_pos(positions)
    ori = [0, 0.5, 1, 2, 3, 2]
    velocity_ori = distance_tool.velocity_orientations(ori)
    print(velocity_ori)
    print(gravity_center)

if __name__ == "__main__":
    test_substrate_builder(config)


