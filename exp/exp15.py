import os
import json  
import time
import imageio as io 
import copy 

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


from systems.build_system import Both0initModularBuildSystem
from systems.phenotype_system import BothEnvNewModular2WiBiPhenotypeSystem
from systems.evaluation_system import BothEnvEvaluationSystem
from systems.save_gen_system import BothSaveGenSystem
from systems.reproduction_system import BothModularReproductionSystem
from systems.save_system import BothSaveSystem

# with changing environment and for several exp or not on substrate 3d and with random choose if tie in dominance 

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

    whole_time = time.time()

    for k in range(config.number_of_config) :
        if k != 0 :
            config.threshold_weight = config.threshold_weight + config.threshold_var

        network_manager = NetworkManager(config)
        function_pool = FunctionPool(config)
        substrate_builder = SubstrateBuilder(config)
        phenotype_builder = PhenotypeBuilder()
        robot_generator = RobotGenerator()
        robot_simulator = RobotSimulator(config)
        parallel_tool = ParallelTool(config)



        for i in range(config.number_of_exp) : 
            if i == 0 and k == 0:
                results_manager.add_results_both_path()
            else : 
                number = int(results_manager.number) + 1 
                results_manager.set_both_path(results_manager.path, number)

            type_genome = "diploid"
            type_env = 0

            time1 = time.time()

            genome_operator = GenomeOperator(config)

            build_system = Both0initModularBuildSystem(config, entity_manager, genome_operator, results_manager, function_pool, type_genome)
            phenotype_system = BothEnvNewModular2WiBiPhenotypeSystem(config, entity_manager, genome_operator, network_manager, substrate_builder, phenotype_builder, function_pool, robot_generator, robot_simulator, results_manager, type_genome, type_env)
            evaluation_system = BothEnvEvaluationSystem(config, robot_simulator, network_manager, parallel_tool, entity_manager, results_manager, type_genome, type_env)
            save_gen_system = BothSaveGenSystem(config, results_manager, type_genome)
            reproduction_system = BothModularReproductionSystem(config, genome_operator, entity_manager, function_pool, results_manager, type_genome)
            save_system = BothSaveSystem(config, results_manager, type_genome)

            
            world.add_builder_system(build_system)
            world.add_step_system(phenotype_system)
            world.add_step_system(evaluation_system)
            world.add_step_system(save_gen_system)
            world.add_step_system(reproduction_system)

            world.add_end_system(save_system)

            for gen in range(1, config.generations + 1) :
                new_env = 0 if (gen//config.switch) % 2 == 0 else 1 
                phenotype_system.switched = (new_env != phenotype_system.type_env)
                phenotype_system.type_env = new_env
                evaluation_system.type_env = new_env

                if gen == 1 : 
                    results_manager.begin_both_env_txt_file(world.all_systems, type_genome, gen)
                    exp_name = __name__
                    results_manager.add_exp_name(exp_name, type_genome)
                    world.build()
                
                world.step()
            
            world.end()

            time2 = time.time()
            total_time = time2 - time1
            print("Total time : ", time2 - time1)

            world.reset()
            # entity_manager.reset()
            # not reset yet because i want to see if my render works and for that i need diff id for entities 

            type_genome = 'haploid'
            type_env = 0

            time1 = time.time()

            genome_operator = HaploidOperator(config)

            build_system = Both0initModularBuildSystem(config, entity_manager, genome_operator, results_manager, function_pool, type_genome)
            phenotype_system = BothEnvNewModular2WiBiPhenotypeSystem(config, entity_manager, genome_operator, network_manager, substrate_builder, phenotype_builder, function_pool, robot_generator, robot_simulator, results_manager, type_genome, type_env)
            evaluation_system = BothEnvEvaluationSystem(config, robot_simulator, network_manager, parallel_tool, entity_manager, results_manager, type_genome, type_env)
            save_gen_system = BothSaveGenSystem(config, results_manager, type_genome)
            reproduction_system = BothModularReproductionSystem(config, genome_operator, entity_manager, function_pool, results_manager, type_genome)
            save_system = BothSaveSystem(config, results_manager, type_genome)

            world.add_builder_system(build_system)
            
            world.add_step_system(phenotype_system)
            world.add_step_system(evaluation_system)
            world.add_step_system(save_gen_system)
            world.add_step_system(reproduction_system)

            world.add_end_system(save_system)

            for gen in range(1, config.generations + 1) :
                new_env = 0 if (gen//config.switch) % 2 == 0 else 1 
                phenotype_system.switched = (new_env != phenotype_system.type_env)
                phenotype_system.type_env = new_env
                evaluation_system.type_env = new_env

                if gen == 1 : 
                    results_manager.begin_both_env_txt_file(world.all_systems, type_genome, gen)
                    exp_name = __name__
                    results_manager.add_exp_name(exp_name, type_genome)
                    world.build()
                
                world.step()
            world.end()

            time2 = time.time()
            print("Total time : ", time2 - time1)

            print('Whole simulations took : ', time2 - time1 + total_time)
            world.reset()
            entity_manager.reset()
        world.reset()
    print('All simulations took : ', time.time() - whole_time)
        

def render() : 

    results_manager = ResultsManager()
    exit = results_manager.both_loader()

    diploid_config = Config(copy.deepcopy(results_manager.config_diploid))
    haploid_config = Config(copy.deepcopy(results_manager.config_haploid))

    haploid_network_manager = NetworkManager(haploid_config)
    diploid_network_manager = NetworkManager(diploid_config)

    diploid_robot_simulator = RobotSimulator(diploid_config)
    haploid_robot_simulator = RobotSimulator(haploid_config)

    diploid_distance_tool = DistanceTool(diploid_config)
    haploid_distance_tool = DistanceTool(haploid_config)

    while exit == False : 
        type_genome, action = results_manager.ask_both_action()

        if type_genome == 'diploid' :
            robot_simulator = diploid_robot_simulator
            network_manager = diploid_network_manager
            distance_tool = diploid_distance_tool
            config = diploid_config
        elif type_genome == 'haploid' :
            robot_simulator = haploid_robot_simulator
            network_manager = haploid_network_manager
            distance_tool = haploid_distance_tool
            config = haploid_config
        else :
            raise Exception('The type of genome is not valid')

        if action == 'bodies' :
            exit = results_manager.print_both_bodies(type_genome)
        
        elif action == 'render' :
            exit, gen, id = results_manager.load_both_ind(type_genome)

            gen, id = int(gen), int(id)
            key = (gen, id)

            if (gen//config.switch) % 2 == 0 :
                type_env = 0
            else :
                type_env = 1

            video_dir = os.path.join(results_manager.results_dir, type_genome, 'video')
            os.makedirs(video_dir, exist_ok=True)

            video_mp4_path = os.path.join(video_dir, 'gen_{}_id_{}.mp4'.format(gen, id))
            # video_gif_path = os.path.join(video_dir, 'gen_{}_id_{}.gif'.format(gen, id))

            print('\n----- Simulating the simulation -----\n')
            name_body = '{}_body_registry'.format(gen)
            name_controller_network = '{}_controller_network_registry'.format(gen)
            body_registry = getattr(results_manager, name_body)
            controller_network_registry = getattr(results_manager, name_controller_network)
            body = body_registry[key]
            controller_network = controller_network_registry[key]
            # print(config)

            images, _ = robot_simulator.simulate_render_mode_env(body.body, controller_network, network_manager, config.n_steps, type_env)

            print('\n----- Rendering the simulation -----\n')
            io.mimwrite(video_mp4_path, images, fps=30, macro_block_size=1)

            print('\n----- Saved Successfully -----\n')
        
        elif action == 'body' :
            exit = results_manager.print_both_body(type_genome)

        elif action == 'haploid genealogy' or action == 'genealogy' :
            exit = results_manager.explore_both_genealogy(type_genome)
        
        elif action == 'render haploid genealogy' or action == 'render genealogy' :
            exit, gen, id, genealogy = results_manager.render_both_family(type_genome)

            video_dir = os.path.join(results_manager.results_dir, type_genome, 'video')
            family_video_dir = os.path.join(video_dir, 'family', 'gen_{}_id_{}'.format(gen, id))
            os.makedirs(family_video_dir, exist_ok=True)

            for i in range(len(genealogy)) :
                cur_gen = gen - i
                if (cur_gen//config.switch) % 2 == 0 :
                    type_env = 0
                else :
                    type_env = 1
                for indi in genealogy[i] :
                    video_mp4_path = os.path.join(family_video_dir, 'gen_{}_id_{}.mp4'.format(cur_gen, indi))
                    # video_gif_path = os.path.join(family_video_dir, 'gen_{}_id_{}.gif'.format(cur_gen, indi))

                    print('\n----- Simulating the simulation -----\n')

                    name_body = '{}_body_registry'.format(cur_gen)
                    name_controller_network = '{}_controller_network_registry'.format(cur_gen)
                    body_registry = getattr(results_manager, name_body)
                    controller_network_registry = getattr(results_manager, name_controller_network)
                    body = body_registry[(cur_gen, indi)]
                    controller_network = controller_network_registry[(cur_gen, indi)]
                
                    images, _ = robot_simulator.simulate_render_mode_env(body.body, controller_network, network_manager, config.n_steps, type_env)
                    
                    io.mimwrite(video_mp4_path, images, fps=30, macro_block_size=1)
                   
                    print('\n----- Saved Successfully -----\n')
        
        elif action == 'save haploid family' or action == 'save family' :
            exit, gen, id, genealogy = results_manager.save_both_family(type_genome)

            images_dir = os.path.join(results_manager.results_dir, type_genome, 'images')
            family_images_dir = os.path.join(images_dir, 'family, gen_{}_id_{}'.format(gen, id))
            os.makedirs(family_images_dir, exist_ok=True)

            print('\n----- Saving the Images -----\n')
            for i in range(len(genealogy)) :
                cur_gen = gen - i
                if (cur_gen//config.switch) % 2 == 0 :
                    type_env = 0
                else :
                    type_env = 1
                for indi in genealogy[i] :
                    image_path = os.path.join(family_images_dir, 'gen_{}_id_{}.png'.format(cur_gen, indi))
                    # video_gif_path = os.path.join(family_images_dir, 'gen_{}_id_{}.gif'.format(cur_gen, indi))

                    name_body = '{}_body_registry'.format(cur_gen)
                    body_registry = getattr(results_manager, name_body)
                    body = body_registry[(cur_gen, indi)]

                    image = robot_simulator.simulate_render_image_mode_env(body.body, type_env)
                    io.imwrite(image_path, image)

            print('\n----- Saved Successfully -----\n')

        elif action == 'save individual' : 
            exit, gen, id = results_manager.save_both_body(type_genome)

            if (gen//config.switch) % 2 == 0 :
                type_env = 0
            else :
                type_env = 1

            images_dir = os.path.join(results_manager.results_dir, type_genome, 'images')
            os.makedirs(images_dir, exist_ok=True)

            print('\n----- Saving the Images -----\n')
            name_body = '{}_body_registry'.format(gen)
            body_registry = getattr(results_manager, name_body)
            body = body_registry[(gen, id)]

            image_path = os.path.join(images_dir, 'gen_{}_id_{}.png'.format(gen, id))

            image = robot_simulator.simulate_render_image_mode_env(body.body, type_env)
            io.imwrite(image_path, image)

            print('\n----- Saved Successfully -----\n')

        elif action == 'distance' :
            exit = results_manager.print_both_distance(distance_tool, type_genome)
        
        else : 
            exit = True 
        
        print('\n----- Exiting the program -----\n')



        
            



        








