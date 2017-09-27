#!python
#cython: language_level=3, boundscheck=False

# CS 4341 Project 2
# Last updated: 9/26/2017
# Chad Underhill, Daniel Kim, Spyridon Antonatos
#
# Usage:
#       Contains methods for running the alpha-beta pruning algorithm.
import math
import time
import Evaluation
import Board

# Depth allowed to run minimax until the evaluation function is used
MAX_NODES_VISITED = 10
nodes_visited = 0
MAX_DEPTH = 2
TIME_START = time.time()
TIME_STOP = 5

# Checks to see if the evaluation function should be used
def checkCutOff(currentDepth):
    global nodes_visited, MAX_NODES_VISITED, MAX_DEPTH, TIME_START, TIME_STOP
    if (currentDepth >= MAX_DEPTH) or (nodes_visited >= MAX_NODES_VISITED) or (time.time() - TIME_START >= TIME_STOP):
        return True
    else:
        return False

# "Max" in the minimax algorithm
def maximumValue(state, alpha, beta, depth):
    global nodes_visited
    nodes_visited += 1
    # Check for terminal states
    result = state.check_terminal_state()
    if result:
        if result == "tie":
            return 0
        else:
            return float(result)
    # Check for time to use evaluation function
    if checkCutOff(depth):
        return Evaluation.evaluationFunction(state)[0]
    # Maximize
    #state.print_board()
    value = -math.inf
    for child in state.get_children():
        value = max(value, minimumValue(child, alpha, beta, depth+1))
        if value >= beta:
            return value
        alpha = max(alpha, value)
    return value

# "Min" in the minimax algorithm
def minimumValue(state, alpha, beta, depth):
    global nodes_visited
    nodes_visited += 1
    # Check for terminal states
    result = state.check_terminal_state()
    if result:
        if result == "tie":
            return 0
        else:
            return float(result)
    # Check for time to use evaluation function
    if checkCutOff(depth):
        return Evaluation.evaluationFunction(state)[0]
    # Minimize
    #state.print_board()
    value = math.inf
    for child in state.get_children():
        value = min(value, maximumValue(child, alpha, beta, depth+1))
        if value <= alpha:
            return value
        beta = min(beta, value)
    return value

# Minimax algorithm with alpha-beta pruning
def minimaxABPruning(gameBoard):
    global TIME_START
    TIME_START = time.time()
    # Current player
    player = gameBoard.color_turn
    # Make second move
    if (gameBoard.number_filled_cells == 1 and
        gameBoard.board["H8"].color == gameBoard.color_next_turn):
        # Replace middle piece
        gameBoard.board["H8"].color = gameBoard.color_turn
        return gameBoard #MOVE
    # Maximize first
    alpha = -math.inf
    beta = math.inf
    children = gameBoard.get_children()
    bestMove = None
    for child in children:
        # Call minimumValue() to start the recursion
        value = minimumValue(child, alpha, beta, 1)
        if value > alpha:
            alpha = value
            bestMove = child
    return bestMove
