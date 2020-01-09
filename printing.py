def make_reports(modules, scores, moves):
    section0 = make_section0(modules, scores)
    section1 = make_section1(modules, scores)
    section2 = make_section2(modules, scores)

    section3 = []
    for index in range(len(modules)):
        section3.append(make_section3(modules, moves, scores, index))
    return section0, section1, section2, section3

def make_section0(modules, scores):
    '''
    Produce the following string:
    ----------------------------------------------------------------------------
    Section 0 - Line up
    ----------------------------------------------------------------------------
    Player 0 (P0): Team name 0, Strategy name 0,
         Strategy 0 description
    Player 1 (P1): Team name 1, Strategy name 1, 
         Strategy 1 description
    '''
    section0 = '-'*80+'\n'
    section0 += 'Section 0 - Line up\n'
    section0 += '-'*80+'\n'
    for index in range(len(modules)):
        section0 += 'Player ' + str(index) + ' (P' + str(index) + '): '
        section0 += str(modules[index].team_name) + ', ' + str(modules[index].strategy_name) + '\n'
        strategy_description = str(modules[index].strategy_description)
        # Format with 8 space indent 80 char wide
        while len(strategy_description) > 1:
            newline = strategy_description[:72].find('\n')
            if newline> -1:
                section0 += ' '*8 + strategy_description[:newline+1]
                strategy_description = strategy_description[newline+1:]
            else:
                section0 += ' '*8 + strategy_description[:72] + '\n'
                strategy_description = strategy_description[72:]
    return section0

def make_section1(modules, scores):
    '''
    ----------------------------------------------------------------------------
    Section 1 - Player vs. Player
    ----------------------------------------------------------------------------
    A column shows pts/round earned against each other player:      
                P0    P1         
    vs. P0 :     0   100          
    vs. P1 :  -500     0             
    TOTAL  :  -500   100
    '''
    # First line
    section1 = '-'*80+'\nSection 1 - Player vs. Player\n'+'-'*80+'\n'
    section1 += 'Each column shows pts/round earned against each other player:\n'
    # Second line
    section1 += '        '
    for i in range(len(modules)):
        section1 += '{:>7}'.format('P'+str(i))
    section1 += '\n'
    # Add one line per team
    for index in range(len(modules)):
        section1 += 'vs. P' + str(index) + ' :'
        for i in range(len(modules)):
            section1 += '{:>7}'.format(int(float(scores[i][index])))
        section1 += '\n'

    # Last line
    section1 += 'TOTAL  :'
    for index in range(len(modules)):
        section1 += '{:>7}'.format(int(sum([float(i) for i in scores[index]])))
    return section1+'\n'

def make_section2(modules, scores):
    '''
    ----------------------------------------------------------------------------
    Section 2 - Leaderboard
    ----------------------------------------------------------------------------
    Average points per round:
    Team name (P#):  Score       with strategy name
    Champ10nz (P0):   100 points with Loyal
    Rockettes (P1):  -500 points with Backstabber
    '''
    section2 = '-'*80+'\nSection 2 - Leaderboard\n'+'-'*80+'\n'
    section2 += 'Average points per round:\n'
    section2 += 'Team name (P#):  Score      with strategy name\n'

    # Make a list of teams' 4-tuples
    section2_list = []
    for index in range(len(modules)):
        section2_list.append((modules[index].team_name,
                              'P'+str(index),
                              str(sum(scores[index])/len(modules)),
                              str(modules[index].strategy_name)))
    section2_list.sort(key=lambda x: int(float(x[2])), reverse=True)

    # Generate one string per team
    # Rockettes (P1):  -500 points with Backstabber
    for team in section2_list:
        team_name, Pn, n_points, strategy_name = team
        section2 += '{:<10}({}): {:>10} points with {:<40}\n'.format(team_name[:10], Pn, int(float(n_points)), strategy_name[:40])
    return section2

def make_section3(modules, moves, scores, index):
    '''Return a string with information for the player at index, like:
    ----------------------------------------------------------------------------
    Section 3 - Game Data for Team Colloid c=-500 b=-250 C=0 B=+100
    ----------------------------------------------------------------------------
    -133 pt/round: Colloid (P6) "Collude every 3rd round"
    -233 pt/round: 2PwnU (P8) "Betray, then alternate"
    bBcBbCbBcBbCbBcBbCbBcBbCbBcBbCbBcBbCbBcBbCbBcBbCbBcBbCbBcBbCbBcBbCbBcBbCbBcB
    bcBcbCbcbcbCBcbcbCBcbcbCBcbcbCBcbcbCBcbcbCBcbcbCBcbcbCBcbcbCBcbcbCBcbcbCBcbc
    '''
    section3:str = '-'*80+'\nSection 3 - Game Data for Team '
    section3 += modules[index].team_name + '\n'
    section3 += '-'*80+'\n'
    # Make 4 lines per opponent
    for opponent_index in range(len(modules)):
        if opponent_index != index:
            # Line 1
            section3 += str(scores[index][opponent_index])
            section3 += ' pt/round: ' + modules[index].team_name +'(P'
            section3 += str(index)+') "'+modules[index].strategy_name + '"\n'
            # Line 2
            section3 += str(scores[opponent_index][index])
            section3 += ' pt/round: ' + modules[opponent_index].team_name +'(P'
            section3 += str(opponent_index)+') "'+modules[opponent_index].strategy_name + '"\n'
            # Lines 3-4
            hist1, hist2 =  capitalize(moves[index][opponent_index], moves[opponent_index][index])
            while len(hist1) > 1:
                section3 += hist1[:80] + '\n'
                section3 += hist2[:80] + '\n\n'
                hist1 = hist1[80:]
                hist2 = hist2[80:]
            section3 += '-'*80 + '\n'
    return section3


def capitalize(history1:str, history2:str)->(str,str):
    '''Accept two strings of equal length.
    Return the same two strings but capitalizing the opponent of 'c' each round.
    '''
    caphistory1, caphistory2 = '', ''
    for p1, p2 in zip(history1, history2):
        if p1 == 'c':
            p2 = p2.upper()
        if p2 in 'cC':
            p1 = p1.upper()
        caphistory1 += p1
        caphistory2 += p2
    return caphistory1, caphistory2
