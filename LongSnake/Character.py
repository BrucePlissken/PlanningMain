import uuid

class Character:
    isAlive = True
    id = uuid.uuid1
    inventory = []

    def __init__(self, name, age, rank, home = None):
        self.name = name
        self.age = age
        self.rank = rank
        self.home = home
        self.location = home

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

    def take_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        if(self.inventory.__contains__(item)):
            return self.inventory.pop(item)

    def die(self):
        isAlive = False

caste = {
    0 : "serf",
    1 : "freeman",
    2 : "cleric",
    3 : "bailiff",
    4 : "duke",
    5 : 'merchant'
}
