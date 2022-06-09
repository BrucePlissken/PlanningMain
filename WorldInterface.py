import random
from IntermediateParser import *
import json

def get_smth(w,n,t = ''):
    if t == '':
        for x in w:
            result = get_smth(w,n,x)
            if result != False:
                return result
    elif t in w:
        for m in w[t]:
            if m["name"].lower() == n.lower():
                return m
    return False

def get_t(w, n):
    for t in w:
        for thing in w[t]:
            if thing['name'] == n:
                return t

def rnd_t(w):
    l = list(w.keys())
    return random.choices(l)[0]

def rnd_n(w, t):
    i = random.choices(w[t])
    n = i[0]["name"]
    return n

def find_holders(w,n):
    result = []
    for t in w:
        for c in w[t]:
            for p in c["predicates"]:
                for name in c["predicates"][p]:
                    if name == n:
                        result.append((t,c))
    return result

def check_precondition(world, lex):
    acc = []
    result = True
    applyFunction(lex["precondition"], lex, prec_check_shell, world,acc,andOp)
    for a in acc:
        result = result and a
    return result

def apply_action_to_world(world, lex):
    if check_precondition(world, lex):
        applyFunction(lex["effect"], lex, apply_action_to_world_shell, world, world, andOp)
        return True
    print('precondCheck failed')
    return False

def prec_check(world, precondition, lex):
    result = True
    precondition = quantify_expr_vars(precondition, lex)
    precond = precondition.split()
    prec = precond.pop(0)
    name = precond.pop()

    smth = get_smth(world, name)

    if prec in smth['predicates']:
        for p in precond:
            result = result and (p in smth['predicates'][prec])
    return result

def prec_check_shell(expression, lex, operator, world, acc):
    pc = operator(prec_check(world, expression, lex), True)
    acc.append(pc)

def apply_action_to_world_shell(expression, lex, operator, world, acc):
    remove = operator is notOp
    action_world(world, expression, lex, remove)
    #print(e)

def quantify_expr_vars(expr, lex):
    for y in expr.split():
        if y in lex['vars']:
            expr = expr.replace(y, lex['vars'][y][0])
    return expr

def action_world(world, effect, lex, remove):
    effect = quantify_expr_vars(effect, lex)

    #print(effect)
    effe = effect.split()
    #ignoring func for now
    if len(effe) < 2:
        return
    pred = effe.pop(0)
    name = effe.pop()

    smth = get_smth(world, name)

    if pred in smth['predicates']:
        for p in effe:
            if remove:
                smth['predicates'][pred].remove(p)
            else:
                smth['predicates'][pred].append(p)
    elif effe == []:
        smth['predicates'][pred] = ['']
    else:
        smth['predicates'][pred] = effe
    return smth

def open_world(world):        
    result = json.load(open(world))
    return result

def mk_agent(world, agent):
    if agent in world['- character']:
        world['- character'].remove(agent)
    world["- agent"] = [agent]

def pop_character(world, character = ''):
    if (character == ''):
        n = random.randint(0, len(world["- character"]) -1)
        return world["- character"].pop(n)

def get_character(world, character = ''):
    if (character == ''):
        n = random.randint(0, len(world["- character"]) -1)
        return world["- character"][n]

def formulate_goal(char):
        if 'mk_goal_double' in char['predicates']:
            if 'goals' not in char:
                char['goals'] = []
            #formulates "mk_goal_double"'s into comprehensive goals
            while(len(char['predicates']['mk_goal_double']) > 1):
                tmpgoal = []
                #a mk_goal_double contains three pieces of information; predicate and two vars,
                for n in range(3):
                    tmpgoal.append(char['predicates']['mk_goal_double'].pop(0))
                goal = mk_goal_double(tmpgoal)
                if goal not in char['goals']:
                    char['goals'].append(goal)

def mk_goal_double(goal):
    result = '('
    result = result + goal.pop(0)
    for n in range(len(goal)):
        result = result + ' ' + goal[n]
    result = result + ')'
    return result

#recursively adds types from world, associated to subject, to accumulator
def add_associations(world, subject, acc):
    for p in subject["predicates"]:
        for n in subject["predicates"][p]:
            for t in world:
                x = get_smth(world,n,t)
                if x:
                    if t in acc:
                        acc[t].append(x)
                    else:
                        acc.update({t : [x]})
                    add_associations(world,x,acc)

"""
testing stuff

import json
wld = json.load(open("tmp/world.json"))

ty = rnd_t(wld)
#print(ty)
nm = rnd_n(wld,ty)
#print(nm)
smt = get_smth(wld,ty,nm)
print(smt)
"""
"""
redacted code

def check_precondition_rec(world, precond, lex, acc, nut = False):
    for p in precond:
        if (p == 'and'):
            for x in precond[p]:
                check_precondition_rec(world, x, lex, acc)
        elif (p == 'not'):
            check_precondition_rec(world, precond[p], lex, acc, True)
        elif (p == 'or'):
            tmp = []
            for x in precond[p]:
                check_precondition_rec(world, x, lex, tmp)
            a = False
            for t in tmp:
                if (t):
                    a = t
                    break
            acc.append(a)

        else:
            if nut: 
                return acc.append(not prec_check(world, precond, lex))
            return acc.append(prec_check(world, precond, lex))

"""
