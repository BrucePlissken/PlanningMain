import json
import PlanApi
from PDDLAccessor import *
import ProblemWriter
import pprint
import random
from WorldInterface import *
import re

class CharacterPlanner():
    def __init__(self, world, domain, problem = '', seed = '', planApi = PlanApi.Cloud_Planner_Api, tmpProbnm = "tmpProb", tmpDomnm = 'tmpDom'):
        self.writer = ProblemWriter.PddlProblemWriter("tmp/" +domain)
        self.pdc = self.writer.pdc
        self.planner = planApi(domain, problem)
        self.world_loc = "tmp/" + world
        self.world = open_world(self.world_loc)
        self.tmpProp = tmpProbnm
        self.tmpDom = tmpDomnm
        if (seed != ''):
            random.seed(seed)

    def update_problem_address(self, problem):
        self.planner.prob = problem
        self.planner.updateParams()

    def update_domain_address(self, domain):
        self.planner.dom = domain
        self.planner.updateParams()

    def run_planner(self):
        return self.planner.get_plan()

    def custom_problem(self, new_world, prob_name):
        temp = self.writer.unwrap_dict(new_world)
        self.writer.create_problem_file(prob_name, temp[0], temp[1])

    def custom_domain(self, actions):
        dom = self.writer.domain.partition('\n(:action')
        result = dom[0]
        for a in actions:
            tmp = '\n(:action ' + a +'\n    '
            pff = getSection(a,dom[2])
            result = result + tmp + pff
        result = result + '\n)'
        f = open('tmp/'+self.tmpDom+'.pddl','w')
        f.write(result)
        f.close()
        self.update_domain_address(self.tmpDom+'.pddl')

    def disect_plan_action(self, planAction):
        result_t = {}
        result_v = {}
        pa = planAction.replace('(', '').replace(')','').split()
        name = pa.pop(0)
        action = self.pdc.getAction(name)
        tmp = []
        for x in action["parameters"].replace('(', '').replace(')','').split():
            if(x[0] == '?'):
                result_v[x] = [pa[0]]
                tmp.append(pa.pop(0))
            elif(x[0] == '-'):
                pass
            else:
                for t in tmp:
                    r_v = ['- ' + x]
                    for pdt in self.pdc.pddltypes:
                        if x in self.pdc.pddltypes[pdt]:
                            r_v.append(pdt)
                    
                    result_t[t] = r_v
                tmp = []

        return {'types' : result_t, 'vars' : result_v, 'precondition': action['precondition'], 'effect': action['effect']}

    def update_world(self, oldWorld, newWorld):
        for smth in newWorld:
            for th in newWorld[smth]:
                if smth not in oldWorld:
                    for pdt in self.pdc.pddltypes:
                        if smth.partition(' ')[2] in self.pdc.pddltypes[pdt]:
                            smth = pdt
                
                pff = get_smth(oldWorld, th['name'])
                oldWorld[smth].remove(pff)
                oldWorld[smth].append(th)
            
    def mk_character_plan(self, character, world, goal):
        mk_agent(world, character)
        self.custom_problem(world, self.tmpProp)
        changeGoal('tmp/'+self.tmpProp +'.pddl', goal)
        self.update_problem_address(cp.tmpProp +'.pddl')
        result = self.run_planner()
        result = re.sub(r'(;.*)', '', result)
        result = result.strip()
        
        result = result.split('\n')
        return result
        

def open_world(world):        
    result = json.load(open(world))
    return result

def mk_agent(world, agent):
    world["- agent"] = [agent]

def pop_character(world, character = ''):
    if (character == ''):
        n = random.randint(0, len(world["- character"]) -1)
        return world["- character"].pop(n)

def get_character(world, character = ''):
    if (character == ''):
        n = random.randint(0, len(world["- character"]) -1)
        return world["- character"][n]

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
"""
world = "world.json"
dom = "CharacterPlanningDom.pddl"
prob = "OVERHERE.pddl"
cp = CharacterPlanner(world, dom, prob)#, planApi=PlanApi.FD_Api)
cp.custom_domain(['pick_up','move','give','take','kill','wt_for_sleep'])
cp.update_problem_address(cp.tmpProp +'.pddl')

n_w = {}
agnt = get_character(cp.world)

vict = get_character(cp.world)
n_w.update({"- character" : [vict]})


it = rnd_n(cp.world, "- item")
holder = find_holder(cp.world,it)

n_w[holder[0]].append(holder[1])



add_associations(cp.world, agnt, n_w)
add_associations(cp.world, vict, n_w)
add_associations(cp.world, holder[1], n_w)

goal = "(inventory " + it + " " + vict["name"] + ")"


plan = cp.mk_character_plan(agnt, n_w,goal)

for n in range(len(plan)):
    dis = cp.disect_plan_action(plan[n])
    apply_action_to_world(n_w, dis)

cp.update_world(cp.world, n_w)
#pprint.pprint(cp.world)


print(goal)
print()
print(plan)
print()
#print(dis)

#pprint.pprint(cp.world)
print()

pprint.pprint(n_w)
"""
print()
print(plan)
"""