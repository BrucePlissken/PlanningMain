import json
import PlanApi
from PDDLAccessor import *
import ProblemWriter
import pprint
import random
from WorldInterface import *

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
                x = get_smth(world,t,n)
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
n_w = {}
cp = CharacterPlanner(world, dom, prob)#, planApi=PlanApi.FD_Api)
cp.custom_domain(['pick_up','move','give','take','kill','wt_for_sleep'])
cp.update_problem_address(cp.tmpProp +'.pddl')

#plan = cp.run_planner()
#print(plan)
#plop = pop_character(cp.world)
agnt = get_character(cp.world)
mk_agent(n_w, agnt)

vict = get_character(cp.world)
n_w.update({"- character" : [vict]})


#goal = "(isdead " + vict["name"] + ")"
it = rnd_n(cp.world, "- item")
holder = find_holder(cp.world,it)

n_w[holder[0]].append(holder[1])

add_associations(cp.world, agnt, n_w)
add_associations(cp.world, vict, n_w)
add_associations(cp.world, holder[1], n_w)

goal = "(inventory " + it + " " + vict["name"] + ")"
cp.custom_problem(n_w, cp.tmpProp)
changeGoal('tmp/'+cp.tmpProp +'.pddl', goal)

cp.update_problem_address(cp.tmpProp +'.pddl')

plan = cp.run_planner()
print()
print(plan)
"""
"""