import uuid

class Location:
    neighbours = []
    id = uuid.uuid1

    def __init__(self, name):
        self.name = name

    def set_neighbour(self, neighbour):
        if (self.neighbours.__contains__(neighbour) == False):
            self.neighbours.append(neighbour)
            neighbour.set_neighbour(self)

class Place(Location):
    parent = None
    children = []

    def __init__(self, name, type):
        super().__init__(name)
        self.type = type
   
    def set_parent(self, p):
        self.parent = p

    def set_child(self, c):
        self.children.append(c)
        c.set_parent(self)

class Building(Location):
    inventory = []
    def __init__(self, number, type, parent):
        self.parent = parent
        name = buildings[type]
        if (number != 0):
            name = (self.parent.name + ', ' + buildings[type] + ' ' + str(number))
        super().__init__(name)
        self.number = number
        self.type = type
        self.parent = parent

    def get_type(self):
        return buildings[self.type]

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        return self.inventory.pop(item)

class Road(Location):
    def __init__(self, name, neighbour, length  = 1):
        super().__init__(name)
        self.length = length
        self.neighbours.append(neighbour)

class Item:
    id = uuid.uuid1
    def __init__(self, type):
        self.name = items[type]
        self.type = type

items = {
    0 : 'stick',
    1 : 'knife',
    2 : 'poison',
    3 : 'bread',
}
    
buildings = {
    0 : 'house',
    1 : 'shop',
    2 : 'farm',
    3 : 'church',
    4 : 'manor',
    5 : 'keep'
}

places = {
    0 : 'village',
    1 : 'town',
    2 : 'city',
    3 : 'castle',
    4 : 'forest',
    5 : 'mountains', 
    6 : 'loner'
}