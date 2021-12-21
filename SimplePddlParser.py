from os import error
import IntermediateParser
from IntermediateParser import *

class ActionParser:
    def __init__(self, domain, prob):
        self.dom = domain
        self.prob = prob
        df = open(domain)
        self.domain = df.read().lower()
        df.close()
        pf = open(prob)
        self.state = pf.read().partition("objects")[2].partition("(:goal")[0].rpartition(")")[0].lower()
        pf.close()
        self.actions = []
        n = self.domain.count("action")
        x = 0
        tempDom = self.domain
        while (x < n):
            tempDom = tempDom.partition("action ")[2]
            self.parseAction(tempDom.partition("\n")[0])
            x += 1
        self.pddltypes = self.mapTyps()
        print(self.pddltypes)

    def parseAction(self, name):        
        actionString = self.domain.partition(name)[2].partition("(:")[0]
        if (actionString == ""):
            print("no such action")

        params = whiteSpaceMatters(actionString.partition("parameters")[2].partition(":precondition")[0])
        preco = parsePddlExpression(actionString.partition("precondition")[2].partition(":effect")[0])
        effe = parsePddlExpression(actionString.partition("effect")[2])


        action = Claction(name, params, preco,effe)
        self.actions.append(action)

    def getAction(self, name):
        for x in self.actions:
            if (x.name == name):
                return x
        print("error: no such action name: " + name)

    def adjustParameters(self, action, params):
        paramargs = action.parameters 
        result = {}
        params = params.partition(" ")[2]
        n = paramargs.count("?")
        x = 0
        while (x < n):
            paramargs = paramargs.partition("?")[2]

            if (paramargs.count(" ") > 0):
                s = "?" + paramargs.partition(" ")[0]
                result[s] = params.partition(" ")[0].replace(")", "")
            elif (paramargs.count(")") > 0):
                s = "?" + paramargs.partition(")")[0]
                result[s] = params.partition(")")[0]

            params = params.partition(" ")[2]
            x += 1

        return result
        #also add the objects to the dictionary

    def mapTyps(self):
        typs = self.domain.partition("(:predicates")[0].partition("types")[2]
        result = {}
        i = typs.count("-")
        n = 0
        while (n < i):
            kvpair = typs.partition("-")
            k = "-" + kvpair[2].partition("\n")[0]
            v = kvpair[0].rpartition("\n")[2].split()
            result[k] = v
            typs = typs.partition(k)[2]
            n +=1
        
        return result

    def ppActions(self):
        for x in self.actions:
            x.pp()

    #todo
    #adjust for intermediateParser: write unwrap method
    def applyAction(self, actionString):
        name = actionString.partition("(")[2].partition(" ")[0]
        action = self.getAction(name)
        lookUpBook = {**self.adjustParameters(action, actionString), **self.pddltypes}
        
        #print(action.precond)
        #check for preconds
        if applyFunction(action.precond, lookUpBook,precondCheck,self.state,True,andOp):
            #applying the allowed change to self.state
            self.state = applyFunction(action.effect, lookUpBook, applyEffect, self.state, self.state, andOp)
            #print("move " + action.name + " allowed")
            return True
        print(action.precond)
        print("action "+ action.name + " NOT allowed")
        return False

        """
        for x in action.precond[0]:
            for y in dict:
                x = x.replace(y, dict[y])
            if (self.state.find(x) < 1):
                print("precondition: " + x + " -not met")
                return False
            """    
        """
            else:
                print("precondition: " + x + " -met")
        
        for x in action.precond[1]:
            for y in dict:
                x = x.replace(y, dict[y])
            if (self.state.find(x) > 0):
                print("neg precondition: " + x + " -not met")
                return False
            else:
                print("neg precondition: " + x + " -met")

        #if preconditions are met apply changes

        for x in action.effect[1]:
            for y in dict:
                x = x.replace(y, dict[y])
            parenthesis = "(" + x + ")\n "
            self.state = self.state.replace(parenthesis, "")

        for x in action.effect[0]:
            for y in dict:
                x = x.replace(y, dict[y])
            parenthesis = "(" + x + ")\n        "
            self.state = self.state + parenthesis

        return True
            """
        
    """
    def mapParameters(self, paramargs, params):
        result = {}
        params = params.partition(" ")[2]
        n = paramargs.count("?")
        x = 0
        while (x < n):
            paramargs = paramargs.partition("?")[2]

            if (paramargs.count(" ") > 0):
                s = "?" + paramargs.partition(" ")[0]
                result[s] = params.partition(" ")[0].replace(")", "")
            elif (paramargs.count(")") > 0):
                s = "?" + paramargs.partition(")")[0]
                result[s] = params.partition(")")[0]

            params = params.partition(" ")[2]
            x += 1
        return result
    
    def splitArgs(self, targetString):
        result = ([],[])
        if (targetString.count("and") > 0):
            targetString = targetString.partition("and")[2]
        
        if (targetString.count("exists") > 0):
            targetString = targetString.partition("(exists")[0]
            
        
        if (targetString.count("forall") > 0):
            targetString = targetString.partition("(forall")[0]
        
        if (targetString.count("increase") > 0):
            targetString = targetString.partition("(increase")[0]
        if (targetString.count("or") > 0):
            targetString = targetString.partition("(or")[0]

        n = targetString.count("(")
        x = 0
        while (x < n):
            targetString = targetString.partition(")")

            if(targetString[0].count("not") == 0):
                result[0].append(targetString[0].partition("(")[2])
                targetString = targetString[2]
            else:
                blah = targetString[0].partition("not")[2].partition("(")[2].partition(")")[0]
                result[1].append(blah)
                targetString = targetString[2].partition(")")[2]    
                x += 1
            x += 1
        return result
    """
    

    def writeChange(self):
        file = open(self.prob)
        tmp = file.read()
        file.close()
        tmpfirst = tmp.partition("init")[0]+"init"
        tmplast = tmp.partition("(:goal")[2]
        result = tmpfirst + self.state.partition("init")[2] + ")\n\n(:goal" + tmplast
        file = open(self.prob, "w")
        file.write(result)
        file.close()

