
import uuid

class Place:
    capacity = int
    residents = []
    parent = None
    child = []
    def __init__(self, name):
        self.name = name

    def set_parent(self, p):
        if self.parent == None:
            self.parent = p
            p.set_child

    def set_child(self, c):
        self.child = c


class NPC:
    name = str
    age = int
    rank = int
    location = Place
    id = uuid.uuid1
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_plan(self):
        print(self.rank)

    def set_rank(self, rank):
        self.rank = rank
    
    def get_rank(self):
        return caste[self.rank]
    
    def set_location(self, loc):
        self.location = loc
    
    def get_location(self):
        result = []
        temp = self.location
        result.append(temp)
        while (temp.parent != None):
            temp = temp.parent
            result.append(temp)
        return result

caste = {
    0 : "serf",
    1 : "freeman",
    2 : "cleric",
    3 : "bailiff",
    4 : "duke"
}
