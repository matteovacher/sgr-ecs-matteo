import math
import os 
import json 
import dill 
import time 


class ResultsManager :

    def __init__(self) : 
        self.time = time.time()
        self.path = None 
        self.number = None 
        self.abs_path_results = None
        self.save = None  
        self.text_dir = None 

    def add_results_path(self) : 
        save = input("Do you want to save the results of this simulation ? \n \t [y] / [n] \n \t")
        if save == "y" : 
            self.save = True 
            path = input("Where do you want to store these data (please indicate the desired folder in results) : ")
            number = input("In order to classify the results, please indicate the experiment ID : ")
            self.path = path 
            self.number = number
            local_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            results_dir = os.path.join(local_dir, "results")
            self.abs_path_results = os.path.join(results_dir, '{}'.format(path), 'id_{}'.format(number))
            json_dir = os.path.join(self.abs_path_results, 'json')
            pkl_dir = os.path.join(self.abs_path_results, 'pkl')
            txt_dir = os.path.join(self.abs_path_results, 'txt')
            os.makedirs(json_dir, exist_ok=True)
            os.makedirs(pkl_dir, exist_ok=True) 
            os.makedirs(txt_dir, exist_ok=True)

        else : 
            self.save = False 
        print('\n\n')
    
    def save_results(self, registry, config) :
        time_1 = time.time()
        if self.save == True : 
            save_config_path = os.path.join(self.abs_path_results, 'json', 'configs.json')
            with open(save_config_path, 'w') as f : 
                json.dump(config.__dict__, f, indent = 4)

            for name, component_registry in registry.__dict__.items() :
                if not component_registry :
                    continue 
                component_path = os.path.join(self.abs_path_results, 'pkl', '{}.pkl'.format(name))
                with open(component_path, 'wb') as f : 
                    dill.dump(component_registry, f)
            passed = time.time() - time_1
            print(f'All results saved successfully in {passed:.3f} s.\n')

            print('\n----- Saved Successfully -----\n\n')

    def begin_txt_file(self, systems) :
        txt_file_dir = os.path.join(self.abs_path_results, 'txt', 'all_info')
        with open(txt_file_dir, 'a') as f :
            f.write('\nHere the different systems below are being used :\n')
            for system in systems :
                f.write('\t + {}\n'.format(system))
            f.write('\n\n')
            comments = input("Please indicate the desired comments : \n")
            f.write('Comments : {}\n\n'.format(comments))


    def _log(self, result):
        print(result)
        if self.save:
            with open(os.path.join(self.abs_path_results, 'txt', 'all_info'), 'a') as f:
                f.write(result)

    def starting(self, config):
        result = '\n'
        result += '----- Running with the following config -----\n'
        result += '\n'
        for key, value in config.__dict__.items():
            result += f'{key} : {value}\n'
        result += '\n'
        self._log(result)


    def end_generation(self) :
        passed = time.time() - self.time
        result = f' This Generation took {passed:.3f} s.\n'
        result += '\n'
        self._log(result)
       
    def start_generation(self, generation, config) :
        self.time = time.time()
        result = f'----- Starting generation number {generation} out of {config.generations} -----\n'
        result += '\n'
        self._log(result)
       

    def bests(self, bests) :
        result = '----- Bests of this generation -----\n'
        result += '\t ID \t Fitness \t Age\n'
        result += '\t====\t=========\t=====\n'
        for id, fitness, age in bests :
            result += f'\t {id} \t {fitness:.3f} \t\t {age}\n'
        result += '\n'
        self._log(result)

    def average_best(self, bests) :
        fitnesses = []
        ids = []
        best_id = bests[0][0]
        fitness_best = bests[0][1]
        for id, fitness, _ in bests :
            ids.append(id)
            fitnesses.append(fitness)
            average = sum(fitnesses) / len(fitnesses)
            averages = [average for _ in range(len(fitnesses))]
            diff = [0 for _ in range(len(averages))]
        for i in range(len(fitnesses)):
            diff[i] = (fitnesses[i] - averages[i]) ** 2
        sigma = math.sqrt(sum(diff) / len(diff))
        result = f'The average of the bests is {average:.3f} with a standard deviation of {sigma:.3f}\n'
        result += '\n'
        self._log(result)
        return best_id, fitness_best, average, sigma

       

    def average_ind(self, all_ind) :
        average = sum(all_ind) / len(all_ind)
        averages = [average for _ in range(len(all_ind))]
        diff = [0 for _ in range(len(averages))]
        for i in range(len(all_ind)):
            diff[i] = (all_ind[i] - averages[i]) ** 2
        sigma = math.sqrt(sum(diff) / len(diff))
        result = f'----- Statistics of this generation -----\n\n'
        result += f'Here is the total average of this generation : {average:.3f}\n'
        result += 'Please be careful, this fitness depends on how you treat the individual with an invalid body, what fitness is attributed, do you even count these individuals ? Here it should be calculated only with the valid individuals.\n'
        result += f'Anyway the standard deviation of the fitness is {sigma:.3f}\n'
        result += '\n'
        self._log(result)
        return average, sigma
       
    def deficient(self, number) :
        results = f'The number of deficient individuals on this generation is {number}. IE with an invalid body. '
        results += '\n'
        self._log(results)  



    def loader(self) : 
        path = input('From which folder do you want to get the results : ')
        number = input('From which experiment ID do you want to get the results : ')
        self.init_load = True 
        local_dir =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        results_dir = os.path.join(local_dir, 'results', '{}'.format(path), 'id_{}'.format(number))
        self.results_dir = results_dir
        json_dir  = os.path.join(results_dir, 'json')
        pkl_dir = os.path.join(results_dir, 'pkl')

        print('\n ----- Loading the results ----- \n')
        print('This will take some time, please wait ... \n\n')
        file = 'configs.json'
        json_dir_file = os.path.join(json_dir, file)
        with open(json_dir_file, 'r') as f : 
            if file.endswith('.json') :
                file = file.removesuffix('.json')
            data_config = json.load(f)
            self.__setattr__(file, data_config)

        for file in os.listdir(pkl_dir) : 
            file_dir = os.path.join(pkl_dir, file)
            with open(file_dir, 'rb') as f : 
                if file.endswith('.pkl') :
                    file = file.removesuffix('.pkl')
                loaded_object = dill.load(f)
                self.__setattr__(file, loaded_object)

        print('\n ----- Results loaded ----- \n')
        return False 
    
    def ask_action(self) :
        action = input('Do you want the body of the individuals or to render a certain individual ? \n \t [b] / [i] \n \t')
        return action

    def load_ind(self) :
        gen = input("Please indicate the generation of the generation of the individual you want to render : ")
        id = input("Please indicate the ID of the individual you want to render : ")
        exit = input("Do you want to exit the program ? \n \t [y] / [n] \n \t")
        if exit == "y" : 
            return True, gen, id  
        else :  
            return False,gen, id
        
    def print_bodies(self) :
        generation = input('Please indicate the generation of the bodies you want to print : ')
        exit = input("Do you want to exit the program ? \n \t [y] / [n] \n \t")
        
        print('\n ----- Loading the bodies of generation {} ----- \n'.format(generation))
        keys = [key for key in self.body_registry.keys() if key[0] == int(generation)]

        for key in keys : 
            print('Here is the body of individual {} : \n'.format(key[1]))
            print(self.body_registry[key].body)
            print('')
    
        if exit == "y" : 
            return True 
        else :  
            return False
        



        
            
            

        
