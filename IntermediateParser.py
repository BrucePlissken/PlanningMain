import re

def prsExp(expstr):

    if (expstr[0:4] == "and "):
        result = andOrLoop(expstr)
        #print("ending *and")
        return {"and" : result}
    
    if (expstr[0:4] == "not "):
        #print("hit 'not'")
        return {"not" : prsExp(nextExpr(expstr)[1])}

    if (expstr[0:3] == "or "):
        #print("hit 'or'")
        result = andOrLoop(expstr)
        return {"or" : result}

    if (expstr[0:7] == "exists "):
        #print("hit exists-loop")
        result = andOrLoop(expstr)
        return {"exists" : result}

    if (expstr[0:7] == "forall "):
        #print("hit forall-loop")
        result = andOrLoop(expstr)
        return {"forall" : result}

    if (expstr[0:9] == "increase "):
        #print("hit increase")
        val = int(expstr.rpartition(")")[2])
        return {"increase" : prsExp(nextExpr(expstr)[1]),
                    "value" : val
        }
    if (expstr[0:5] == "when "):
        #print("hit when")
        result = andOrLoop(expstr)
        return {"when" : result}

    if (expstr[0:2] == "= "):
        #equality not implemented
        return {"=": prsExp(expstr.partition("=")[2])}

    if (isSingleExpr(expstr)):
        return expstr
    #print("reached end")
    return "not intended"

#check to see if the string contains a bare-bones expression statement
def isSingleExpr(expstr):
    if (expstr.count("(") == 0):
        return True
    return False

#loops through expressions comming in line
def andOrLoop(expstr):
    result = []
    expr = nextExpr(expstr)
    while (True):
        #print(result)
        result.append(prsExp(expr[1]))
        if (expr[2] == ")"):
            break
        expr = nextExpr(expr[2])

    return result
    
#strips outer parenthensis and returns the next expression in line
def nextExpr(exprString):
    i = 1
    result = ""

    for x in exprString.partition("(")[2]:
        if (x == "("):
            i += 1
        if (x == ")"):
            i -= 1
        if (i == 0):
            if (result != ""):
                thingy = exprString.partition(result)
                return thingy
            else:
                print("Kurt Carpenter")
                return False
        result += x

#outer method for convenience of running the parser
def parsePddlExpression(expression):
    return prsExp(nextExpr(whiteSpaceMatters(expression))[1])

#removes most of the whitespace between expressions
def whiteSpaceMatters(expression):
    result = re.sub("\s*\(", "(", expression)
    result = re.sub("\)\s*", ")", expression)
    return result.lower()

def applyFunction(expressions, lookUpbook, func, pddlProblem, acc, operator):

    if(isinstance(expressions, dict)):
        
        if "and" in expressions:
            for e in expressions["and"][::-1]:
                #print("and...")
                acc = applyFunction(e, lookUpbook, func, pddlProblem, acc, andOp)
                #print(acc)
        
        if "or" in expressions:
            for e in expressions["or"]:
                #print("or")
                #this should probably be the way it is implemented across the board
                acc =  orOp(applyFunction(e, lookUpbook, func, pddlProblem, acc, nonOp), acc)
        
        if "not" in expressions:
            if(isinstance(expressions, list)):
                for e in expressions["not"]:    
                    acc = applyFunction(e, lookUpbook, func, pddlProblem, acc, notOp)
            else:
                acc = applyFunction(expressions["not"], lookUpbook, func, pddlProblem, acc, notOp)

        if "increase" in expressions:
                acc = func(expressions["increase"], lookUpbook, addOp, pddlProblem, acc)

        if "exists" in expressions:
            typ = expressions["exists"][0].partition(" -")
            typs = pddlProblem.partition("-" + typ[2])[0].rpartition("\n")[2].split()
           #print("exists")
            for x in typs:
                pamphlet = lookUpbook
                #print(typ[0] +" "+ x)
                pamphlet[typ[0]] = x 
                temp = applyFunction(expressions["exists"][1], pamphlet, stringReplacer, pddlProblem, "", andOp )
                
                #temp = applyFunction(expressions["exists"][1], lookUpbook, stringReplacer, typ[0] +" "+ x, "", andOp )

                #print(temp)
                temp = parsePddlExpression(temp)
                #print(temp)
                acc = applyFunction(temp, lookUpbook, func, pddlProblem, acc, andOp)

        if "forall" in expressions:
            typi = expressions["forall"][0].partition(" -")
            typ = "-" + typi[2]
            typs = pddlProblem.partition(typ)[0].rpartition("\n")[2].split()
            if typ in lookUpbook:
                for x in lookUpbook[typ]:
                    #print(x + ".")
                    temp = pddlProblem.partition(" - " + x)[0].rpartition("\n")[2].split()
                    #print(temp)
                    if (temp != []):
                        for x in temp:
                            typs.append(x)
            
           #print("forall")
            #print(typ)
            #print(typs)
            for x in typs:
                #print(x)
                pamphlet = lookUpbook
                #print(typ[0] +" "+ x)
                pamphlet[typi[0]] = x 
                #print("blah")
                temp = applyFunction(expressions["forall"][1], pamphlet, stringReplacer, pddlProblem, "", andOp)
                #print("blah2")
                if (temp == ""):
                    continue
                temp = parsePddlExpression(temp)
                #print(temp)
                acc = applyFunction(temp, lookUpbook, func, pddlProblem, acc, andOp)
                #print(acc)

        if "when" in expressions:
            

            condition = applyFunction(expressions["when"][0], lookUpbook, func, pddlProblem, acc, nonOp)
            #print(condition)
            condition = applyFunction(condition, lookUpbook, precondCheck, pddlProblem, True, andOp)
            #print(condition)
            #print("when")
            #print(expressions["when"][0])
            #print(expressions["when"][1])
            #print(acc)
            if (condition):
                    #cannot handle multiple statements at this point
                    acc = applyFunction(expressions["when"][1], lookUpbook, func, pddlProblem, acc, andOp)
                    #print("just one")
                    #print(expressions["when"][1])
                    #print(acc)

        return acc
        
    return func(expressions, lookUpbook, operator, pddlProblem, acc)

