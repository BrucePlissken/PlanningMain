import random

def get_smth(w,t,n):
    for m in w[t]:
        if m["name"] == n:
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
