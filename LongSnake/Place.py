import uuid

class Place:
    parent = None
    child = []
    id = uuid.uuid1

    def __init__(self, name):
        self.name = name

    def set_parent(self, p):
        self.parent = p
        p.set_child

    def set_child(self, c):
        self.child.append(c)

class Building(Place):

    def __init__(self, number, type, place):
        self.parent = place
        name = buildings[type]
        if (number != 0):
            name = (self.parent.name + ', ' + buildings[type] + ' ' + str(number))
        super().__init__(name)
        self.number = number
        self.type = type

    def get_type(self):
        return buildings[self.type]

    def add_item(self, item):
        self.child.append(item)

    def remove_item(self, item):
        return self.child.pop(item)

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