def stringReplacer(expression, lookUpbook, operator, pddlProblem, acc):
    #print("stringreplacer")
    for y in expression.split():
        if y in lookUpbook:
            expression = expression.replace(y, lookUpbook[y])
#    result = expression.replace(temp[0], temp[1])
    #print("result")
    
    #print(expression)
    result = operator(expression, acc)
    #print(result)
    return result

def ifOp(it, em):
    if type(it) is bool:
        if(it):
            return em
        else:
            return not em
    elif type(it) is str:
        return "(when (" + it + ") " +em +")"

def nonOp(it, em):
    if type(it) is bool:
        return it & em
    elif type(it) is str:
        return "(" + it + ")"


def andOp(it, em):
    if type(it) is bool:
        return it & em
    elif type(it) is str:
        return "(and (" + it + ") " + em +")"

def notOp(it, em):
    #print("not")
    if type(it) is bool:
        return (not it) & em
    elif type(it) is str:
        return "(not (" + it + ")) " +em 

def orOp(it, em):
    if type(it) is bool:
        return it | em
    elif type(it) is str:
        return "(or (" + it + ") " +em +")" 

def addOp(it,em):
    if type(it) is bool:
        return it


def printExpression(expression, noot, pddlProblem, number = 0):
    result = expression
    
    if (not noot):
        result = "not " + expression
    if (number != 0):
        result = "increase " + result + " by " + str(number)

    #print(result)

def precondCheck(expression, lookUpbook, operator, pddlProblem, acc):
    #if (number != 0):
    #    return True
    #print("precond check")
    #print(lookUpbook)
    #print("precond check")
    
    for y in expression.split():
        if y in lookUpbook:
            expression = expression.replace(y, lookUpbook[y])
    result = (pddlProblem.count(expression) > 0)
    #print("pC expression: " + expression)
    #print(pddlProblem)
    result = operator(result,  acc)
    #if (not result & acc):
       #print(expression)
       #print(operator)
       #print(result)
    return result 

def applyEffect(expression, lookUpbook, operator, pddlProblem, acc):
    #print("applyEffect")
    #print(expression)
    #print(lookUpbook)
    for y in expression.split():
            if y in lookUpbook:
                expression = expression.replace(y, lookUpbook[y])
    parenthesis = "    (" + expression + ")\n"
    if (operator == addOp):
        return acc
    if (operator == notOp):
        acc = acc.replace(parenthesis, "")
    elif (operator == ifOp):
        print("ifop")
        #print(acc)
        
    else: 
        acc = acc + parenthesis
    #print("applyEffect2")
    #print(acc)
    return acc




"""
pfff = " (and (not (atloc dudeascii town)) (atloc dudeascii town))\n    (increase (total-cost) 22)\n    ))\n"
p = "(not (atloc dudeascii farm))"
f ="(not (isSecret ?to))"    
pff = "(and (atLoc ?char1 ?from) (atLoc ?char2 ?from) (not (isSecret ?to))\n(isAvailable ?char2) (or (and (not (isSus ?char2)) (not (isBound ?char2))) (and (isSus ?char2) (isBound ?char2))) (exists (?sus - monster) (or (not (atLoc ?sus ?from)) (isDead ?sus)\n)))\n)"
hep = parsePddlExpression(pff)
prob = open("tmp/AdventureProb.pddl")
prob2 = prob.read()
prob.close()
blah = applyFunction(hep, precondCheck, prob2, True, andOp)
print(blah)

print(prob)
print(hep)
#print(whiteSpaceMatters(pfff))
#print(parsePddlExpression(pfff))
pf = "(and (atLoc ?char1 ?from) (atLoc ?char2 ?from) (isAvailable ?char2))"
"""