class Claction:
    def __init__(self, name, parameters, precond, effect):
        self.name = name
        self.parameters = parameters
        self.precond = precond
        self.effect = effect
    
    def pp(self):
        print("\nname: " + self.name)
        print("parameters: ")        
        print(self.parameters)        
        print("preconditions: ")        
        print(self.precond)
        print("effects: ")        
        print(self.effect)
        
def changeGoal(prob, newGoal):
    file = open(prob)
    tmp = file.read()
    file.close()
    tmp = tmp.partition("(:goal")
    result = tmp[0] + tmp[1] + "\n    " + newGoal + "\n  )\n)"
    file = open(prob, "w")
    file.write(result)
    file.close()

def addObject(prob, obj, typ = None):
    file = open(prob)
    tmp = file.read()
    file.close()
    if (typ == None):
        tmp = tmp.partition("(:objects")
        result = tmp[0] + tmp[1] + " " + obj + "        \n" + tmp[2]
    else:
        tmp = tmp.partition("- " + typ)
    #bug can occur if type is nonexcistent
        if (tmp[2] == ""):
            return error
        result = tmp[0] + obj + " " + tmp[1] + tmp[2]
    
    file = open(prob, "w")
    file.write(result)
    file.close()


"""
dom = "tmp/domdom.pddl"
prob = "tmp/probcopy.pddl"

ap = ActionParser(dom,prob)

print(ap.state)
ap.applyAction("(pick ball1 rooma left)")
ap.writeChange()
ap.applyAction("(pick ball2 rooma right)")
ap.writeChange()
ap.applyAction("(move rooma roomb)")
ap.writeChange()
ap.applyAction("(drop ball1 roomb left)")
ap.writeChange()
ap.applyAction("(drop ball2 roomb right)")
ap.writeChange()
ap.applyAction("(move roomb rooma)")
ap.writeChange()
ap.applyAction("(pick ball3 rooma left)")
ap.writeChange()
ap.applyAction("(pick ball4 rooma right)")
ap.writeChange()
ap.applyAction("(move rooma roomb)")
ap.writeChange()
ap.applyAction("(drop ball3 roomb left)")
ap.writeChange()

ap.applyAction("(drop ball4 roomb right)")
ap.writeChange()

print(ap.state)
"""