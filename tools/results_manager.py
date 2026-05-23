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

                
            print('\n----- Saved Successfully -----\n\n')

    def begin_txt_file(self, systems) :
        txt_file_dir = os.path.join(self.abs_path_results, 'txt', 'all_info')
        with open(txt_file_dir, 'a') as f :
            f.write('\nHere the different systems below are being used :\n')
            for system in systems :
                f.write('\t' + system + '\n')
            f.write('\n\n')


    def _log(self, result):
        print(result)
        if self.save:
            with open(os.path.join(self.abs_path_results, 'txt', 'all_info'), 'a') as f:
                f.write(result)

    def starting(self, config):
        result = '\n'
        result += '----- Running with the following config -----\n'
        result += '\n'
        result += config + '\n'
        result += '\n'
        self._log(result)


    def end_generation(self) :
        passed = time.time() - self.time
        result = f' This Generation took {passed:.3f} s.\n'
        result += '\n'
        self._log(result)
       
    def start_generation(self, generation) :
        self.time = time.time()
        result = f'----- Starting generation number {generation} out of {self.config.generations} -----\n'
        result += '\n'
        self._log(result)
       

    def bests(self, bests) :
        result = '----- Bests of this generation -----\n'
        result += '\t ID \t fitness \n'
        result += '\t====\t=========\n'
        for id, fitness in bests :
            result += f'\t {id} \t {fitness:.3f}\n'
        result += '\n'
        self._log(result)
       

    def average_ind(self, all_ind) :
        average = sum(all_ind) / len(all_ind)
        averages = [average for _ in range(len(all_ind))]
        diff = [0 for _ in range(len(averages))]
        for i in range(len(all_ind)):
            diff[i] = (all_ind[i] - averages[i]) ** 2
        sigma = math.sqrt(sum(diff) / len(diff))
        result = f'Here is the total average of this generation : {average:.3f}\n'
        result += 'Please be careful, this fitness depends on how you treat the individual with an invalid body, what fitness is attributed, do you even count these individuals ? Here it should be calculated only with the valid individuals.\n'
        result += f'Anyway the standard deviation of the fitness is {sigma:.3f}\n'
        result += '\n'
        self._log(result)
       
    def deficient(self, number) :
        results = f'The number of deficient individuals on this generation is {number}. IE with an invalid body. '



    def loader(self) : 
        path = input('From which folder do you want to get the results : ')
        number = input('From which experiment ID do you want to get the results : ')
        local_dir =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        results_dir = os.path.join(local_dir, 'results', '{}'.format(path), 'id_{}'.format(number))
        json_dir  = os.path.join(results_dir, 'json')
        pkl_dir = os.path.join(results_dir, 'pkl')

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


        
            
            

        
