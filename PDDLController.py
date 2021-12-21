import PDDLAccessor
import IntermediateParser
from IntermediateParser import *

class PDDLController:
    def __init__(self, domain, prob):
        self.domainFile = domain
        self.problemFile = prob
        self.domain = PDDLAccessor.fileAsString(domain).lower()
        self.problem = PDDLAccessor.fileAsString(prob).lower()
        self.state = PDDLAccessor.getSection("init", self.problem)
        
        self.actions = []
        n = self.domain.count("action")
        tempDom = self.domain
        while (n > 0):
            tempDom = tempDom.partition("action ")[2]
            action = PDDLAccessor.parseAction(tempDom.partition("\n")[0], self.domain)
            self.actions.append(action)
            n -= 1

        self.pddltypes = self.mapTyps()

    def getAction(self, name):
        for x in self.actions:
            if (x.get("name") == name):
                return x
        print("error: no such action name: " + name)

    def adjustParameters(self, action, params):
        paramargs = action.get("parameters") 
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

    #returns a dict of the different types in the domain
    def mapTyps(self):
        typs = PDDLAccessor.getSection("types", self.domain)
        result = {}
        i = typs.count("-")
        while (i > 0):
            kvpair = typs.partition("-")
            k = "-" + kvpair[2].partition("\n")[0]
            v = kvpair[0].rpartition("\n")[2].split()
            result[k] = v
            typs = typs.partition(k)[2]
            i -=1
        
        return result
    #applies an action from an action string expression eg. (actionName arg1 arg2) with the variables filled out
    def applyAction(self, actionString):
        name = actionString.partition("(")[2].partition(" ")[0]
        action = self.getAction(name)
        lookUpBook = {**self.adjustParameters(action, actionString), **self.pddltypes}
        
        #check for precondition satisfaction
        if (applyFunction(action.get("precondition"), lookUpBook, precondCheck, self.state,True,andOp)):
            #applying the allowed change to self.state
            self.state = applyFunction(action.get("effect"), lookUpBook, applyEffect, self.state, self.state, andOp)
            return True
        #on failure:
        print("action "+ actionString + " NOT allowed")
        return False

    #applies the current state (:init...) to the pddl problem file
    def writeChange(self):
        tmp = self.problem
        tmpfirst = tmp.partition("init")[0]+"init"
        tmplast = tmp.partition("(:goal")[2]
        result = tmpfirst + self.state.partition("init")[2] + ")\n\n(:goal" + tmplast
        file = open(self.problemFile, "w")
        file.write(result)
        file.close()