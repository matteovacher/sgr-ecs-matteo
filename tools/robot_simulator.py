import gymnasium as gym
import math 
import numpy as np 

import evogym.envs

from evogym.utils import get_full_connectivity 


class RobotSimulator:
    def __init__(self, config) :
        self.config = config 



    def _get_env(self, robot):
        connections = get_full_connectivity(robot)
        env = gym.make(self.config.env_name, body = robot, connections = connections)
        return env.unwrapped 
    
    def _get_env_mode_env(self, robot, type_env) :
        connections = get_full_connectivity(robot)
        env = gym.make(self.config.env_name[type_env], body = robot, connections = connections)
        return env.unwrapped

    def get_observation_size(self, robot) :
        env = self._get_env(robot)
        observation, _ = env.reset()
        env.close()
        del env 
        return len(observation)
    
    def get_observation_size_mode_env(self, robot, type_env) :
        env = self._get_env_mode_env(robot, type_env)
        observation, _ = env.reset()
        env.close()
        del env 
        return len(observation)
    

    def simulate(self, id, robot, controller, n_steps, controller_manager) :
        try :
            env = self._get_env(robot)
            reward = 0

            observation, _ = env.reset()

            actuators = env.get_actuator_indices("robot")
            inputs_size = math.ceil(math.sqrt(len(observation)))

            finished = False

            for _ in range (n_steps) :
                observation.resize(inputs_size**2)
                all_actions = controller_manager.activate(controller, observation)
                action = np.array([all_actions[i] for i in actuators])
                observation, step_reward, terminated, truncated, _ = env.step(action)

                reward += step_reward

                done = terminated or truncated

                if done :
                    finished = True
                    break

            env.close()
            del env
            return id, reward, finished

        except Exception :
            return id, -1000, True
    
    def simulate_mode_env(self, id, robot, controller, n_steps, controller_manager, type_env) : 
        env = self._get_env_mode_env(robot, type_env) 
        reward = 0  

        observation, _ = env.reset()

        actuators = env.get_actuator_indices("robot")
        inputs_size = math.ceil(math.sqrt(len(observation)))

        finished = False 

        for _ in range (n_steps) : 
            observation.resize(inputs_size**2)
            all_actions = controller_manager.activate(controller, observation)
            action = np.array([all_actions[i] for i in actuators])
            observation, step_reward, terminated, truncated, _ = env.step(action)

            reward += step_reward

            done = terminated or truncated 

            if done : 
                finished = True 
                break 

        env.close() 
        del env 
        return id, reward, finished

    def _get_env_render(self, robot) : 
        print('----- Here is the simulated robot -----\n')
        connections = get_full_connectivity(robot)
        env = gym.make(self.config.env_name, body=robot, connections=connections, render_mode="rgb_array")
        return env.unwrapped
    
    def _get_env_render_mode_env(self, robot, type_env) : 
        print('----- Here is the simulated robot -----\n')
        connections = get_full_connectivity(robot)
        env = gym.make(self.config.env_name[type_env], body=robot, connections=connections, render_mode="rgb_array")
        return env.unwrapped
    
    def simulate_render(self, robot, controller, controller_manager, n_steps) : 
        env = self._get_env_render(robot)
        fitness = 0
        observation, _ = env.reset()

        actuators = env.get_actuator_indices("robot")
        inputs_size = math.ceil(math.sqrt(len(observation)))

        images = []

        for _ in range (n_steps) : 

            images.append(env.render())

            observation.resize(inputs_size**2)
            all_actions = controller_manager.activate(controller, observation)
            action = np.array([all_actions[i] for i in actuators])
            observation, reward, terminated, truncated, _ = env.step(action)

            done = terminated or truncated 
            fitness += reward
            if done : 
                break 

        env.close()
        del env 
        print(f'Individual fitness : {fitness}\n')
        print('----- End of simulation -----\n')
        return images, fitness 
    
    def simulate_render_mode_env(self, robot, controller, controller_manager, n_steps, type_env) : 
        env = self._get_env_render_mode_env(robot, type_env)
        fitness = 0
        observation, _ = env.reset()

        actuators = env.get_actuator_indices("robot")
        inputs_size = math.ceil(math.sqrt(len(observation)))

        images = []

        for _ in range (n_steps) : 

            images.append(env.render())

            observation.resize(inputs_size**2)
            all_actions = controller_manager.activate(controller, observation)
            action = np.array([all_actions[i] for i in actuators])
            observation, reward, terminated, truncated, _ = env.step(action)

            done = terminated or truncated 
            fitness += reward
            if done : 
                break 

        env.close()
        del env 
        print(f'Individual fitness : {fitness}\n')
        print('----- End of simulation -----\n')
        return images, fitness 
    
    def simulate_render_image_mode_env(self, robot, type_env) :
        env = self._get_env_render_mode_env(robot, type_env)
        _, _ = env.reset()
        robot_image = env.render()
        env.close()
        del env 
        return robot_image
        
