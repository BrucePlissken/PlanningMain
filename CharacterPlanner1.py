import random
from PDDLAccessor import *
from mockdbapi import MockDbJs
from WorldInterface import *
import PlanApi
import ProblemWriter

class CharacterPlanner:
    def __init__(self, world, domain, databaseadress, databaseApi = MockDbJs, planApi = PlanApi.Cloud_Planner_Api, tmpProbnm = "tmp/tmpProb.pddl", tmpDomnm = 'tmp/tmpDom.pddl', seed = ''):
        self.writer = ProblemWriter.PddlProblemWriter(domain)
        self.pddlcontroler = self.writer.pdc
        self.planner = planApi(domain, tmpProbnm)
        self.world = json.load(open(world))
        self.tmpProp = tmpProbnm
        self.tmpDom = tmpDomnm
        self.knowledgedb = databaseApi(databaseadress)
        if (seed != ''):
            random.seed(seed)

    def update_problem_address(self, problem):
        self.planner.prob = problem
        self.planner.updateParams()

    def update_domain_address(self, domain):
        self.planner.dom = domain
        self.planner.updateParams()

    def run_planner(self, show = False ):
        return self.planner.get_plan(show)

    def custom_problem(self, new_world, prob_name, goal = "", metric = ""):
        #pprint.pprint(new_world)
        temp = self.writer.unwrap_dict(new_world)
       # pprint.pprint(temp[1])
        self.writer.create_problem_file(prob_name, temp[0], temp[1], goal, metric)

    def custom_domain(self, actions):
        dom = self.writer.domain.partition('\n(:action')
        result = dom[0]
        for a in actions:
            tmp = '\n(:action ' + a +'\n    '
            pff = getSection(a,dom[2])
            if pff == '':
                continue
            result = result + tmp + pff
        result = result + '\n)'
        f = open(self.tmpDom+'.pddl','w')
        f.write(result)
        f.close()
        self.update_domain_address(self.tmpDom+'.pddl')

    #check wether goals of a char have been achieved in a world, and if so removes the goal from the list of goals and if empty removes the entry from char
    def check_goal_resolved(self, world, char):
        name = char['name']
        if 'goals' in char:
            for g in char['goals']:
                prec = g.replace('(', '').replace(')','')
                lex = copy.deepcopy(self.pddlcontroler.pddltypes)
                lex.update({'precondition' : prec,
                            'vars' : []}) 
                if check_precondition(world, lex):
                    print(f'{name} resolved goal: {g}')
                    remove_item_from_thing(char, 'goals', g)

    #takes in a plan-action and returns a dict of info for feeding to the intermediate parser
    def disect_plan_action(self, planAction):
        result_t = {}
        result_v = {}
        pa = planAction.replace('(', '').replace(')','').split()
        name = pa.pop(0)
        action = self.pddlcontroler.getAction(name)
        tmp = []
        for x in action["parameters"].replace('(', '').replace(')','').split():
            if(x[0] == '?'):
                result_v[x] = [pa[0]]
                tmp.append(pa.pop(0))
            elif(x[0] == '-'):
                pass
            else:
                for t in tmp:
                    tis = get_t(self.world, t)
                    if tis:
                        tis = tis.split()[1]
                        #r_v = ['- ' + x]
                        r_v = ['- ' + tis]
                        for pdt in self.pddlcontroler.pddltypes:
                            if tis in self.pddlcontroler.pddltypes[pdt]:
                                r_v.append(pdt)
                        result_t[t] = r_v
                        if ('- ' + x in r_v or (x == 'agent' and '- character' in r_v)):
                            pass
                        else:
                            strong = f'{t} is not - {x}, but - {tis}'
                            return strong
                    else:
                        strong = f'there is no {t}'
                        return strong
                tmp = []
        return {'types' : result_t, 'vars' : result_v, 'precondition': action['precondition'], 'effect': action['effect']}

    def update_world(self, oldWorld, newWorld):
        for smth in newWorld:
            for th in newWorld[smth]:
                if smth not in oldWorld:
                    for pdt in self.pddlcontroler.pddltypes:
                        if smth.partition(' ')[2] in self.pddlcontroler.pddltypes[pdt]:
                            smth = pdt
                        elif smth in self.pddlcontroler.pddltypes[pdt]:
                            smth = pdt
                
                oldThing = get_smth(oldWorld, th['name'])
                oldWorld[smth].remove(oldThing)
                oldWorld[smth].append(th)
            
    def mk_character_plan(self, character, world, goal, metric = "", show = False):
        #tmp_world = copy.deepcopy(world)
        tmp_world = self.mk_known_world(world, character)
        mk_agent(tmp_world, character)
        if 'actions' in character:
            self.custom_domain(character['actions'])

        self.custom_problem(tmp_world, self.tmpProp, goal, metric)
        #changeGoal('tmp/'+self.tmpProp +'.pddl', goal)
        self.update_problem_address(self.tmpProp)
        plan = self.run_planner(show)
        if plan == '':
            return False
        #result = plan_splitter(plan)
        return plan

    #takes a world and a character, and returns a world with the characters imediate associations
    #to be expanded upon, perhaps with a database of known things... thinking of some one to many sql shenanigans
    def mk_known_world(self, world, character):
        known_world = {'- character': [character],
                     '- pred': world['- pred']}
        add_associations(world, character, known_world)

        pfft = find_holders(world, character['predicates']['whereabouts'][0])
        merge_worlds(known_world, pfft)
        #pprint.pprint(known_world)


        #goal loop for adding goal specific info. This might be replaced in it's entirety as knowledge db gets implemented
        """
        goalthings = goal.replace('(', ' ')
        goalthings = goalthings.replace(')', ' ')
        goalthings = goalthings.split()
        
        for gt in goalthings:
            oldthing = get_smth(world, gt)
            if oldthing != False:
                intemp = get_smth(known_world, gt)
                if intemp == False:
                    tp = get_t(world, gt)
                    tmp = { tp : [oldthing]}
                    merge_worlds(known_world, tmp)
        """
        
        known = self.knowledgedb.get_knldg(character['name'])
        for k in known:
            q = []
            if not get_smth(known_world, k):
                t = get_t(world, k)
                smth = copy.copy(get_smth(world, k, t))
                for p in smth["predicates"]:
                    #print(smth["name"])
                    #print(smth["predicates"][p])
                    for i in smth["predicates"][p]:
                        #print(i)
                        if i not in known:
                            q.append(i)
                for s in q:    
                    smth["predicates"][p].remove(s)
                tmp = {t:[smth]}
                merge_worlds(known_world,tmp)

        return known_world

    def goals_to_plans(self, world, c):
        if "goals" in c:
            #print(c["name"])
            goal = ''
            itL = copy.copy(c['goals'])
            for g in itL:
                goal = goal + g
            #print(goal)
            plan = self.mk_character_plan(c,world,goal, "(:metric minimize (total-cost))\n")
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

    def apply_plan_step(self, world):
        for c in world["- character"]:
            if 'plan' in c and len(c['plan']) > 0:
                p = c['plan'].pop(0)
                #print(p)
                pd = self.disect_plan_action(p)
                #print(pd)
                apply_action_to_world(world, pd)


    
    
