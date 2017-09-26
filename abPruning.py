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

# Time allowed to run minimax until the evaluation function is used
minimax_time = 9

# Checks time to see if minimax_time has been reached
def checkCutOff(startTime):
    currentTime = time.time()
    if currentTime - startTime >= minimax_time:
        return True
    else:
        return False

# "Max" in the minimax algorithm
def maximumValue(state, alpha, beta, startTime):
    if Board.terminalState(state):
        return Board.terminalEval(state)
    if checkCutOff(startTime):
        return Evaluation.evaluationFunction(state)
    value = -math.inf
    for child in Board.children(state):
        value = max(value, minimumValue(child, alpha, beta, startTime))
        if value >= beta:
            return value
        alpha = max(alpha, value)
    return value

# "Min" in the minimax algorithm
def minimumValue(state, alpha, beta, startTime):
    if Board.terminalState(state):
        return Board.terminalEval(state)
    if checkCutOff(startTime):
        return evaluationFunction(Board, 1)[0]
    value = -math.inf
    for child in Board.children(state):
        value = min(value, maximumValue(child, alpha, beta, startTime))
        if value <= alpha:
            return value
        beta = min(beta, value)
    return value

# Alpha-beta pruning algorithm
def minimaxABPruning(gameBoard, startTime):
    startTime = time.time()
    player = gameBoard.to_move(gameBoard.currentState())
    # Make second move
    if (Board(state).secondMove()):
        #replace piece
        return #move
    # Call minVal?
    best_val = -math.inf
    beta = math.inf
    children = gameBoard.children(state)
    best = None
    for child in children:
        value = minimumValue(state, best_val, beta, startTime)
        if value > best_val:
            best_val = value
            best = state
    return best


