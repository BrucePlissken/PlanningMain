from CharacterPlanner1 import *

def game_loop(char_planner, name):
    run = True
    cp = char_planner
    char = get_smth(cp.world, name)
    while(run):
        whereabouts = char['predicates']['whereabouts'][0]
        others = []
        connections = []
        items = []
        actions = char['actions']
        inventory = char['predicates']['inventory']


        #using 'find_holders' to get upper connections and ppl at location
        for h in find_holders(cp.world, whereabouts):
            if h[0] == '- location':
                connections.append(h[1]['name'])
            if h[0] == '- character':
                if h[1]['name'] != name:
                    others.append(h[1]['name'])
        if len(connections) == 0:
            connections.append(whereabouts)

        #using get smt to find lower connections and items at location
        for i in get_smth(cp.world, whereabouts)['predicates']['atloc']:
            it = get_t(cp.world,i)
            if it == '- location':
                connections.append(i)
            if it in ['- item', '- weapon', '- consumable']:
                items.append(i)

        #dumb text ui
        print(f'\n\n\n\n\n\n\ninventory: {inventory}\n')
        print(f'  you are at {whereabouts} connections: {connections}')
        if len(others) > 0:
            print(f'  other characters here are: {others}')
        if len(items) > 0:
            print(f'  items here are: {items}')
        print(f'\n  actions: {actions} and [\'wait\', \'quit\']')

        flop = True
        while flop:
            #collecting input
            x = input('\ninput command: ').split()

            #is it exit command? breaks loop by flipping run to false.
            if x[0].lower() in ['quit','exit','q']:
                return
            #breaks input loop
            if x[0].lower() in ['wait']:
                flop = False
            #is the input an action?
            elif (x[0] in actions):
                #if so attempt to parse it
                action = attempt_parse_action_request(name, x, whereabouts, connections[0]) 
                if action != False:

                    if (check_precondition(cp.world, cp.disect_plan_action(action))):
                        print(action)
                        flop = False                
                    else:
                        print(f'{action} was not applied to world')
                else:
                    print(f'could not parse action {x[0]}')

            else:
                print(f'{x[0]} is not an available action')

def attempt_parse_action_request(name, ls, loc, superloc):
    if len(ls) < 2:
        print(f'missing input to complete action: {ls[0]}')
        return False
    action = ''
    if ls[0] == 'move':
        action = '(' + ls[0] + ' ' + name  + ' ' + loc + ' ' + ls[1] + ' ' + superloc +')'
    if ls[0] in ['drop', 'pick_up']:
        action = '(' + ls[0] + ' ' + name + ' ' + ls[1] + ' ' + loc + ')'
    if ls[0] in ['give', 'kill', 'take']:
        if len(ls) < 3:
            print(f'missing input to complete action: {ls[0]}')
            return False
        action = '(' + ls[0] + ' ' + name + ' ' + ls[1] + ' '+ ls[2] +' '+ loc +')'

    return action


world2 = "redCapWorld.json"
dom2 = "redcapdom.pddl"
cp = CharacterPlanner(world2, dom2, planApi=PlanApi.FD_Api)


game_loop(cp, 'redcap')