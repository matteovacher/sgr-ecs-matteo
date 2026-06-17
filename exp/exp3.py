import os 
import json 
import time 
import imageio as io 

from entity_manager import EntityManager 
from tools.distance import DistanceTool 
from world import World 
from systems.build_system import HaploidBuildSystem
from systems.evaluation_system import HaploidEvaluationSystem
from systems.reproduction_system import HaploidReproductionSystem
from systems.phenotype_system import HaploidPhenotypeSystem
from systems.save_system import SaveSystem
from systems.save_gen_system import HaploidSaveGenSystem

from config import Config 

from tools.network_manager import NetworkManager
from tools.func_pool import FunctionPool
from tools.genome_operator import HaploidOperator
from tools.hyper_encoding import PhenotypeBuilder
from tools.parallel_tool import ParallelTool
from tools.results_manager import ResultsManager
from tools.robot_generator import RobotGenerator
from tools.robot_simulator import RobotSimulator
from tools.substrate import SubstrateBuilder


def main() :

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
    haploid_operator = HaploidOperator(config)
    substrate_builder = SubstrateBuilder(config)
    phenotype_builder = PhenotypeBuilder()
    robot_generator = RobotGenerator()
    robot_simulator = RobotSimulator(config)
    parallel_tool = ParallelTool(config)

    build_system = HaploidBuildSystem(config, entity_manager, haploid_operator, results_manager, function_pool)
    phenotype_system = HaploidPhenotypeSystem(config, entity_manager, haploid_operator, network_manager, substrate_builder, phenotype_builder, function_pool, robot_generator, robot_simulator, results_manager)
    evaluation_system = HaploidEvaluationSystem(config, robot_simulator, network_manager, parallel_tool, entity_manager, results_manager)
    save_gen_system = HaploidSaveGenSystem(config, results_manager)
    reproduction_system = HaploidReproductionSystem(config, haploid_operator, entity_manager, function_pool, results_manager)
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
    print (f"Total time: {time2-time1} s")

def render() :

    results_manager = ResultsManager()
    exit = results_manager.loader()
    config = Config(results_manager.configs)
    network_manager = NetworkManager(config)
    robot_simulator = RobotSimulator(config)
    distance_tool = DistanceTool(config)

    while exit == False :
        action = results_manager.ask_haploid_action()
        if action == 'bodies' : 
            exit = results_manager.print_bodies()
        elif action == 'render' :
            exit, gen, id = results_manager.load_ind()

            gen, id = int(gen), int(id)
            key = (gen, id)

            video_dir = os.path.join(results_manager.results_dir, 'video')
            os.makedirs(video_dir, exist_ok=True)

            video_mp4_path = os.path.join(video_dir, 'gen_{}_id_{}.mp4'.format(gen, id))
            video_gif_path = os.path.join(video_dir, 'gen_{}_id_{}.gif'.format(gen, id))

            print('\n----- Simulating the simulation -----\n')
            name_body = '{}_body_registry'.format(gen)
            name_controller_network = '{}_controller_network_registry'.format(gen)
            body_registry = getattr(results_manager, name_body)
            controller_network_registry = getattr(results_manager, name_controller_network)
            body = body_registry[key]
            controller_network = controller_network_registry[key]

            images, _ = robot_simulator.simulate_render(body.body, controller_network, network_manager, config.n_steps)

            print('\n----- Rendering the simulation -----\n')
            io.mimwrite(video_mp4_path, images, fps=30, macro_block_size=1)

            print('\n----- Saved Successfully -----\n')

        elif action == "haploid genealogy" :
            exit = results_manager.explore_haploid_genealogy()

        elif action == 'body' :
            exit = results_manager.print_body()

        elif action == 'render haploid genealogy' :
            exit, gen, id, genealogy = results_manager.render_haploid_family()
            video_dir = os.path.join(results_manager.results_dir, 'video')
            family_video_dir = os.path.join(video_dir, 'family', 'gen_{}_id_{}'.format(gen, id))
            os.makedirs(family_video_dir, exist_ok=True)

            for i in range(len(genealogy)) :
                cur_gen = gen - i
                for indi in genealogy[i] :
                    video_mp4_path = os.path.join(family_video_dir, 'gen_{}_id_{}.mp4'.format(cur_gen, indi))
                    video_gif_path = os.path.join(family_video_dir, 'gen_{}_id_{}.gif'.format(cur_gen, indi))

                    print('\n----- Simulating the simulation -----\n')

                    name_body = '{}_body_registry'.format(cur_gen)
                    name_controller_network = '{}_controller_network_registry'.format(cur_gen)
                    body_registry = getattr(results_manager, name_body)
                    controller_network_registry = getattr(results_manager, name_controller_network)
                    body = body_registry[(cur_gen, indi)]
                    controller_network = controller_network_registry[(cur_gen, indi)]
                
                    images, _ = robot_simulator.simulate_render(body.body, controller_network, network_manager, config.n_steps)
                    
                    io.mimwrite(video_mp4_path, images, fps=30, macro_block_size=1)
                   
                    print('\n----- Saved Successfully -----\n')
        
        elif action == 'save haploid family' :
            exit, gen, id, genealogy = results_manager.save_haploid_family()
            images_dir = os.path.join(results_manager.results_dir, 'images')
            family_images_dir = os.path.join(images_dir, 'family')
            os.makedirs(family_images_dir, exist_ok=True)

            gam_gen_dir = os.path.join(family_images_dir, 'gen_{}_id_{}'.format(gen, id))
            os.makedirs(gam_gen_dir, exist_ok=True)

            for i in range(len(genealogy)) :
                cur_gen = gen - i
                for indi in genealogy[i] :
                    image_path = os.path.join(gam_gen_dir, 'gen_{}_id_{}.png'.format(cur_gen, indi))

                    name_body = '{}_body_registry'.format(cur_gen)
                    body_registry = getattr(results_manager, name_body)
                    body = body_registry[(cur_gen, indi)]

                
                    image = robot_simulator.simulate_render_image(body.body)
                    io.imwrite(image_path, image)
        
        elif action == 'save individual' :
            exit, gen, id = results_manager.save_body()
            images_dir = os.path.join(results_manager.results_dir, 'images')

            os.makedirs(images_dir, exist_ok=True)

            image_path = os.path.join(images_dir, 'gen_{}_{}.png'.format(gen, id))


            name_body = '{}_body_registry'.format(gen)
            body_registry = getattr(results_manager, name_body)
            body = body_registry[(gen, id)]

            image = robot_simulator.simulate_render_image(body.body)
            io.imwrite(image_path, image)
        
        elif action == 'distance' :
            exit = results_manager.print_distance(distance_tool)

        else :
            exit = True
    
    print('\n----- Exiting -----\n')







