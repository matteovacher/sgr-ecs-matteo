import os
import json  
import time
import imageio as io 

from config import Config 

from entity_manager import EntityManager 
from world import World 


from tools.network_manager import NetworkManager
from tools.func_pool import FunctionPool
from tools.genome_operator import GenomeOperator, HaploidOperator
from tools.hyper_encoding import PhenotypeBuilder
from tools.parallel_tool import ParallelTool
from tools.results_manager import ResultsManager
from tools.robot_generator import RobotGenerator
from tools.robot_simulator import RobotSimulator
from tools.substrate import SubstrateBuilder
from tools.distance import DistanceTool


from systems.build_system import BothBuildSystem
from systems.phenotype_system import BothPhenotypeSystem
from systems.evaluation_system import BothEvaluationSystem
from systems.save_gen_system import BothSaveGenSystem
from systems.reproduction_system import BothReproductionSystem
from systems.save_system import BothSaveSystem

def main() : 
    # first exp with diploidy 

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
    substrate_builder = SubstrateBuilder(config)
    phenotype_builder = PhenotypeBuilder()
    robot_generator = RobotGenerator()
    robot_simulator = RobotSimulator(config)
    parallel_tool = ParallelTool(config)

    results_manager.add_results_both_path()

    type_genome = "diploid"

    time1 = time.time()

    genome_operator = GenomeOperator(config)

    build_system = BothBuildSystem(config, entity_manager, genome_operator, results_manager, function_pool, type_genome)
    phenotype_system = BothPhenotypeSystem(config, entity_manager, genome_operator, network_manager, substrate_builder, phenotype_builder, function_pool, robot_generator, robot_simulator, results_manager, type_genome)
    evaluation_system = BothEvaluationSystem(config, robot_simulator, network_manager, parallel_tool, entity_manager, results_manager, type_genome)
    save_gen_system = BothSaveGenSystem(config, results_manager, type_genome)
    reproduction_system = BothReproductionSystem(config, genome_operator, entity_manager, function_pool, results_manager, type_genome)
    save_system = BothSaveSystem(config, results_manager, type_genome)

    
    world.add_builder_system(build_system)
    world.add_step_system(phenotype_system)
    world.add_step_system(evaluation_system)
    world.add_step_system(save_gen_system)
    world.add_step_system(reproduction_system)

    world.add_end_system(save_system)
    
    results_manager.begin_both_txt_file(world.all_systems)

    world.build()
    for generation in range(config.generations) :
        world.step()
    world.end()

    time2 = time.time()
    total_time = time2 - time1
    print("Total time : ", time2 - time1)

    world.reset()

    type_genome = 'haploid'

    time1 = time.time()

    genome_operator = HaploidOperator(config)

    build_system = BothBuildSystem(config, entity_manager, genome_operator, results_manager, function_pool, type_genome)
    phenotype_system = BothPhenotypeSystem(config, entity_manager, genome_operator, network_manager, substrate_builder, phenotype_builder, function_pool, robot_generator, robot_simulator, results_manager, type_genome)
    evaluation_system = BothEvaluationSystem(config, robot_simulator, network_manager, parallel_tool, entity_manager, results_manager, type_genome)
    save_gen_system = BothSaveGenSystem(config, results_manager, type_genome)
    reproduction_system = BothReproductionSystem(config, genome_operator, entity_manager, function_pool, results_manager, type_genome)
    save_system = BothSaveSystem(config, results_manager, type_genome)

    world.add_builder_system(build_system)
    world.add_step_system(phenotype_system)
    world.add_step_system(evaluation_system)
    world.add_step_system(save_gen_system)
    world.add_step_system(reproduction_system)

    world.add_end_system(save_system)

    results_manager.begin_both_txt_file(world.all_systems)

    world.build()
    for generation in range(config.generations) :
        world.step()
    world.end()

    time2 = time.time()
    print("Total time : ", time2 - time1)

    print('Whole simulations took : ', time2 - time1 + total_time)
    

def render() :
    pass