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
        print('\n')
    
    def add_results_both_path(self) : 
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
        print('\n')

    
    
    def save_results(self, registry, config) :
        print('\n----- Saving JSON -----\n')
        if self.save == True : 
            save_config_path = os.path.join(self.abs_path_results, 'json', 'configs.json')
            with open(save_config_path, 'w') as f : 
                json.dump(config.__dict__, f, indent = 4)

            print('\n----- JSON Saved Successfully -----\n\n')

            print('\n----- Saving statistic_registry -----\n')
            component_path = os.path.join(self.abs_path_results, 'pkl', 'statistic_registry.pkl')
            with open(component_path, 'wb') as f : 
                dill.dump(registry.statistic_registry, f)
            print('\n----- Statistic registry saved successfully -----\n')




    def save_generation_registry(self, component_registry, name, generation  ) :
        print('\n----- Saving {} of Generation {} -----\n'.format(name, generation))
        time_1 = time.time()
        if self.save == True :
            component_path = os.path.join(self.abs_path_results, 'pkl', '{}_{}.pkl'.format(generation, name))
            with open(component_path, 'wb') as f : 
                dill.dump(component_registry, f)
            print('\n----- {} saved successfully -----\n'.format(name))
            time_2 = time.time()
            print('This took {} s.'.format(time_2 - time_1))
            
                


    def begin_txt_file(self, systems) :
        txt_file_dir = os.path.join(self.abs_path_results, 'txt', 'all_info')
        with open(txt_file_dir, 'a') as f :
            f.write('\nHere the different systems below are being used :\n')
            for system in systems :
                f.write('\t + {}\n'.format(system))
            f.write('\n')
            comments = input("Please indicate the desired comments for the text file report : \n")
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
        result = f'\nTHIS GENERATION TOOK {passed:.3f} s.\n'
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
        result += 'Here all the valid individuals are considered.\n'
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
        self.pkl_dir = os.path.join(results_dir, 'pkl')

        print('\n ----- Loading the Config ----- \n')
        file = 'configs.json'
        json_dir_file = os.path.join(json_dir, file)
        with open(json_dir_file, 'r') as f : 
            if file.endswith('.json') :
                file = file.removesuffix('.json')
            data_config = json.load(f)
            self.__setattr__(file, data_config)

        print('\n ----- Config loaded ----- \n')
        return False 
    
    def ask_action(self) :
        action = input('Do you want the body of a given generation ? or a single body ? or to render a certain individual ? or to explore the genealogy of a certain individual ? or to render a whole genealogy ? or to save images of a whole family ?  or to save the image of an individual ? or the distance between two individuals ?\n \t [bodies] / [body] / [render] / [genealogy] / [render genealogy] / [save family] / [save individual] / [distance] / [anything else to quit] \n \t')
        return action
    
    def ask_haploid_action(self) :
        action = input('Do you want the body of a given generation ? or a single body ? or to render a certain individual ? or to explore the genealogy of a certain individual ? or to render a whole genealogy ? or to save images of a whole family ?  or to save the image of an individual ? or the distance between two individuals ?\n \t [bodies] / [body] / [render] / [haploid genealogy] / [render haploid genealogy] / [save haploid family] / [save individual] / [distance] / [anything else to quit] \n \t')
        return action

    def load_ind(self) :
        gen = input("Please indicate the generation of the generation of the individual you want to render : ")
        id = input("Please indicate the ID of the individual you want to render : ")
        exit = input("Do you want to exit the program ? \n \t [y] / [n] \n \t")
        
        print('\n ----- Loading the save ----- \n')
        for file in os.listdir(self.pkl_dir) :
            if file.startswith('{}'.format(gen)) :
                file_dir = os.path.join(self.pkl_dir, file)
                with open(file_dir, 'rb') as f : 
                    if file.endswith('.pkl') :
                        file = file.removesuffix('.pkl')
                    loaded_object = dill.load(f)
                    self.__setattr__(file, loaded_object)
        print('\n ----- Save loaded ----- \n')
        if exit == "y" : 
            return True, gen, id  
        else :  
            return False,gen, id
        
    def save_body(self) :
        generation = input("Please indicate the generation of the body you want to render : ")
        ind = input("Please indicate the ID of the individual you want to render : ")
        exit = input("Do you want to exit the program ? \n \t [y] / [n] \n \t")
        ind = int(ind)
        generation = int(generation)
        print('\n----- Loading the save ----- \n')
        file = '{}_body_registry.pkl'.format(generation)
        file_dir = os.path.join(self.pkl_dir, file)
        with open(file_dir, 'rb') as f :    
            if file.endswith('.pkl') :  
                file = file.removesuffix('.pkl')
            loaded_object = dill.load(f)
            self.__setattr__(file, loaded_object)
        print('\n----- Save loaded ----- \n')
        if exit == "y" : 
            return True, generation, ind  
        else :  
            return False, generation, ind
    
    def print_body(self) :
        generation = input('Please indicate the generation of the body you want to print : ')
        ind = input('Please indicate the ID of the individual you want to print : ')
        exit = input("Do you want to exit the program ? \n \t [y] / [n] \n \t")
        ind = int(ind)
        generation = int(generation)
        print('\n ----- Loading the save ----- \n')
        
        file = '{}_body_registry.pkl'.format(generation)
        file_dir = os.path.join(self.pkl_dir, file)
        with open(file_dir, 'rb') as f :    
            if file.endswith('.pkl') :
                file = file.removesuffix('.pkl')
            loaded_object = dill.load(f)
            self.__setattr__(file, loaded_object)

        file = '{}_fitness_registry.pkl'.format(generation)
        file_dir = os.path.join(self.pkl_dir, file)
        with open(file_dir, 'rb') as f : 
            if file.endswith('.pkl') :
                file = file.removesuffix('.pkl')
            loaded_object = dill.load(f)
            self.__setattr__(file, loaded_object)
        print('\n ----- Save loaded ----- \n')

        name_body = '{}_body_registry'.format(generation)
        name_fitness = '{}_fitness_registry'.format(generation)

        body_registry = self.__getattribute__(name_body)
        fitness_registry = self.__getattribute__(name_fitness)
        print('Here is the body of the individual {} of generation {} with fitness {} : \n'.format(ind, generation, fitness_registry[(generation, ind)].fitness))
        print(body_registry[(generation, ind)].body)
        if exit == "y" : 
            return True
        else :  
            return False
        


    def print_bodies(self) :
        generation = input('Please indicate the generation of the bodies you want to print : ')
        exit = input("Do you want to exit the program ? \n \t [y] / [n] \n \t")

        print('\n ----- Loading the save ----- \n')
        
        file = '{}_body_registry.pkl'.format(generation)
        file_dir = os.path.join(self.pkl_dir, file)
        with open(file_dir, 'rb') as f : 
            if file.endswith('.pkl') :
                file = file.removesuffix('.pkl')
            loaded_object = dill.load(f)
            self.__setattr__(file, loaded_object)

        file = '{}_fitness_registry.pkl'.format(generation)
        file_dir = os.path.join(self.pkl_dir, file)
        with open(file_dir, 'rb') as f : 
            if file.endswith('.pkl') :
                file = file.removesuffix('.pkl')
            loaded_object = dill.load(f)
            self.__setattr__(file, loaded_object)
        print('\n ----- Save loaded ----- \n')
        
        print('\n ----- Loading the bodies of generation {} ----- \n'.format(generation))
        attr_name = '{}_body_registry'.format(generation)
        fitness_name = '{}_fitness_registry'.format(generation)
        body_registry = getattr(self, attr_name)
        fitness_registry = getattr(self, fitness_name)
        keys = [key for key in body_registry if key[0] == int(generation)]

        for key in keys : 
            print('Here is the body of individual {} : with a fitness of {}\n'.format(key[1], fitness_registry[key].fitness))
            print(body_registry[key].body)
            print('')
    
        if exit == "y" : 
            return True 
        else :  
            return False
        
    def explore_genealogy(self) :
        generation = input('Please indicate the generation of the individual you want to explore the genealogy : ')
        id = input('Please indicate the ID of the individual you want to explore : ')
        exit = input("Do you want to exit the program ? \n \t [y] / [n] \n \t")
        generation = int(generation)
        id = int(id)
        print('\n ----- Loading the save ----- \n')
        
        for i in range(3) :
            file = '{}_body_registry.pkl'.format(generation - i)
            file_dir = os.path.join(self.pkl_dir, file)
            with open(file_dir, 'rb') as f : 
                if file.endswith('.pkl') :
                    file = file.removesuffix('.pkl')
                loaded_object = dill.load(f)
                self.__setattr__(file, loaded_object)

            file = '{}_fitness_registry.pkl'.format(generation - i)
            file_dir = os.path.join(self.pkl_dir, file)
            with open(file_dir, 'rb') as f : 
                if file.endswith('.pkl') :
                    file = file.removesuffix('.pkl')
                loaded_object = dill.load(f)
                self.__setattr__(file, loaded_object)
            
            file = '{}_genome_registry.pkl'.format(generation - i)
            file_dir = os.path.join(self.pkl_dir, file)
            with open(file_dir, 'rb') as f : 
                if file.endswith('.pkl') :
                    file = file.removesuffix('.pkl')
                loaded_object = dill.load(f)
                self.__setattr__(file, loaded_object)

            file = '{}_parents_registry.pkl'.format(generation - i)
            file_dir = os.path.join(self.pkl_dir, file)
            with open(file_dir, 'rb') as f : 
                if file.endswith('.pkl') :
                    file = file.removesuffix('.pkl')
                loaded_object = dill.load(f)
                self.__setattr__(file, loaded_object)

        idddd = int(id)
        genealogy = [[id]]
        for i in range(3 - 1) :
            all_parents = []
            ids_to_get_parent = genealogy[i]
            name_parents_registry = '{}_parents_registry'.format(generation - i)
            parents_registry = getattr(self, name_parents_registry)
            for id in ids_to_get_parent : 
                parents = parents_registry[(generation - i, id)].parents
                parent1, parent2 = parents[0], parents[1]
                all_parents.append(parent1)
                all_parents.append(parent2)
            genealogy.append(all_parents)


        name_parents_registry = '{}_parents_registry'.format(generation)
        parents_registry = getattr(self, name_parents_registry)
        id_of_chromosome_parent1 = parents_registry[(generation, idddd)].parents_choices[0]
        id_of_chromosome_parent2 = parents_registry[(generation, idddd)].parents_choices[1]
        parent1 = parents_registry[(generation, idddd)].parents[0]
        parent2 = parents_registry[(generation, idddd)].parents[1]

        genealogy_choice = []
        genealogy_choice.append([(parent1, id_of_chromosome_parent1), (parent2, id_of_chromosome_parent2)])

        for i in range(1, 3 - 1) :
            name_parents_registry = '{}_parents_registry'.format(generation - i)
            parents_registry = getattr(self, name_parents_registry)
            to_who_look = genealogy_choice[i - 1]
            parent1 = parents_registry[(generation - i, to_who_look[0][0])].parents[to_who_look[0][1]]
            parent2 = parents_registry[(generation - i, to_who_look[1][0])].parents[to_who_look[1][1]]
            id_of_chromosome_parent1 = parents_registry[(generation - i, to_who_look[0][0])].parents_choices[to_who_look[0][1]]
            id_of_chromosome_parent2 = parents_registry[(generation - i, to_who_look[1][0])].parents_choices[to_who_look[1][1]]
            genealogy_choice.append([(parent1, id_of_chromosome_parent1), (parent2, id_of_chromosome_parent2)])

          
        print('I will try to print the genealogy so that it is readable')
        for i in range(len(genealogy)) :
        
            print('\n ----- Generation {} ----- \n'.format(generation - 2 + i))
            for id in genealogy[2 - i] :
                if i == 0 :
                    name_body = '{}_body_registry'.format(generation - 2 + i)
                    name_fitness = '{}_fitness_registry'.format(generation - 2 + i)
                    name_genome = '{}_genome_registry'.format(generation - 2 + i)
                    body_registry = getattr(self, name_body)
                    fitness_registry = getattr(self, name_fitness)
                    genome_registry = getattr(self, name_genome)
                    print('ID : {}'.format(id))
                    print('The fitness of this individual is : {}'.format(fitness_registry[(generation - 2 + i, id)].fitness))
                    print('The body of this individual is : \n{}'.format(body_registry[(generation - 2 + i, id)].body))
                    print('The Dominances of this individual is : \n{}\n{}'.format(genome_registry[(generation - 2 + i, id)].dominances[0], genome_registry[(generation - 2 + i, id)].dominances[1]))
                    print('')
                else :
                    name_parents = '{}_parents_registry'.format(generation - 2 + i)
                    name_body = '{}_body_registry'.format(generation - 2 + i)
                    name_fitness = '{}_fitness_registry'.format(generation - 2 + i)
                    name_genome = '{}_genome_registry'.format(generation - 2 + i)
                    parents_registry = getattr(self, name_parents)
                    body_registry = getattr(self, name_body)
                    fitness_registry = getattr(self, name_fitness)
                    genome_registry = getattr(self, name_genome)
                    print('ID : {}'.format(id))
                    print('The parents of this individual are : {} and {}'.format(parents_registry[(generation - 2 + i, id)].parents[0], parents_registry[(generation - 2 + i, id)].parents[1]))
                    print('The fitness of this individual is : {}'.format(fitness_registry[(generation - 2 + i, id)].fitness))
                    print('The body of this individual is : \n{}'.format(body_registry[(generation - 2 + i, id)].body))
                    print('The Dominances of this individual is : \n{}\n{}'.format(genome_registry[(generation - 2 + i, id)].dominances[0], genome_registry[(generation - 2 + i, id)].dominances[1]))
                    print('')
            
        print('Now let s study the genes and from which individual they are inherited, since we do not mix genomes like the meiosis it is simpler to analyze : \n')
        print('The first chromosome comes from the individual {} who is his grand parent.'.format(parent1))
        print('The second chromosome comes from the individual {} who is his grand parent.\n\n'.format(parent2))

        if exit == "y" : 
            return True  
        else :  
            return False
        
    def explore_haploid_genealogy(self) :
        generation = input('Please indicate the generation of the individual you want to explore the genealogy : ')
        id = input('Please indicate the ID of the individual you want to explore : ')
        exit = input("Do you want to exit the program ? \n \t [y] / [n] \n \t")
        generation = int(generation)
        id = int(id)
        print('\n ----- Loading the save ----- \n')
        
        for i in range(3) :
            file = '{}_body_registry.pkl'.format(generation - i)
            file_dir = os.path.join(self.pkl_dir, file)
            with open(file_dir, 'rb') as f : 
                if file.endswith('.pkl') :
                    file = file.removesuffix('.pkl')
                loaded_object = dill.load(f)
                self.__setattr__(file, loaded_object)

            file = '{}_fitness_registry.pkl'.format(generation - i)
            file_dir = os.path.join(self.pkl_dir, file)
            with open(file_dir, 'rb') as f : 
                if file.endswith('.pkl') :
                    file = file.removesuffix('.pkl')
                loaded_object = dill.load(f)
                self.__setattr__(file, loaded_object)
            
            file = '{}_haploid_registry.pkl'.format(generation - i)
            file_dir = os.path.join(self.pkl_dir, file)
            with open(file_dir, 'rb') as f : 
                if file.endswith('.pkl') :
                    file = file.removesuffix('.pkl')
                loaded_object = dill.load(f)
                self.__setattr__(file, loaded_object)

            file = '{}_haploid_parents_registry.pkl'.format(generation - i)
            file_dir = os.path.join(self.pkl_dir, file)
            with open(file_dir, 'rb') as f : 
                if file.endswith('.pkl') :
                    file = file.removesuffix('.pkl')
                loaded_object = dill.load(f)
                self.__setattr__(file, loaded_object)

        idddd = int(id)
        genealogy = [[id]]
        for i in range(3 - 1) :
            all_parents = []
            ids_to_get_parent = genealogy[i]
            name_parents_registry = '{}_haploid_parents_registry'.format(generation - i)
            parents_registry = getattr(self, name_parents_registry)
            for id in ids_to_get_parent : 
                parents = parents_registry[(generation - i, id)].parents
                parent1, parent2 = parents[0], parents[1]
                all_parents.append(parent1)
                all_parents.append(parent2)
            genealogy.append(all_parents)


        name_parents_registry = '{}_haploid_parents_registry'.format(generation)
        parents_registry = getattr(self, name_parents_registry)
        parent1 = parents_registry[(generation, idddd)].parents[0]
        parent2 = parents_registry[(generation, idddd)].parents[1]

          
        print('I will try to print the genealogy so that it is readable')
        for i in range(len(genealogy)) :
        
            print('\n ----- Generation {} ----- \n'.format(generation - 2 + i))
            for id in genealogy[2 - i] :
                if i == 0 :
                    name_body = '{}_body_registry'.format(generation - 2 + i)
                    name_fitness = '{}_fitness_registry'.format(generation - 2 + i)
                    name_haploid = '{}_haploid_registry'.format(generation - 2 + i)
                    body_registry = getattr(self, name_body)
                    fitness_registry = getattr(self, name_fitness)
                    haploid_registry = getattr(self, name_haploid)
                    print('ID : {}'.format(id))
                    print('The fitness of this individual is : {}'.format(fitness_registry[(generation - 2 + i, id)].fitness))
                    print('The body of this individual is : \n{}'.format(body_registry[(generation - 2 + i, id)].body))
                    print('The Dominances of this individual is : \n{}'.format(haploid_registry[(generation - 2 + i, id)].dominances))
                    print('')
                else :
                    name_parents = '{}_haploid_parents_registry'.format(generation - 2 + i)
                    name_body = '{}_body_registry'.format(generation - 2 + i)
                    name_fitness = '{}_fitness_registry'.format(generation - 2 + i)
                    name_haploid = '{}_haploid_registry'.format(generation - 2 + i)
                    parents_registry = getattr(self, name_parents)
                    body_registry = getattr(self, name_body)
                    fitness_registry = getattr(self, name_fitness)
                    haploid_registry = getattr(self, name_haploid)
                    print('ID : {}'.format(id))
                    print('The parents of this individual are : {} and {}'.format(parents_registry[(generation - 2 + i, id)].parents[0], parents_registry[(generation - 2 + i, id)].parents[1]))
                    print('The fitness of this individual is : {}'.format(fitness_registry[(generation - 2 + i, id)].fitness))
                    print('The body of this individual is : \n{}'.format(body_registry[(generation - 2 + i, id)].body))
                    print('The Dominances of this individual is : \n{}'.format(haploid_registry[(generation - 2 + i, id)].dominances))
                    print('')

        if exit == "y" : 
            return True  
        else :  
            return False
        
    def render_family(self) :
        generation = input("Please indicate the generations of the family you want to render : ")
        ind = input("Please indicate the ID of the individual you want to render : ")
        exit = input("Do you want to exit the program ? \n \t [y] / [n] \n \t")
        ind = int(ind)
        generation = int(generation)

        print('\n ----- Loading the save ----- \n')
        for i in range(3) :
            for file in os.listdir(self.pkl_dir) :
                if file.startswith('{}'.format(generation - i)) :
                    file_dir = os.path.join(self.pkl_dir, file)
                    with open(file_dir, 'rb') as f : 
                        if file.endswith('.pkl') :
                            file = file.removesuffix('.pkl')
                        loaded_object = dill.load(f)
                        self.__setattr__(file, loaded_object)
        
        genealogy = [[ind]]
        for i in range(3 - 1) :
            all_parents = []
            ids_to_get_parent = genealogy[i]
            name_parents_registry = '{}_parents_registry'.format(generation - i)
            parents_registry = getattr(self, name_parents_registry)
            for id in ids_to_get_parent : 
                parents = parents_registry[(generation - i, id)].parents
                parent1, parent2 = parents[0], parents[1]
                all_parents.append(parent1)
                all_parents.append(parent2)
            genealogy.append(all_parents)

        if exit == "y" :
            return True, generation, ind, genealogy
        else : 
            return False, generation, ind, genealogy
        
    def render_haploid_family(self) :
        generation = input("Please indicate the generations of the family you want to render : ")
        ind = input("Please indicate the ID of the individual you want to render : ")
        exit = input("Do you want to exit the program ? \n \t [y] / [n] \n \t")
        ind = int(ind)
        generation = int(generation)

        print('\n ----- Loading the save ----- \n')
        for i in range(3) :
            for file in os.listdir(self.pkl_dir) :
                if file.startswith('{}'.format(generation - i)) :
                    file_dir = os.path.join(self.pkl_dir, file)
                    with open(file_dir, 'rb') as f : 
                        if file.endswith('.pkl') :
                            file = file.removesuffix('.pkl')
                        loaded_object = dill.load(f)
                        self.__setattr__(file, loaded_object)
        
        genealogy = [[ind]]
        for i in range(3 - 1) :
            all_parents = []
            ids_to_get_parent = genealogy[i]
            name_parents_registry = '{}_haploid_parents_registry'.format(generation - i)
            parents_registry = getattr(self, name_parents_registry)
            for id in ids_to_get_parent : 
                parents = parents_registry[(generation - i, id)].parents
                parent1, parent2 = parents[0], parents[1]
                all_parents.append(parent1)
                all_parents.append(parent2)
            genealogy.append(all_parents)

        if exit == "y" :
            return True, generation, ind, genealogy
        else : 
            return False, generation, ind, genealogy
        
        
    def save_family(self) :
        generation = input("Please indicate the generations of the family you want to render : ")
        ind = input("Please indicate the ID of the individual you want to render : ")
        exit = input("Do you want to exit the program ? \n \t [y] / [n] \n \t")
        ind = int(ind)
        generation = int(generation)

        print('\n ----- Loading the save ----- \n')
        for i in range(3) :
            for file in os.listdir(self.pkl_dir) :
                if file.startswith('{}'.format(generation - i)) :
                    file_dir = os.path.join(self.pkl_dir, file)
                    with open(file_dir, 'rb') as f : 
                        if file.endswith('.pkl') :
                            file = file.removesuffix('.pkl')
                        loaded_object = dill.load(f)
                        self.__setattr__(file, loaded_object)
        
        genealogy = [[ind]]
        for i in range(3 - 1) :
            all_parents = []
            ids_to_get_parent = genealogy[i]
            name_parents_registry = '{}_parents_registry'.format(generation - i)
            parents_registry = getattr(self, name_parents_registry)
            for id in ids_to_get_parent : 
                parents = parents_registry[(generation - i, id)].parents
                parent1, parent2 = parents[0], parents[1]
                all_parents.append(parent1)
                all_parents.append(parent2)
            genealogy.append(all_parents)

        if exit == "y" :
            return True, generation, ind, genealogy
        else : 
            return False, generation, ind, genealogy
        
    def save_haploid_family(self) :
        generation = input("Please indicate the generations of the family you want to render : ")
        ind = input("Please indicate the ID of the individual you want to render : ")
        exit = input("Do you want to exit the program ? \n \t [y] / [n] \n \t")
        ind = int(ind)
        generation = int(generation)

        print('\n ----- Loading the save ----- \n')
        for i in range(3) :
            for file in os.listdir(self.pkl_dir) :
                if file.startswith('{}'.format(generation - i)) :
                    file_dir = os.path.join(self.pkl_dir, file)
                    with open(file_dir, 'rb') as f : 
                        if file.endswith('.pkl') :
                            file = file.removesuffix('.pkl')
                        loaded_object = dill.load(f)
                        self.__setattr__(file, loaded_object)
        
        genealogy = [[ind]]
        for i in range(3 - 1) :
            all_parents = []
            ids_to_get_parent = genealogy[i]
            name_parents_registry = '{}_haploid_parents_registry'.format(generation - i)
            parents_registry = getattr(self, name_parents_registry)
            for id in ids_to_get_parent : 
                parents = parents_registry[(generation - i, id)].parents
                parent1, parent2 = parents[0], parents[1]
                all_parents.append(parent1)
                all_parents.append(parent2)
            genealogy.append(all_parents)

        if exit == "y" :
            return True, generation, ind, genealogy
        else : 
            return False, generation, ind, genealogy
        
    def print_distance(self, distance_tool) :
        generation1 = input('Please indicate the generation of the first individual : ')
        id1 = input('Please indicate the ID of the first individual : ')
        generation2 = input('Please indicate the generation of the second individual : ')
        id2 = input('Please indicate the ID of the second individual : ')
        exit = input("Do you want to exit the program ? \n \t [y] / [n] \n \t")
        generation1, id1, generation2, id2 = int(generation1), int(id1), int(generation2), int(id2)

        print('\n ----- Loading the save ----- \n')
        file1 = '{}_body_registry.pkl'.format(generation1)
        file_dir = os.path.join(self.pkl_dir, file1)
        with open (file_dir, 'rb') as f :    
            if file1.endswith('.pkl') :  
                file1 = file1.removesuffix('.pkl')
            loaded_object = dill.load(f)
            self.__setattr__(file1, loaded_object)

        file2 = '{}_body_registry.pkl'.format(generation2)    
        file_dir = os.path.join(self.pkl_dir, file2)
        with open (file_dir, 'rb') as f :    
            if file2.endswith('.pkl') :  
                file2 = file2.removesuffix('.pkl')
            loaded_object = dill.load(f)
            self.__setattr__(file2, loaded_object)
        
        name_body1 = '{}_body_registry'.format(generation1)
        name_body2 = '{}_body_registry'.format(generation2)
        body_registry1 = getattr(self, name_body1)
        body_registry2 = getattr(self, name_body2)
        body1 = body_registry1[(generation1, id1)].body
        body2 = body_registry2[(generation2, id2)].body

        file1 = '{}_cppn_registry.pkl'.format(generation1)
        file_dir = os.path.join(self.pkl_dir, file1)
        with open (file_dir, 'rb') as f :    
            if file1.endswith('.pkl') :  
                file1 = file1.removesuffix('.pkl')
            loaded_object = dill.load(f)
            self.__setattr__(file1, loaded_object)

        file2 = '{}_cppn_registry.pkl'.format(generation2)
        file_dir = os.path.join(self.pkl_dir, file2)
        with open (file_dir, 'rb') as f :
            if file2.endswith('.pkl') :  
                file2 = file2.removesuffix('.pkl')
            loaded_object = dill.load(f)
            self.__setattr__(file2, loaded_object)

        name_cppn1 = '{}_cppn_registry'.format(generation1)
        name_cppn2 = '{}_cppn_registry'.format(generation2)
        cppn_registry1 = getattr(self, name_cppn1)
        cppn_registry2 = getattr(self, name_cppn2)
        node_evals1 = cppn_registry1[(generation1, id1)].node_evals
        node_evals2 = cppn_registry2[(generation2, id2)].node_evals

        act_function_distance, weight_distance, bias_distance, normalized_act_function_distance, normalized_weight_distance, normalized_bias_distance = distance_tool.distance_expressed_genome(node_evals1, node_evals2)
        distance, distance_normalized = distance_tool.phenotypic_body_distance(body1, body2)
        print('\n ----- Save loaded ----- \n')
        print('The body of the individual {} of generation {} is : \n{} \nAnd the body of the individual {} of generation {} is : \n{} \n'.format(id1, generation1, body1, id2, generation2, body2))
        print('The phenotypic body distance between the individual {} of generation {} and the individual {} of generation {} is : \n{} \nAnd the normalized distance is : \n{} \nAnd the compatibility is : \n{}% \n'.format(id1, generation1, id2, generation2, distance, distance_normalized, 100 * (1 - distance_normalized)))
        print('The distance between the activation functions of the CPPNs of the individual {} of generation {} and the individual {} of generation {} is : \n{} \n'.format(id1, generation1, id2, generation2, act_function_distance))
        print('The distance between the weights of the CPPNs of the individual {} of generation {} and the individual {} of generation {} is : \n{} \n'.format(id1, generation1, id2, generation2, weight_distance))
        print('The distance between the biases of the CPPNs of the individual {} of generation {} and the individual {} of generation {} is : \n{} \n'.format(id1, generation1, id2, generation2, bias_distance))
        print('The normalized distance between the activation functions of the CPPNs of the individual {} of generation {} and the individual {} of generation {} is : \n{} \n'.format(id1, generation1, id2, generation2, normalized_act_function_distance))
        print('The normalized distance between the weights of the CPPNs of the individual {} of generation {} and the individual {} of generation {} is : \n{} \n'.format(id1, generation1, id2, generation2, normalized_weight_distance))
        print('The normalized distance between the biases of the CPPNs of the individual {} of generation {} and the individual {} of generation {} is : \n{} \n'.format(id1, generation1, id2, generation2, normalized_bias_distance))
        print('\nPlease note that here, a normalized distance of 1 means that twice the parameter_range is between the two considered genome. For example for a weight range of 5, a normalized distance of 1 means that the two genome are separated by a distance of 20')
        

        if exit == "y" :
            return True
        else : 
            return False

        




        
            
            

        
