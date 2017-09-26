# Minimax + alpha-beta pruning algorithm
import math
import time

def checkCutOff(startTime):
    currentTime = time.time()
    if currentTime - startTime >= 9:
        return True
    else:
        return False

def maximumValue(state, alpha, beta, startTime):
    if GomokuBoard.terminalState(state):
        return GomokuBoard.terminalEval(state)
    if checkCutOff(startTime):
        return evaluationFunction(state)
    value = -math.inf
    for child in GomokuBoard.children(state):
        value = max(value, minimumValue(child, alpha, beta, startTime))
        if value >= beta:
            return value
        alpha = max(alpha, value)
    return value

def minimumValue(state, alpha, beta, startTime):
    if GomokuBoard.terminalState(state):
        return GomokuBoard.terminalEval(state)
    if checkCutOff(startTime):
        return evaluationFunctino(state)
    value = -math.inf
    for child in GomokuBoard.children(state):
        value = min(value, maximumValue(child, alpha, beta, startTime))
        if value <= alpha:
            return value
        beta = min(beta, value)
    return value

def minimaxABPruning(gameBoard, startTime):
    startTime = time.time()
    player = gameBoard.to_move(gameBoard.currentState())
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

