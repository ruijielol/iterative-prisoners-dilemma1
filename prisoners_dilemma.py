#####
# Computer Science and Software Engineering
# PLTW AP CS Principles
# (c)2014 Project Lead The Way, Inc.
#
# Activity 1.3.9 Tools for Collaboration
# Project 1.3.10 Collaborating on a Project
#
# To run a tournament, execute this file.
# Place each team's strategy in a file in the same directory as this file.
# Tournament results saved to tournament.txt in this directory.
#
# prisoners_dilemma.py automates competition among different strategies
# for the Iterative Prisoners Dilemma, the canonical game of game-theory.
# Each strategy is pitted against each other strategy for 100 to 200 rounds.
# The results of all previous rounds within a 100-200 round stretch are known
# to both players.
#
# play_tournament([team0, team1, team2]) executes a tournament and writes to tournament.txt
#
# Each team's strategy should be coded in their assigned Python file, called a module.
# Each player should have their own .py file containing
# three strings team_name, strategy_name, and strategy_description
# and a function move(my_history, their_history, my_score, their_score)
#
# By default, when executing this file, [example0, example1, example2, example3]
# play a tournament. To run the tournament of [team, team1, team1, example1]:
# scores, moves, reports = main_play([team1]*3+[example1])
# section0, section1, section2, section3 = reports
#######
import os.path
import random

#examples and teams now in separate folder
from examples import (example0, example1, example2, example3, example4,
                      example5, example6, example7, example8)
from period5 import (team0, team1, team2, team3, team4, team5, team6, team7,
                     team8, team9, team10, team11, team12, team13, team14)
from printing import capitalize, make_reports

betray = example1
collude = example0

example_modules = [example0, example1, example2, example3, example4, example5, example6, example7,]

team_modules = [team0, team2, team3, team5, team10, team11, team12, team13]

modules = team_modules

for module in modules:
    # reload(module)
    # print ('reloaded',module)
    for required_variable in ['team_name', 'strategy_name', 'strategy_description']:
        if not hasattr(module, required_variable):
            setattr(module, required_variable, 'missing assignment')

def main_play(modules):
    '''main_play plays a tournament and outputs results to screen and file.
    This function is called once when this file is executed.
    modules: a list of modules such as [team1, team2]    
    
    Returns:
        scores:
        moves:
        sections: a list of [str, str, str, list of str]    
            '''
    scores, moves = play_tournament(modules)
    section0, section1, section2, section3 = make_reports(modules, scores, moves)
    # On screen, include the first three out of four sections of the report.
    print(section0+section1+section2)
    # To file output, store all teams' code and all teams' section 3 reports.
    post_to_file(section0+section1+section2 + ''.join(section3))
    return scores, moves, [section0, section1, section2, section3]

def play_tournament(modules):
    '''Each argument is a module name
    Each module must contain 
        team_name: a string
        strategy_name: a string
        strategy_description: a string
        move: A function that returns 'c' or 'b'
    '''
    zeros_list = [0]*len(modules) # to initialize each player's head-to-head scores
    scores = [zeros_list[:] for module in modules] # Copy it or it's only 1 list
    moves = [zeros_list[:] for module in modules] # Copy it or it's only 1 list
    for first_team_index in range(len(modules)):
        for second_team_index in range(first_team_index):
            player1 = modules[first_team_index]
            player2 = modules[second_team_index]
            score1, score2, moves1, moves2 = play_iterative_rounds(player1, player2)
            scores[first_team_index][second_team_index] = score1/len(moves1) # int division not an issue
            moves[first_team_index][second_team_index] = moves1
            # Redundant, but record this for the other player, from their perspective
            scores[second_team_index][first_team_index] = score2/len(moves2)
            moves[second_team_index][first_team_index] = moves2
        # Playing yourself doesn't do anything
        scores[first_team_index][first_team_index] = 0
        moves[first_team_index][first_team_index] = ''
    return scores, moves


def play_iterative_rounds(player1, player2):
    '''
    Plays a random number of rounds (between 100 and 200 rounds) 
    of the iterative prisoners' dilemma between two strategies.
    player1 and player2 are modules.
    Returns 4-tuple, for example ('cc', 'bb', -200, 600) 
    but with much longer strings 
    '''
    number_of_rounds = random.randint(100, 200)
    moves1 = ''
    moves2 = ''
    score1 = 0
    score2 = 0
    for round in range(number_of_rounds):
        score1, score2, moves1, moves2 = play_round(player1, player2, score1, score2, moves1, moves2)
    return (score1, score2, moves1, moves2)

def play_round(player1, player2, score1, score2, moves1, moves2):
    '''
    Calls the move() function from each module which return
    'c' or 'b' for collude or betray for each player.
    The history is provided in a string, e.g. 'ccb' indicates the player
    colluded in the first two rounds and betrayed in the most recent round.
    Returns a 2-tuple with score1 and score2 incremented by this round
    '''

    RELEASE = 0 # (R, "reward" in literature) when both players collude
    TREAT = 100 # (T, "temptation" in literature) when you betray your partner
    SEVERE_PUNISHMENT = -500 # (S, "sucker" in literature) when your partner betrays you
    PUNISHMENT = -250 # (P) when both players betray each other

    # Keep T > R > P > S to be a Prisoner's Dilemma
    # Keep 2R > T + S to be an Iterative Prisoner's Dilemma

    ERROR = -250

    # Get the two players' actions and remember them.
    action1 = player1.move(moves1, moves2, score1, score2)
    action2 = player2.move(moves2, moves1, score2, score1)
    if (type(action1) != str) or (len(action1) != 1):
        action1=' '
    if (type(action2) != str) or (len(action2) != 1):
        action2=' '

    # Change scores based upon player actions.
    actions = action1 + action2
    if actions == 'cc':
        # Both players collude; get reward.
        score1 += RELEASE
        score2 += RELEASE
    elif actions == 'cb':
        # Player 1 colludes, player 2 betrays; get severe, treat.
        score1 += SEVERE_PUNISHMENT
        score2 += TREAT
    elif actions == 'bc':
        # Player 1 betrays, player 2 colludes; get treat, severe.
        score1 += TREAT
        score2 += SEVERE_PUNISHMENT
    elif actions == 'bb':
        # Both players betray; get punishment.
        score1 += PUNISHMENT
        score2 += PUNISHMENT
    else:
        # Both players get the "error score" if someone's code returns an improper action.
        score1 += ERROR
        score2 += ERROR

    # Append the actions to the previous histories.
    if action1 in 'bc':
        moves1 += action1
    else:
        moves1 += ' '
    if action2 in 'bc':
        moves2 += action2
    else:
        moves2 += ' '

    # Return scores incremented by this round's results.
    return (score1, score2, moves1, moves2)

def post_to_file(string, filename='tournament.txt', directory=''):
    '''Write output in a txt file.
    '''
    # Use the same directory as the python script
    if directory=='':
        directory = os.path.dirname(os.path.abspath(__file__))
    # Name the file tournament.txt
    filename = os.path.join(directory, filename)
    # Create the file for the round-by-round results
    filehandle = open(filename,'w')
    filehandle.write(string)

### Call main_play() if this file is executed
if __name__ == '__main__':
    scores, moves, reports = main_play(modules)
    section0, section1, section2, section3 = reports
