import os 
import imageio as io 

from config import Config

from tools.results_manager import ResultsManager
from tools.robot_simulator import RobotSimulator
from tools.network_manager import NetworkManager


def render() : 
    
    results_manager = ResultsManager()
    exit = results_manager.loader()
    config = Config(results_manager.configs)
    network_manager = NetworkManager(config)
    robot_simulator = RobotSimulator(config)

    while exit == False :
        action = results_manager.ask_action()
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
            io.mimwrite(video_mp4_path, images, fps=24, macro_block_size=1)
            io.mimwrite(video_gif_path, images, fps=24, macro_block_size=1)

            print('\n----- Saved Successfully -----\n')

        elif action == 'genealogy' :
            exit = results_manager.explore_genealogy()

        elif action == 'body' :
            exit = results_manager.print_body()

        elif action == 'render genealogy' :
            exit, gen, id, genealogy = results_manager.render_family()
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
                    
                    io.mimwrite(video_mp4_path, images, fps=24, macro_block_size=1)
                    io.mimwrite(video_gif_path, images, fps=24, macro_block_size=1)

                    print('\n----- Saved Successfully -----\n')
        
        elif action == 'save family' :
            exit, gen, id, genealogy = results_manager.save_family()
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

        else :
            exit = True
    
    print('\n----- Exiting -----\n')



if __name__ == "__main__" : 
    render()