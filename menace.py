import numpy as np
import itertools
import pickle
import tictactoe
import pygame
from pygame.locals import *
# https://raw.githubusercontent.com/nyergler/teaching-python-with-pygame/master/ttt-tutorial/tictactoe.py
class State():
    def __init__(self, state):
        self.state = state
        self.beads = self.init_beads()
    
    def init_beads(self):
        beads = {}
        zero_count = max(self.state.count('0') - 1,2)
        for idx, i in enumerate(self.state):
            if i == '0':
                beads[idx] = zero_count
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

def check_draw(states):
    if states.count('0') == 0:
        return True
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
        
def quit_prompt():
    print('Wanna Quit? Press Y')
    s = input()
    if s == 'Y':
        return True
    return False

def game_on(states, path, ttt):
    try:
        pickle_in = open(path,"rb")
        states = pickle.load(pickle_in)
    except FileNotFoundError:
        pass
    wanna_quit = False
    while(not wanna_quit):
        print("Game Start")
        current_state = list('000000000')
        prnt_game(current_state)
        menacing_steps = []
        menacing_states = []
        while(True):
            # create the game board
            board = tictactoe.initBoard (ttt)
            try:
                row, col = [0,0]
                for event in pygame.event.get():
                    if event.type is QUIT:
                        wanna_quit = True
                        break
                    elif event.type is MOUSEBUTTONDOWN:
                        # the user clicked; place an X or O
                        tictactoe.clickBoard(board)
                        # check for a winner
                        row, col = tictactoe.gameWon(board)
                        a = row * 3 + col
                        if current_state[a] == '0':
                            current_state[a] = '2'
                        else:
                            print('The place is already  filled! Please fill an unoccupied  place')
                            continue
                        if check_win(current_state):
                            give_reward(states, menacing_states, menacing_steps, -1)
                            prnt_game(current_state)
                            print('User won')
                            wanna_quit = quit_prompt()
                            break
                        if check_draw(current_state):
                            give_reward(states, menacing_states, menacing_steps, 1)
                            prnt_game(current_state)
                            wanna_quit = quit_prompt()
                            print('Game Draw')
                            break
                        print('********')
                        print(''.join(current_state))
                        menacing_states.append(tuple(current_state))
                        current_bead = states[''.join(current_state)].get_beads()
                        menacing_steps.append(current_bead)
                        print(current_bead)
                        print('********')
                        row_bead = int(current_bead / 3)
                        col_bead = current_bead % 3
                        tictactoe.drawMove (board, row_bead, col_bead, "O")
                        tictactoe.gameWon(board)
                        if current_state[current_bead] == '0':
                            current_state[current_bead] = '1'
                        else:
                            print('The place is already filled! Please fill an unoccupied place')
                            break
                        if check_win(current_state):
                            give_reward(states, menacing_states, menacing_steps, 3)
                            prnt_game(current_state)
                            print('Menace won')
                            wanna_quit = quit_prompt()
                            break
                        if check_draw(current_state):
                            give_reward(states, menacing_states, menacing_steps, 1)
                            prnt_game(current_state)
                            print('Game Draw')
                            wanna_quit = quit_prompt()
                            break
                        prnt_game(current_state)
                        tictactoe.showBoard(ttt, board)
            except ValueError:
                print('The place is already  filled! Please fill an unoccupied  place')
                continue
    pickle_out = open(path,"wb")
    pickle.dump(states, pickle_out)
    pickle_out.close()

def main():# --------------------------------------------------------------------
# initialize pygame and our window
    pygame.init()
    ttt = pygame.display.set_mode ((300, 325))
    pygame.display.set_caption ('Tic-Tac-Toe')
    path = 'model.pickle'
    all_permutations  = ["".join(seq) for seq in itertools.product("012", repeat=9)]
    states = create_states(all_permutations)
    game_on(states, path, ttt)


if __name__ == "__main__":
    main()
    pass