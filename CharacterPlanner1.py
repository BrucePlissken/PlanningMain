import random
import re
from PDDLAccessor import *
from WorldInterface import *
import PlanApi
import ProblemWriter

class CharacterPlanner():
    def __init__(self, world, domain, seed = '', planApi = PlanApi.Cloud_Planner_Api, tmpProbnm = "tmpProb", tmpDomnm = 'tmpDom'):
        self.writer = ProblemWriter.PddlProblemWriter("tmp/" +domain)
        self.pdc = self.writer.pdc
        self.planner = planApi(domain, tmpProbnm + '.pddl')
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
        return self.planner.get_plan()#False)

    def custom_problem(self, new_world, prob_name, goal = "", metric = ""):
        temp = self.writer.unwrap_dict(new_world)
        self.writer.create_problem_file(prob_name, temp[0], temp[1], goal, metric)

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
                        elif smth in self.pdc.pddltypes[pdt]:
                            smth = pdt
                
                oldThing = get_smth(oldWorld, th['name'])
                oldWorld[smth].remove(oldThing)
                oldWorld[smth].append(th)
            
    def mk_character_plan(self, character, world, goal, metric = ""):
        tmp_world = copy.deepcopy(world)
        mk_agent(tmp_world, character)
        if 'actions' in character:
            self.custom_domain(character['actions'])

        self.custom_problem(tmp_world, self.tmpProp, goal, metric)
        #changeGoal('tmp/'+self.tmpProp +'.pddl', goal)
        self.update_problem_address(cp.tmpProp +'.pddl')
        plan = self.run_planner()
        if plan == '':
            return False
        #result = plan_splitter(plan)
        return plan

    def resolve_goals(self, world):
        for c in world["- character"]:
            if "goals" in c:
                #print(c["name"])
                goal = ''
                itL = copy.copy(c['goals'])
                for g in itL:
                    goal = goal + g
                #print(goal)
                plan = self.mk_character_plan(c,world,goal, "(:metric minimize (cost))\n")
                print(plan)
                if not plan:
                    pass
                    """
                    for g in itL:
                        plan = self.mk_character_plan(c,world,goal)
                        if not plan:
                            dg = self.deconstruct_goal(g)
                            #c["goals"].remove(g)
                            if "abstract_goal" not in c["predicates"]:
                                c["predicates"]["abstract_goal"] = []
                            for ag in dg:
                                if ag not in c["predicates"]["abstract_goal"]:
                                    c["predicates"]["abstract_goal"].append(ag)
                    """
                else:
                    plan = plan_splitter(plan)
                    if "plan" not in c:
                        c["plan"] = plan
                    else:
                        c["plan"] = plan
                        
                        #for p in plan:
                        #    c["plan"].append(p)
    """
    def deconstruct_goal(self, goal):
        tmp = goal.partition(' ')[2].rpartition(")")[0]
        return tmp.split()
    """

    def resolve_plan_step(self, world):
        for c in world["- character"]:
            if 'plan' in c:
                p = c['plan'].pop(0)
                #print(p)
                pd = self.disect_plan_action(p)
                #print(pd)
                apply_action_to_world(world, pd)

    def formulate_goals(self, world):
        for c in world['- character']:
            if 'mk_goal_double' in c['predicates']:
                if 'goals' not in c:
                    c['goals'] = []
                
                while(len(c['predicates']['mk_goal_double']) > 1):
                    tmpgoal = []
                    for n in range(3):
                        tmpgoal.append(c['predicates']['mk_goal_double'].pop(0))
                    goal = mk_goal_double(tmpgoal)
                    if goal not in c['goals']:
                        c['goals'].append(goal)
                

def mk_goal_double(goal):
    result = '('
    result = result + goal.pop(0)
    for n in range(len(goal)):
        result = result + ' ' + goal[n]
    result = result + ')'
    return result

def plan_splitter(plan):
    result = re.sub(r'(;.*)', '', plan)
    result = result.strip()
    result = result.split('\n')
    return result
    
"""
testing stuff
"""
import pprint
world = "world.json"
world2 = "redCapWorld.json"
dom = "CharacterPlanningDom.pddl"
dom2 = "redcapdom.pddl"
prob = "OVERHERE.pddl"
cp = CharacterPlanner(world2, dom2)#, planApi=PlanApi.FD_Api)
#cp.custom_domain(['pick_up','move','give'])#,'take','kill','wt_for_sleep'])
cp.update_problem_address(cp.tmpProp +'.pddl')
#pprint.pprint(cp.world)

#c = get_smth(cp.world, "redcap")
#plan = cp.mk_character_plan(c, cp.world, "(inventory wine grandma) (inventory cake grandma)", "(:metric minimize (total-cost))\n")
cp.resolve_goals(cp.world)
#print(plan)
#print(plan)
#c['plan'] = plan_splitter(plan)
cp.resolve_plan_step(cp.world)
cp.resolve_plan_step(cp.world)
cp.formulate_goals(cp.world)
cp.resolve_goals(cp.world)
"""
cp.resolve_plan_step(cp.world)
cp.resolve_goals(cp.world)

pprint.pprint(cp.world)
mom = get_smth(cp.world, 'mom')
goal = ''
for g in rc["goals"]:
    goal = goal + g

plan = cp.mk_character_plan(rc, cp.world, goal)
print(plan)

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
print()
print(plan)
"""