"""
testing stuff
"""

world2 = "Resource/redCapWorld.json"
dom2 = "Resource/redcapdom.pddl"
db2 = 'Resource/redcapknowledgedb.json'


data = [world2,dom2,db2]
cp = CharacterPlanner(data[0], data[1], data[2], planApi=PlanApi.Cloud_Planner_Api)

WI_test = ['(move redcap moms_house village village)', '(pick_up redcap cake moms_house)', '(move redcap village path path)','(move redcap moms_house grandmas_house village)','(move redcap path village path)','(move redcap village moms_house village)']
WI_results = []

for test in WI_test:
    WI_results.append(check_precondition(cp.world, cp.disect_plan_action(test))[0])

for test in WI_test:
    WI_results.append(apply_action_to_world(cp.world, cp.disect_plan_action(test)))

WI_expected = [True,True,False,False,False,False, True,False,True,False,True,True]

#print(f' results: {results}')

if WI_results == WI_expected:
    print('WI-test success')
else: 
    print('WI-test failure')


c = get_smth(cp.world, "redcap")
plan = cp.mk_character_plan(c, cp.world, "(inventory wine grandma) (inventory cake grandma)", "(:metric minimize (total-cost))\n", show = False)

if plan != False:
    plan = plan_splitter(plan)

plan_test =['(pick_up redcap wine moms_house)',
'(pick_up redcap cake moms_house)',
'(move redcap moms_house village village)',
'(move redcap village path path)',
'(move redcap path forrest path)',
'(move redcap forrest grandmas_house forrest)',
'(give redcap grandma wine grandmas_house)',
'(give redcap grandma cake grandmas_house)',]

if plan == plan_test:
    print('plan-test success')
else:
    print(f'plan-test failure {plan}')


"""
world = "world.json"
world2 = "redCapWorld.json"
dom = "CharacterPlanningDom.pddl"
dom2 = "redcapdom.pddl"
prob = "OVERHERE.pddl"
db2 = 'redcapknowledgedb.json'
cp = CharacterPlanner(world2, dom2, db2, planApi=PlanApi.FD_Api)
#cp.custom_domain(['pick_up','move','give'])#,'take','kill','wt_for_sleep'])
#cp.update_problem_address(cp.tmpProp +'.pddl')
#pprint.pprint(cp.world)

c = get_smth(cp.world, "redcap")
plan = cp.mk_character_plan(c, cp.world, "(inventory wine grandma) (inventory cake grandma)", "(:metric minimize (total-cost))\n")
cp.resolve_goals(cp.world)
#print(plan)
#print(plan)
#c['plan'] = plan_splitter(plan)
cp.apply_plan_step(cp.world)
cp.apply_plan_step(cp.world)
formulate_goal(get_smth(cp.world, 'redcap'))
cp.resolve_goals(cp.world)


cp.apply_plan_step(cp.world)

cp.resolve_plan_step(cp.world)
cp.resolve_plan_step(cp.world)
pprint.pprint(cp.world)
cp.resolve_goals(cp.world)

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