import os 
import json
import numpy as np 
from config import Config

from tools.distance import DistanceTool
from tools.substrate import SubstrateBuilder
from tools.genome_operator import GenomeOperator
from tools.func_pool import FunctionPool


config_path = "tests/testconfig.json"
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


def test_init(config) :
    genome = GenomeOperator(config)
    nodes_by_layer = genome.nodes_by_layer_with_modu_regu(config.shape_of_cppn)

    print(nodes_by_layer)


def test_build_init(config) :
    genome = GenomeOperator(config)
    nodes_by_layer = genome.nodes_by_layer_with_modu_regu(config.shape_of_cppn)
    function_pool = FunctionPool(config)
    connections1, connections2, bias1, bias2, activation_functions1, activation_functions2, dominance1, dominance2 = genome.generate_first_generation_of_genome_with_modu_regu(nodes_by_layer, function_pool.pool)
    print(connections1)
    print(connections2)
    print(bias1)
    print(bias2)
    print(activation_functions1)
    print(activation_functions2)
    print(dominance1)
    print(dominance2)

def test_dom(config) :
    genome = GenomeOperator(config)
    nodes_by_layer = genome.nodes_by_layer_with_modu_regu(config.shape_of_cppn)
    function_pool = FunctionPool(config)
    connections1, connections2, bias1, bias2, activation_functions1, activation_functions2, dominance1, dominance2 = genome.generate_first_generation_of_genome_with_modu_regu(nodes_by_layer, function_pool.pool)

if __name__ == "__main__":
    test_build_init(config)


