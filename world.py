from registry import ComponentRegistry


class World : 
    def __init__(self) : 
        self.registry = ComponentRegistry()
        self._builder_systems = []
        self._step_systems = []
        self._end_systems = []
        self.all_systems = []

    def add_builder_system(self, system) : 
        self._builder_systems.append(system)
        self.all_systems.append(system)
    
    def add_step_system(self, system) : 
        self._step_systems.append(system)
        self.all_systems.append(system)
    
    def add_end_system(self, system) : 
        self._end_systems.append(system)
        self.all_systems.append(system)


    def build(self) : 
        for system in self._builder_systems : 
            system.process(self.registry)

    def step(self) : 
        for system in self._step_systems : 
            system.process(self.registry)
    
    def end(self) : 
        for system in self._end_systems : 
            system.process(self.registry)