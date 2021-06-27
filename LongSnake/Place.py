class Place:
    parent = None
    child = []

    def __init__(self, name):
        self.name = name

    def set_parent(self, p):
        self.parent = p
        p.set_child

    def set_child(self, c):
        self.child.append(c)