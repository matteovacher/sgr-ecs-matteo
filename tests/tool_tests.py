import os 
import json

from config import Config

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
    print(shape)
    substrate = substrate_builder.shape_into_coordinates(shape)
    print(substrate)
    print(len(substrate))
    print(len(substrate[-1]))
    shape = substrate_builder.extract_controller_network_shape(3, config)
    print(shape)
    substrate = substrate_builder.shape_into_coordinates(shape)
    print(substrate)
    print(len(substrate))
    print(len(substrate[-1]))


if __name__ == "__main__":
    test_substrate_builder(config)


