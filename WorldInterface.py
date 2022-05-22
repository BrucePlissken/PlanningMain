import random
from IntermediateParser import *

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

def rnd_t(w):
    l = list(w.keys())
    return random.choices(l)[0]

def rnd_n(w, t):
    i = random.choices(w[t])
    n = i[0]["name"]
    return n

def find_holder(w,n):
    for t in w:
        for c in w[t]:
            for p in c["predicates"]:
                for name in c["predicates"][p]:
                    if name == n:
                        return (t,c)

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

def sorta_get_smth(world, name, lex):
        
    ts = lex['types'][name]
    t = 0
    smth = False
    while (smth == False):
        smth = get_smth(world, name, ts[t])
        t+=1
    return smth

def prec_check(world, precondition, lex):
    result = True
    precondition = quantify_expr_vars(precondition, lex)
    precond = precondition.split()
    prec = precond.pop(0)
    name = precond.pop()

    smth = sorta_get_smth(world, name, lex)

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

    effe = effect.split()
    pred = effe.pop(0)
    name = effe.pop()

    smth = sorta_get_smth(world, name, lex)

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