import numpy as np
import itertools
class State():
    def __init__(self, state):
        self.state = state
        self.beads = self.init_beads()
    
    def init_beads(self):
        beads = {}
        for idx, i in enumerate(self.state):
            if i == '0':
                beads[idx] = 4
        return beads
    
    def get_beads(self):
        rand = np.random.rand(1)
        values = np.array(list(self.beads.values()))
        keys = np.array(list(self.beads.keys()))
        print(values)
        values = values / np.sum(values)
        print(values)
        prob = 0
        for  idx, i in enumerate(values):
            prob += i
            if rand < prob:
                self.beads[keys[idx]] -= 1
                return keys[idx]
        
    def set_beads(self, key, reward):
        self.beads[key] += reward

def create_states(all_permutations):
    states = {}
    for string in all_permutations:
        states[string] = State(string)
    return states

def check_win_case(i,j,k, state):
    if(state[i] == state[j] and state[i] == state[k] and state[i] != '0'):
        return True
    return False
def check_win(state):
    if check_win_case(0,4,8, state):
        return True
    elif check_win_case(0,1,2,state):
        return True
    elif check_win_case(0,3,6,state):
        return True
    elif check_win_case(1,4,7,state):
        return True
    elif check_win_case(2,4,6,state):
        return True
    elif check_win_case(2,5,8,state):
        return True
    elif check_win_case(3,4,5,state):
        return True
    elif check_win_case(6,7,8,state):
        return True
    else:
        return False

def give_reward(states, menacing_states, menacing_steps, reward):
    for idx, state in enumerate(menacing_states):
        print(''.join(list(state)))
        print(menacing_steps[idx], idx)
        print(states[''.join(list(state))].beads)
        states[''.join(list(state))].set_beads(menacing_steps[idx], reward)
        print(states[''.join(list(state))].beads)

def prnt_game(state):
    for idx, i in enumerate(state):
        print(i + ' | ', end='')
        if (idx+1)%3 == 0:
            print('\n- | - | -')
        

def game_on(states):
    while(True):
        print("Game Start")
        current_state = list('000000000')
        menacing_steps = []
        menacing_states = []
        while(True):
            try:
                a = int(input())
                if a < 1 or a > 9:
                    print('Chutiye sahi se bhar')
                    continue
                a -= 1
                if current_state[a] == '0':
                    current_state[a] = '2'
                else:
                    print('Chutiye sahi se bhar')
                    continue
                if check_win(current_state):
                    give_reward(states, menacing_states, menacing_steps, -1)
                    prnt_game(current_state)
                    print('User won')
                    break
                print('********')
                print(''.join(current_state))
                menacing_states.append(tuple(current_state))
                current_bead = states[''.join(current_state)].get_beads()
                menacing_steps.append(current_bead)
                print(current_bead)
                print('********')
                if current_state[current_bead] == '0':
                    current_state[current_bead] = '1'
                else:
                    print('Chutiye sahi se bhar')
                    break
                if check_win(current_state):
                    give_reward(states, menacing_states, menacing_steps, 3)
                    prnt_game(current_state)
                    print('Menace won')
                    break
                prnt_game(current_state)
            except ValueError:
                print('Chutiye sahi se bhar')
                continue

def main():
    all_permutations  = ["".join(seq) for seq in itertools.product("012", repeat=9)]
    states = create_states(all_permutations)
    print(states[all_permutations[33]].beads, all_permutations[33])
    game_on(states)
    pass

if __name__ == "__main__":
    main()
    pass