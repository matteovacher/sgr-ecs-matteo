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
        if action == 'b' : 
            exit = results_manager.print_bodies()
        elif action == 'i' :
            exit, gen, id = results_manager.load_ind()

            gen, id = int(gen), int(id)
            key = (gen, id)

            video_dir = os.path.join(results_manager.results_dir, 'video')
            os.makedirs(video_dir, exist_ok=True)

            video_mp4_path = os.path.join(video_dir, 'gen_{}_id_{}.mp4'.format(gen, id))
            video_gif_path = os.path.join(video_dir, 'gen_{}_id_{}.gif'.format(gen, id))

            print('\n----- Simulating the simulation -----\n')
            body = results_manager.body_registry[key]
            controller_network = results_manager.controller_network_registry[key]
        
            images, _ = robot_simulator.simulate_render(body.body, controller_network, network_manager, config.n_steps)
            
            print('\n----- Rendering the simulation -----\n')
            io.mimwrite(video_mp4_path, images, fps=30, macro_block_size=1)
            io.mimwrite(video_gif_path, images, fps=30, macro_block_size=1)

            print('\n----- Saved Successfully -----\n')
        else :
            exit = True
    
    print('\n----- Exiting -----\n')



if __name__ == "__main__" : 
    render()