"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided
import time
#import codeskulptor
#codeskulptor.set_timeout(30)

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def trial(board, player):

    empty_sq = board.get_empty_squares()
    len_empsq = len(empty_sq)
    board_dimn = board.get_dim()
    uplim = board_dimn*(board_dimn-1)
    random.shuffle(empty_sq)
    bmove = board.move
    bcheck = board.check_win
    for idx, (row,col) in enumerate(empty_sq):
        bmove(row,col,player)
        player = provided.switch_player(player)
        if (len_empsq - idx <= uplim ) and bcheck() != None:
            return
#        if bcheck() != None:
#            return
        
def update_scores(scores, board, player):
   
    board_dim = board.get_dim()
    winner = board.check_win()
    other = provided.switch_player(player)

    if winner == player:
        score_current = SCORE_CURRENT
        score_other = -1 * SCORE_OTHER
    elif winner == other:
        score_current = -1 * SCORE_CURRENT
        score_other = SCORE_OTHER
    else:
        return
    
    bsquare = board.square
    for row in range(board_dim):
        for col in range(board_dim):
            status = bsquare(row, col)
            if status == player:
                scores[row][col] += score_current
            elif status == other:
                scores[row][col] += score_other

def best_move_grab(board, scores):
   
    empty_squares = board.get_empty_squares()
    if empty_squares == []:
        return
    maxval = -float('inf')
    maxidx = []
    idxapd = maxidx.append
    for idx,(row,col) in enumerate(empty_squares):
        score = scores[row][col]
        if score > maxval:
            maxval = score
            maxidx = [idx]
        elif score == maxval:
            idxapd(idx)
    return empty_squares[random.choice(maxidx)]
            
def move(board, player, trials):
 
    board_dimn = board.get_dim()
    scores = [[0 for _ in range(board_dimn)] for _ in range(board_dimn)]
    bclone = board.clone
    for _ in xrange(trials):
        trial_board = bclone()
        trial(trial_board, player)
        update_scores(scores, trial_board, player)
    return best_move_grab(board, scores)
    
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

poc_ttt_gui.run_gui(3, provided.PLAYERX, move, NTRIALS, False)
