from utils import *
from parameters import BOARD

if __name__ == "__main__":

    team1, team2, BOARD = start(BOARD)
    show_map(BOARD)
    turn = True

    while team1 and team2:
        print('The game must go on.')
        if turn:
            print('Team 1 turn.')
        else:
            print('Team 2 turn.')

        print('In your turn you can move a unit in one of the four directions [up, down, left, right]',
              'or attack with one unit.')
        action = input("Whats your choice? ")

        if action == 'move':
            u = input('Chose your unit entering its id: ')
            if turn:
                u = search_unit(team1, u)
            else:
                u = search_unit(team2, u)
            if u == 0:
                print('That unit not yours.')
            else:
                d = input('Chose the direciton: ')
                new_position = movement(u, d, BOARD)

        elif action == 'attack':
            u = input('Chose your unit for the attack: ')
            if turn:
                u = search_unit(team1, u)
            else:
                u = search_unit(team2, u)
            t = input('Chose the target with the id: ')
            if not turn:
                t = search_unit(team1, t)
            else:
                t = search_unit(team2, t)
            if u == 0 or t == 0:
                print('Invalid units')
            else:
                attack_result = attack(u, t, BOARD)
                if attack_result != 0:
                    if turn:
                        team2.remove(t)
                    else:
                        team1.remove(t)
        else:
            print("You can't do this action, you lose your turn")

        turn = not turn
        show_map(BOARD)
    else:
        if team1:
            print('Team 1 wins')
        else:
            print('Team 2 wins')
