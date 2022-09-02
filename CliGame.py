"""
auth: Jakob Ehlers
a simple cli game for playing around within dynamic stories
"""
from CharacterPlanner1 import *
import DynamicPlanGenerator
import pprint

class CliGame:

    def __init__(self, data) -> None:
        self.cp = CharacterPlanner(data[0], data[1], data[2], planApi=PlanApi.FD_Api)

    def game_loop(self, name):
        run = True
        cp = self.cp
        char = get_smth(cp.world, name)
        db = cp.knowledgedb
        while(run):
            #gather data
            headline = ''
            whereabouts = char['predicates']['whereabouts'][0]
            others = []
            connections = []
            items = []
            name = char['name']
            inventory = char['predicates']['inventory']
            actions = char['actions']

            #changing abstract goals to concrete goals, to be depricated
            if 'mk_goal_double' in char['predicates']:
                formulate_goal(char)


            #using 'find_holders' to get upper connections and ppl at location
            holders = find_holders(cp.world, whereabouts)
            if '- location' in holders:
                for l in holders['- location']:
                    kn = db.get_knldg(name)
                    #print(kn)
                    if (l['name'] in kn):
                        connections.append(l['name'])
            if '- character' in holders:
                for c in holders['- character']:
                    if c['name'] != name:
                        others.append(c['name'])

            #using get smt to find lower connections and items at location
            for i in get_smth(self.cp.world, whereabouts)['predicates']['atloc']:
                it = get_t(self.cp.world,i)
                if it == '- location':
                    if (i in db.get_knldg(name)):
                        connections.append(i)
                if it in ['- item', '- weapon', '- consumable']:
                    items.append(i)

            goals = []
            if 'goals' in char:
                goals = char['goals']
            

            self.std_display(headline, inventory, whereabouts, others, connections, goals, items, actions)
            run = self.input_loop(char,name,whereabouts,connections)

    #waits for player input
    def input_loop(self, char, name, whereabouts, connections):
        while True:
            #collecting input
            x = input('\ninput command: ').split()
            if len(x) > 0:
                #is it exit command? breaks loop by flipping run to false.
                if x[0].lower() in ['quit','exit','q']:
                    return False
                #breaks input loop 
                elif x[0].lower() in ['wait']:
                    self.resolve_actions(self.cp.world, name)
                    return True

                elif x[0].lower() in ['print']:
                    pprint.pprint(self.cp.world)
                    #is the input an action?
                elif (x[0] in char['actions']):
                    #if so attempt to parse it
                    action = self.attempt_parse_action_request(name, x, whereabouts, connections[0]) 
                    if action != False:
                        fails = []
                        for a in action:
                            canDo = check_precondition(self.cp.world, self.cp.disect_plan_action(a))
                            if (canDo[0]):
                                self.resolve_actions(self.cp.world, name, a)
                                return True
                            fails.append(canDo[1])
                        print(f'{action} failed, because {fails}')
                    else:
                        print(f'could not parse action {x[0]}')

                else:
                    print(f'{x[0]} is not an available action')

    #tries to make sense of the players input
    def attempt_parse_action_request(self, name, ls, loc, superloc):
        if len(ls) < 2:
            print(f'missing input to complete action: {ls[0]}')
            return False
        action = []
        if ls[0] == 'move':
            action = ['(' + ls[0] + ' ' + name  + ' ' + loc + ' ' + ls[1] + ' ' + superloc +')',
                      '(' + ls[0] + ' ' + name  + ' ' + loc + ' ' + ls[1] + ' ' + loc +')']
        if ls[0] in ['drop', 'pick_up']:
            action = ['(' + ls[0] + ' ' + name + ' ' + ls[1] + ' ' + loc + ')']
        if ls[0] in ['give', 'kill', 'take', 'talk']:
            if len(ls) < 3:
                print(f'missing input to complete action: {ls[0]}')
                return False
            action = ['(' + ls[0] + ' ' + name + ' ' + ls[1] + ' '+ ls[2] +' '+ loc +')','(' + ls[0] + ' ' + name + ' '+ ls[2] + ' ' + ls[1] +' '+ loc +')']


        return action

    #takes and resolves an action to be applied to a world by a character, followed by other impending actions in the world
    def resolve_actions(self, world, character, action = [], doneList = []):

        if action != []:
            action = [(character, action)]
        impendingActions = action + get_impending_plan_steps(world, blackList= [character] + doneList)

        for a in impendingActions:
            if apply_action_to_world(world, self.cp.disect_plan_action(a[1])):
                print(f'\n{a[0]}, perfomed action: {a[1]}')
                tmp = get_smth(world, a[0], '- character')
                if 'plan' in tmp:
                    if a[1] in tmp['plan']:
                        tmp['plan'].remove(a[1])
                        purge_thing_if_empty(tmp, 'plan')
                self.cp.check_goal_resolved(self.cp.world, tmp)
    

    #dumb text ui
    def std_display(self, headLine = [], inventory = [], whereabouts = [], others = [], connections = [], goals = [], items = [], actions = []):        
        print(f'\n\n\n\n\n\n\n {headLine}')
        if inventory != []:
            print(f'inventory: {inventory}\n')
        if len(goals) > 0:
            print(f'goals: {goals}\n')
        print(f'  you are at {whereabouts}. connections: {connections}')
        if len(others) > 0:
            print(f'  other characters here are: {others}')
        if len(items) > 0:
            print(f'  items here are: {items}')
        print(f'\n  actions: {actions} and  [\'wait\', \'quit\']')


world2 = "Resource/redCapWorld.json"
dom2 = "Resource/redcapdom.pddl"
db2 = 'Resource/redcapknowledgedb.json'

instance = CliGame([world2,dom2,db2])

tchar = get_smth(instance.cp.world, 'redcap')
print (tchar)
print(tchar['actions'])

tmp_world = cp.mk_known_world(cp.world, tchar)

mk_agent(tmp_world, tchar)
if 'actions' in tchar:
    cp.custom_domain(tchar['actions'])

cp.custom_problem(tmp_world, cp.tmpProp)
#changeGoal('tmp/'+self.tmpProp +'.pddl', goal)
cp.update_problem_address(cp.tmpProp)



pprint.pprint(fileToString(cp.tmpDom))

dpg = DynamicPlanGenerator.DPG(cp.tmpDom, cp.tmpProp, lexicon= json.load(open("tmp/RedRidingLex.json")))

instance.game_loop('redcap')
#pprint.pprint(instance.cp.world)