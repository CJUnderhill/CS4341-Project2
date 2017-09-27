# CS 4341 Project 2
# Last updated: 9/26/2017
# Chad Underhill, Daniel Kim, Spyridon Antonatos
# Based on the theory described here: http://www.renju.nu/wp-content/uploads/sites/46/2016/09/Go-Moku.pdf
"""
Functionality we need from Board:
size: the size of the board (x or y, should be square)
validMove: check if proposed move is valid?
getTurn: get the current turn from the board (black or white)
    getNot: get the opposite of the current turn from the board)
connect: Requirements to win a game (how many in a row do we need?)
onBoard: Returns true if position is within board
black:  List of all of black's pieces
white:  List of all of white's pieces
"""
from queue import *
import Board as b
import time
import random


def firstMove(board):
    """
    The most logical first move is dead-center of the board, so the AI should do just this.
    @param:     board   The playing board.
    @returns:   A tuple containing the coordinates of the move.
    """
    x = board.size / 2
    return (x, x)


def secondMove(board):
    """
    The most strategic second move is diagonal-adjacent to the first placed tile.
    This move is more strategic if it's diagonal into the larger area of the board, if possible
    @param:     board   The playing board.
    @returns:   A tuple containing the coordinates of the move.
    """
    # Get position of first tile
    (y1, x1) = board.black[0]

    if y1 <= board.size / 2:
        y2 = 1
    else:
        y2 = -1

    if x1 <= board.size / 2:
        x2 = 1
    else:
        x2 = -1
    return (y1 + y2, x1 + x2)


def randomMove(board):
    """
    Randomly chooses a location to place the tile
    @param:     board   The playing board.
    @returns:   A tuple containing the coordinates of the move.
    """
    go = True
    while go:
        y = random.randint(0, board.size - 1)
        x = random.randint(0, board.size - 1)
        go = not board.validMove((y, x))
    return (y, x)


def evalFunction(board, position, mode):
    """
    Evaluates the importance of a given position on the board, based on the number of ways
        the board can connect if a tile is placed there. The position is weighted exponentially
        based on the number of pieces that can be connected from that position. The mode controls
        whether the player is "on the attack" or "defending" (think Min/Max?), where connections are
        weighted heavier in attack mode - thus the function prefers taking a winning move in "attack"
        mode over taking a move that blocks another players winning move.
    @param:     board       The playing board.
    @param:     position    Coordinates of a location on the board.
    @param:     mode        Positional strategy. True if "attack", false if "defend".
    @returns:   The importance/strategic value of the position.
    """
    (x0, y0) = position
    evaluation = 0
    opts = ((1, 0), (0, 1), (1, 1), (1, -1))

    # Determine how we're weighing the evaluation (for attack or defend)
    color = board.our_color
    if color == "white":
        not_color = "black"
    else:
        not_color = "white"

    #print("Color: " + color + ", Not Color: " + not_color)

    # Evaluate all neighboring nodes of current position
    for pair in opts:

        # Establish the position and instantiate the pathlist
        (x1, y1) = pair
        pathlist = ["."]

        for j in (1, -1):
            for i in range(1, board.connect):

                # Determine new coordinates to check for potential impact on position's value
                y2 = y0 + y1 * i * j
                x2 = x0 + x1 * i * j
                x_ol = x2 + x1 * j
                y_ol = y2 + y1 * j
                #print("newCoords: " + str(y2) + " " + str(x2) + " " + str(y_ol) + " " + str(x_ol))

                """
                Check if the projected position is not on the board, is already taken by the opponent,
                    or if move would form an overline. If yes, then break. Otherwise, check to see
                    where the move is added to the list of paths
                """
                if (not board.cell_exists(x2, y2) or board.get_cell(x2, y2).color == not_color) or \
                    (i + 1 == board.connect and board.cell_exists(x_ol, y_ol) and
                     board.get_cell(x_ol, y_ol).color == color):
                    break
                elif j > 0:  # Insert at back of list if right of position
                    pathlist.append(board.get_cell(x2, y2).color)
                elif j < 0:  # Insert at front of list if left of position
                    pathlist.insert(0, board.get_cell(x2, y2).color)

        # Determine the number of connections that can be formed at the given position
        paths_num = len(pathlist) - board.connect + 1

        # Determine the total consecutive score for the given position
        if paths_num > 0:
            #print("here5" + str(paths_num))
            for i in range(paths_num):
                if mode:
                    consec = pathlist[i:i + board.connect].count(color)
                else:
                    consec = pathlist[i:i + board.connect].count(not_color)

                if consec != board.connect - 1:
                    if consec != 0:
                        evaluation += 5**consec
                else:
                    if mode:
                        evaluation += 100000
                        print(color + " " + str(mode))
                    else:
                        evaluation += 1000
                #print("evaluation: " + str(evaluation))

    return evaluation


def evaluatePosition(board, position):
    """
    Evaluates the net value of a given position on the board by finding summing the position's
        value to both the player and their opponent. By choosing the position with the most value
        to the player and the most value to the opponent, we are effectively making the move with 
        the greatest offensive and defensive value, thus making it the most strategic. An invalid
        move is returned with an importance value of 0.
    @param:     board       The playing board.
    @param:     position    Coordinates of a location on the board.
    @returns:   The importance/strategic value of the position.
    """
    (x, y) = position
    if board.cell_exists(x, y):
        result = evalFunction(board, position, True) + \
            evalFunction(board, position, False)
        #print("RESULT: " + str(result))
        return result
    else:
        return 0


def attackArea(initPair, connect):
    """
    Determines the coordinates of connect spaces at a position.
    @param:     pair        The starting coordinates in the format (y, x).
    @param:     connect     Connect size.
    @returns:   A list containing coordinates of connect spaces.
    """
    area = []
    opts = ((1, 0), (0, 1), (1, 1), (1, -1))
    (x, y) = initPair

    for pair in opts:
        (x1, y1) = pair

        for s in (1, -1):
            for i in range(1, connect):
                x2 = x + x1 * i * s
                y2 = y + y1 * i * s
                area.append((x2, y2))

    return area


def topMoves(board, limit):
    """
    Determines a limited amount of "top moves" based on the evaluatePosition function.
    @param:     board       The playing board.
    @param:     limit       The number of "top" moves to return.
    @returns:   A map of the top moves available along with their values as the key.
    """
    spots = set()
    top_list = []
    top_queue = PriorityQueue()

    board.print_board()
    # print(board.get_filled_coordinates())

    # For each piece on the board
    for n in board.get_filled_coordinates():

        # For each potential connect space within range
        for m in attackArea(n, board.connect):

            (x, y) = m

            # If the connect space is on the board, add to list of potential spots
            if board.cell_exists(x, y) and m not in board.get_filled_coordinates():
                spots.add(m)

    trackingList = []

    # Evaluate potential of each spot, and add to queue
    for p in spots:
        top_queue.put((evaluatePosition(board, p) * (-1), p))
        #trackingList.append(str((evaluatePosition(board, p) * (-1), p)))

    # print("\nQueue: " + str(trackingList) + "\n")

    for z in range(limit):
        top_list.append(top_queue.get())

    return top_list[0]


def evaluationFunction(board):
    return topMoves(board, 1)
