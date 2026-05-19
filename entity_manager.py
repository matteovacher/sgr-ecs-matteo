



class EntityManager : 

    def __init__(self) : 
        self.next_id = 0 
        self._alive = set()

    def create_entity(self) : 
        id = self.next_id 
        self.next_id += 1
        self._alive.add(id)
        return id 
    
    def destroy_entity(self, entity_id) : 
        self._alive.remove(entity_id)

    def is_alive(self, entity_id) : 
        return entity_id in self._alive
    
    