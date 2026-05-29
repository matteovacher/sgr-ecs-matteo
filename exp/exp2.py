import os
import json  
import time

from entity_manager import EntityManager 
from world import World 
from systems.build_system import BuildSystem
from systems.evaluation_system import EvaluationSystem
from systems.reproduction_system import ReproductionSystem
from systems.phenotype_system import PhenotypeSystem
from systems.save_system import SaveSystem
from systems.save_gen_system import SaveGenSystem

from config import Config

from tools.network_manager import NetworkManager
from tools.func_pool import FunctionPool
from tools.genome_operator import GenomeOperator
from tools.hyper_encoding import PhenotypeBuilder
from tools.parallel_tool import ParallelTool
from tools.results_manager import ResultsManager
from tools.robot_generator import RobotGenerator
from tools.robot_simulator import RobotSimulator
from tools.substrate import SubstrateBuilder






def main():
    time1 = time.time()
    entity_manager = EntityManager()
    world = World()


    config_path = input("\nEnter the path to the config file from the configs folder (can be just config.json) : ")
    local_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path_final = os.path.join(local_dir, "configs", config_path)
    with open(config_path_final, 'r') as f : 
        config = json.load(f)

    config = Config(config)

    results_manager = ResultsManager()
    network_manager = NetworkManager(config)
    function_pool = FunctionPool(config)
    genome_operator = GenomeOperator(config)
    substrate_builder = SubstrateBuilder(config)
    phenotype_builder = PhenotypeBuilder()
    robot_generator = RobotGenerator()
    robot_simulator = RobotSimulator(config)
    parallel_tool = ParallelTool(config)


    build_system = BuildSystem(config, entity_manager, genome_operator, results_manager, function_pool)
    phenotype_system = PhenotypeSystem(config, entity_manager, genome_operator, network_manager, substrate_builder, phenotype_builder, function_pool, robot_generator, robot_simulator, results_manager)
    evaluation_system = EvaluationSystem(config, robot_simulator, network_manager, parallel_tool, entity_manager, results_manager)
    save_gen_system = SaveGenSystem(config, results_manager)
    reproduction_system = ReproductionSystem(config, genome_operator, entity_manager, function_pool, results_manager)
    save_system = SaveSystem(config, results_manager)

    world.add_builder_system(build_system)
    world.add_step_system(phenotype_system)
    world.add_step_system(evaluation_system)
    world.add_step_system(save_gen_system)
    world.add_step_system(reproduction_system)
    world.add_end_system(save_system)

    results_manager.add_results_path()
    results_manager.begin_txt_file(world.all_systems)

    world.build()

    for generation in range(config.generations) : 
        world.step()

    world.end()

    time2 = time.time()
    passed = time2 - time1
    print(f'YOUR SIMULATION TOOK {passed:.3f} s.')
