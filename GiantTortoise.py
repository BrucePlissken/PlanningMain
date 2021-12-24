"""
Let's try to make a genetic algorithm
Auth: Jakob Ehlers
"""
import PDDLController
import IntermediateParser
from IntermediateParser import *

class GiantTortoise:
    def __init__(self, domainF, problemF):
        self.pc = PDDLController.PDDLController(domainF, problemF)
        self.goalPredicates = self.getGoalPredicates()
        self.thesaurus = {**self.expandDict(self.pc.pddltypes, self.pc.probjects, "- "), **self.pc.probjects}

        n = 3
        m = 8

        temp = self.substituteVar(self.goalPredicates[n],m)

        print(temp)

    #creates a list of achievable goal-state expressions from action effects and domain predicates
    def getGoalPredicates(self):
        result = []
        temp = ""
        for action in self.pc.actions:
            for effect in action["effect"]["and"]:
                ton = False
                if (type(effect) is dict):
                    if (list(effect.keys()).__contains__("not")):
                        ton = True
                        effect = effect["not"]
                    else: continue
                for pred in self.pc.predicates:
                    if (pred.count(effect.split()[0]) > 0):
                        if (ton):
                            temp = "(not " + pred + ")"
                            break
                        else:
                            temp = pred
                            break
                if (result.__contains__(temp) == False):
                    result.append(temp)
        return result

    #expand definitions so upper categories include sub's content
    def expandDict(self, super_dict, sub_dict, prefix = ""):
        result = {}
        for x in super_dict:
            temp = []
            for k in super_dict[x]:
                key = prefix + k
                if(list(sub_dict.keys()).__contains__(key)):
                    temp = temp + sub_dict[key]
            result[x] = temp

        return result

    def makeGene(self):

        pass

    def substituteVar(self, predicate, no, variable = ""):
        if (variable == ""):
            temp = predicate.partition("?")
            preTemp = temp[0]
            variable = "?" + temp[2].partition(" ")[0]
            signifier = temp[2].partition("- ")[2].partition(")")[0]
        if(signifier.count(" ") > 0):
            signifier = signifier.partition(" ")[0]
        signifier = "- " + signifier
        value = self.thesaurus[signifier][no]

        result = predicate.replace(variable,value)

        if (result.partition(signifier)[0].count("?") < 1):
            signifier = " " + signifier
            result = result.replace(signifier, "")
        
        return result

"""
testing stuff
"""        
import pprint


pd = "tmp/AdventureDomCopy.pddl"
pp = "tmp/AdventureProbCopycopy.pddl"

dna = GiantTortoise(pd,pp)

"""
pprint.pprint(dna.thesaurus)


for x in dna.goalPredicates:
    print(x)

print()
pprint.pprint(dna.pc.probjects)
print()
pprint.pprint(dna.pc.pddltypes)

"""