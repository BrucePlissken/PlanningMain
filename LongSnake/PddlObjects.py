class Location:
    def __init__(self, name):
        self.name = name
        self.items = []
        self.ppl = []

class Character:
    def __init__(self, name):
        self.name = name
        self.skills = []
        self.status = []
        self.known = []
        self.inventory = []