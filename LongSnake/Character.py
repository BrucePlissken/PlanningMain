
import uuid
import Place
from Place import Place

class Character:
    location = Place
    isAlive = True
    id = uuid.uuid1

    def __init__(self, name, age, rank):
        self.name = name
        self.age = age
        self.rank = rank

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

    def die(self):
        isAlive = False

caste = {
    0 : "serf",
    1 : "freeman",
    2 : "cleric",
    3 : "bailiff",
    4 : "duke"
}
