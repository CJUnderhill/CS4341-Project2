# CS 4341 Project 2
# Last updated: 9/26/2017
# Chad Underhill, Daniel Kim, Spyridon Antonatos
#
# Usage:
#       Contains methods for running the alpha-beta pruning algorithm.
import math
import time
#import Evaluation
import Board

# Depth allowed to run minimax until the evaluation function is used
minimax_depth = 10

# Checks depth to see if minimax_depth has been reached
def checkCutOff(currentDepth):
    if currentDepth >= minimax_depth:
        return True
    else:
        return False

# "Max" in the minimax algorithm
def maximumValue(state, alpha, beta, depth):
    result = state.check_terminal_state()
    if result:
        if result == "tie":
            return 0
        else:
            return float(result)
    if checkCutOff(depth):
        #print("in eval")
        #Evaluation.evaluationFunction(state)
        return 1.0
    value = -math.inf
    for child in state.get_children():
        value = max(value, minimumValue(child, alpha, beta, depth+1))
        if value >= beta:
            return value
        alpha = max(alpha, value)
    return value

# "Min" in the minimax algorithm
def minimumValue(state, alpha, beta, depth):
    result = state.check_terminal_state()
    if result:
        if result == "tie":
            return 0
        else:
            return float(result)
    if checkCutOff(depth):
        #print("in eval min")
        #Evaluation.evaluationFunction(state)
        return 1.0
    value = math.inf
    for child in state.get_children():
        value = min(value, maximumValue(child, alpha, beta, depth+1))
        if value <= alpha:
            return value
        beta = min(beta, value)
    return value

# Alpha-beta pruning algorithm
def minimaxABPruning(gameBoard):
    player = gameBoard.color_turn
    # Make second move
    if (gameBoard.number_filled_cells == 1 and
        gameBoard.board["H8"].color == gameBoard.color_next_turn):
        #replace piece
        return Move
    best_val = -math.inf
    beta = math.inf
    children = gameBoard.get_children()
    best = None
    for child in children:
        value = minimumValue(child, best_val, beta, 1)
        if value > best_val:
            best_val = value
            best = child
    return best

# TESTING
b1 = Board.Board("black")

##b1.make_move("A","1")
##b1.make_move("A","2")
##
##b1.make_move("A","3")
##
##b1.make_move("A","4")
##
##b1.make_move("A","5")
##
##b1.make_move("B","2")
##b1.make_move("C","3")
##b1.make_move("D","4")
##b1.make_move("D","5")
##
##b1.make_move("D","6")
##
##b1.make_move("D","7")
##b1.make_move("D","8")
##
##b1.make_move("E","5")
##b1.make_move("F","6")

for i in range(15):
    b1.make_move("A", str(i+1))
for i in range(15):
    b1.make_move("E", str(i+1))
##for i in range(15):
##    b1.make_move("B", str(i+1))
##for i in range(15):
##    b1.make_move("F", str(i+1))
##for i in range(15):
##    b1.make_move("C", str(i+1))
##for i in range(15):
##    b1.make_move("G", str(i+1))
##for i in range(15):
##    b1.make_move("D", str(i+1))
##for i in range(15):
##    b1.make_move("K", str(i+1))
##for i in range(15):
##    b1.make_move("I", str(i+1))
##for i in range(15):
##    b1.make_move("L", str(i+1))
##for i in range(15):
##    b1.make_move("J", str(i+1))
##for i in range(15):
##    b1.make_move("M", str(i+1))
##for i in range(15):
##    b1.make_move("H", str(i+1))
##for i in range(15):
##    b1.make_move("N", str(i+1))
##for i in range(12):
##    b1.make_move("O", str(i+1))
b1.print_board()
b2 = minimaxABPruning(b1)
print(b2)
b2.print_board()
