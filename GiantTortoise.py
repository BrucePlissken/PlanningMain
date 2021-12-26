"""
Let's try to make a genetic algorithm
Auth: Jakob Ehlers
"""
import PDDLController
import IntermediateParser
from IntermediateParser import *
import random

class GiantTortoise:
    def __init__(self, domainF, problemF):
        self.pc = PDDLController.PDDLController(domainF, problemF)
        self.goalPredicates = self.getGoalPredicates()
        self.thesaurus = {**self.expandDict(self.pc.pddltypes, self.pc.probjects, "- "), **self.pc.probjects}

        self.genome = [len(self.goalPredicates)] + self.mapGenome(self.thesaurus)
        #random.seed("the blood in my urine tastes too much like iron")
        
        #making a random gene from the genome for goalpredicates
        gene = []
        for x in self.genome:
            n = random.randrange(0, x)
            gene.append(n)
        print(self.makeGene(gene, self.goalPredicates))


    #creates a list of achievable goal-state expressions from action effects and domain predicates
    def getGoalPredicates(self):
        result = []
        temp = ""
        for action in self.pc.actions:
            for effect in action["effect"]["and"]:
                ton = False
                if (type(effect) is dict):
                    #let's try skipping the "nots" and instead add them later on, by checking against the current state
                    continue
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
                if (list(super_dict.keys()).__contains__(key)):
                    for p in super_dict[key]:
                        pey = prefix + p
                        if(list(sub_dict.keys()).__contains__(pey)):
                            temp = temp + sub_dict[pey]        
                if(list(sub_dict.keys()).__contains__(key)):
                    temp = temp + sub_dict[key]
            result[x] = temp

        return result

    #returns a gene from an int[] by popping the first int and picking the complying expression from the pool, and using the rest of the list as choices for substitution
    def makeGene(self, dna, pool):
        cellShell = dna.pop(0)

        cellShell = pool[cellShell -1]
        result = self.substituteVar(cellShell, dna)
        #to "not" or not to "not"
        if (self.pc.state.count(result) > 0):
            result = "(not " + result + ")"
        return result

    #takes in an expression and, if no variable is given the first, ?smth variable that gets substituted with a fitting string from the thesaurus
    #maybe this should be made more general and put in the parser
    def substituteVar(self, predicate, dna):
        result = predicate
        while (result.count("?") > 0):    
            temp = result.partition("?")
            variable = "?" + temp[2].partition(" ")[0]
            signifier = temp[2].partition("- ")[2].partition(")")[0]

            if(signifier.count(" ") > 0):
                signifier = signifier.partition(" ")[0]
            signifier = "- " + signifier
            p = 0
            for x in self.thesaurus:
                if (x == signifier):
                    no = dna[p] -1
                p += 1
            value = self.thesaurus[signifier][no]

            result = result.replace(variable,value)

            if (result.partition(signifier)[0].count("?") < 1):
                signifier = " " + signifier
                result = result.replace(signifier, "")
        return result

    #returns a list of ints from the length of the lists of parameter possibilities of the expression
    def mapGenome(self, source):
        result = []
        for x in source:
            temp = len(source[x])
            result.append(temp)
        
        return result

"""
testing stuff
"""        
import pprint


pd = "tmp/AdventureDomCopy.pddl"
pp = "tmp/AdventureProbCopycopy.pddl"

pd1 = "tmp/lrrhDom.pddl"
pp1 = "tmp/lrrhProb.pddl"

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