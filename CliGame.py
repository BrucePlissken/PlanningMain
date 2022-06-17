"""
auth: Jakob Ehlers
a simple cli game for playing around within dynamic stories
"""
from CharacterPlanner1 import *
import pprint

class CliGame:

    def __init__(self, data) -> None:
        self.cp = CharacterPlanner(data[0], data[1], data[2], planApi=PlanApi.FD_Api)

    def game_loop(self, name):
        run = True
        cp = self.cp
        char = get_smth(cp.world, name)
        #this is hardcoding:
        #cp.goals_to_plans(cp.world, get_smth(cp.world, 'mom'))
        while(run):
            #gather data
            whereabouts = char['predicates']['whereabouts'][0]
            others = []
            connections = []
            items = []
            name = char['name']

            #changing abstract goals to concrete goals, to be depricated
            if 'mk_goal_double' in char['predicates']:
                formulate_goal(char)


            #using 'find_holders' to get upper connections and ppl at location
            holders = find_holders(cp.world, whereabouts)
            if '- location' in holders:
                for l in holders['- location']:
                    connections.append(l['name'])
            if '- character' in holders:
                for c in holders['- character']:
                    if c['name'] != name:
                        others.append(c['name'])
            
            if len(connections) == 0:
                connections.append(whereabouts)

            #using get smt to find lower connections and items at location
            for i in get_smth(self.cp.world, whereabouts)['predicates']['atloc']:
                it = get_t(self.cp.world,i)
                if it == '- location':
                    connections.append(i)
                if it in ['- item', '- weapon', '- consumable']:
                    items.append(i)

            goals = []
            if 'goals' in char:
                goals = char['goals']
            
            self.std_display(char, whereabouts, others, connections, goals, items)
            run = self.input_loop(char,name,whereabouts,connections)

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
                        for a in action:
                            canDo = check_precondition(self.cp.world, self.cp.disect_plan_action(a))
                            if (canDo[0]):
                                self.resolve_actions(self.cp.world, name, a)
                                return True
                        print(f'{action} failed, because {canDo[1]}')
                    else:
                        print(f'could not parse action {x[0]}')

                else:
                    print(f'{x[0]} is not an available action')

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
        if ls[0] in ['give', 'kill', 'take']:
            if len(ls) < 3:
                print(f'missing input to complete action: {ls[0]}')
                return False
            action = ['(' + ls[0] + ' ' + name + ' ' + ls[1] + ' '+ ls[2] +' '+ loc +')','(' + ls[0] + ' ' + name + ' '+ ls[2] + ' ' + ls[1] +' '+ loc +')']

        return action

    def resolve_actions(self, world, character, action = [], doneList = []):
        if action != []:
            action = [(character, action)]
        impendingActions = action + get_impending_plan_steps(world, [character] + doneList)
        #print(impendingActions)

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
    def std_display(self, char, whereabouts, others, connections, goals, items):        
        print(f'\n\n\n\n\n\n\ninventory: {char["predicates"]["inventory"] }\n')
        if len(goals) > 0:
            print(f'goals: {goals}\n')
        print(f'  you are at {whereabouts}. connections: {connections}')
        if len(others) > 0:
            print(f'  other characters here are: {others}')
        if len(items) > 0:
            print(f'  items here are: {items}')
        print(f'\n  actions: {char["actions"]} and [\'wait\', \'quit\']')


world2 = "redCapWorld.json"
dom2 = "redcapdom.pddl"
db2 = 'redcapknowledgedb.json'

instance = CliGame([world2,dom2,db2])
instance.game_loop('redcap')
#pprint.pprint(instance.cp.world)