""" Developed by: Chad Underhill on 9/19/2017 """
""" Based on the theory described here: http://www.renju.nu/wp-content/uploads/sites/46/2016/09/Go-Moku.pdf """
"""
Functionality we need from Board:
size: the size of the board (x or y, should be square)
validMove: check if proposed move is valid?
getTurn: get the current turn from the board (black or white)
    getNot: get the opposite of the current turn from the board)
connect: ???
onBoard: Returns true if position is within board
black:  List of all of black's pieces
white:  List of all of white's pieces
"""
import Queue
import Board as b
import time
import random

"""
The most logical first move is dead-center of the board, so the AI should do just this.
@param:     board   The playing board.
@returns:   A tuple containing the coordinates of the move.
"""


def firstMove(board):
    x = board.size / 2
    return (x, x)


"""
The most strategic second move is diagonal-adjacent to the first placed tile.
This move is more strategic if it's diagonal into the larger area of the board, if possible
@param:     board   The playing board.
@returns:   A tuple containing the coordinates of the move.
"""


def secondMove(board):

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


"""
Randomly chooses a location to place the tile
@param:     board   The playing board.
@returns:   A tuple containing the coordinates of the move.
"""


def randomMove(board):
    go = True
    while go:
        y = random.randint(0, board.size - 1)
        x = random.randint(0, board.size - 1)
        go = not board.validMove((y, x))
    return (y, x)


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


def evalFunction(board, position, mode):

    (y0, x0) = position
    total_consec = 0
    opts = ((1, 0), (0, 1), (1, 1), (1, -1))

    # This is basically just simulating minimax?
    if mode:
        color = board.getTurn()
    else:
        #TODO: This
        color = board.getTurn.getNot()

    #
    for pair in opts:

        #
        (y1, x1) = pair
        pathlist = ["."]

        #
        for j in (1, -1):

            #
            # TODO: Board.connect???
            for i in range(1, board.connect):

                # Determine new coordinates to check for potential impact on position's value
                y2 = y0 + y1 * i * j
                x2 = x0 + x1 * i * j

                x_ol = x2 + x1 * j
                y_ol = y2 + y1 * j
                """
                Check if the projected position is not on the board, is already taken by the opponent,
                    or if move would form an overline. If yes, then break. Otherwise, check to see
                    where the move is added to the list of paths
                """
                if (not board.onBoard((y2, x2)) or board[y2][x2] == color.getNot().symbol) or \
                    (i + 1 == board.connect and board.onBoard((y_ol, x_ol)) and
                     board[y_ol][x_ol] == color.symbol):
                    break
                elif j > 0:  # Insert at back of list if right of position
                    pathlist.append(board[y2][x2])
                elif j < 0:  # Insert at front of list if left of position
                    pathlist.insert(0, board[y2][x2])

        # Determine the number of connections that can be formed at the given position
        paths_num = len(pathlist) - len(board) + 1

        # Determine the total consecutive score for the given position
        if paths_num > 0:
            for i in range(paths_num):
                consec = pathlist[i:i + board.connect].count(color.symbol)

                if consec != board.connect - 1:
                    total_consec += consec**5
                else:
                    if mode:
                        total_consec += 100**9
                    else:
                        total_consec += 100**8

    return total_consec


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


def evaluatePosition(board, position):

    if board.validMove(position):
        return evalFunction(board, position, True) + evalFunction(board, position, False)
    else:
        return 0


"""
Determines the coordinates of connect spaces at a position.
@param:     pair        The starting coordinates in the format (y, x).
@param:     connect     Connect size.
@returns:   A list containing coordinates of connect spaces.
"""


def attackArea(initPair, connect):
    area = []
    opts = ((1, 0), (0, 1), (1, 1), (1, -1))
    (y, x) = initPair

    for pair in opts:
        (y1, x1) = pair

        for s in (1, -1):

            for i in range(1, connect):
                y2 = y + y1 * i * s
                x2 = x + x1 * i * s
                area.append((y2, x2))

    return area


"""
Determines a limited amount of "top moves" based on the evaluatePosition function.
@param:     board       The playing board.
@param:     limit       The number of "top" moves to return.
@returns:   A map of the top moves available along with their values as the key.
"""


def topMoves(board, limit):
    spots = set()
    top_list = []
    top_queue = Queue.PriorityQueue()

    # For each piece on the board
    for n in board.black + board.white:

        # For each potential connect space within range
        for m in attackArea(n, len(board)):

            # If the connect space is on the board, add to list of potential spots
            if board.onBoard(m):
                spots.add(m)

    # Evaluate potential of each spot, and add to queue
    for p in spots:
        top_queue.put((evaluatePosition(board, p) * (-1), p))

    # Pull queue into list
    for x in range(limit):
        top_list.append(top_queue.get())

    # return map(lambda (x, y): (-x, y), top_list)
    return map(lambda x, y: (-x, y), top_list)


''' We don't need this stuff below, should delete before submission

def justBestMoves(board, limit):
    """
    board : board object
    limit : int
    return: list of (int,int)
    The same as topatoms(), but returns only
    moves valued equal to the best valued move
    as rated by evalutate_position(), and the
    list returned does not contain the values
    of the moves returned
    """
    toplist = topatoms(board, limit)
    topval = toplist[0][0]
    bestlist = []
    for atom in toplist:
        (val, move) = atom
        if val == topval:
            bestlist.append(move)
    return bestlist


def nextMove(board, tlimit, dive=1):
    """
    board : board object
    tlimit: float
    dive  : int
    return: (int,int)
    Takes a board, a time limit (tlimit), and a dive number, and
    implements quiescent search dive_#.
    Returns a move where quiescent search predicts a win, or
    the best move according to evalute_position()
    """
    checkTOP_ = 10
    checkDEPTH_ = 20
    atomlist = topatoms(board, checkTOP_)
    mehlist = []
    bahlist = []

    tfract = (tlimit - ((0.1) * (tlimit / 10 + 1))) / float(len(atomlist))
    for atom in atomlist:
        (val, move) = atom
        nextboard = board.move(move)
        if nextboard.win:
            return move
        if dive == 1:
            score = -dive_1(nextboard, checkDEPTH_ - 1)
        elif dive == 2:
            score = -dive_2(nextboard, checkDEPTH_ - 1)
        elif dive == 3:
            score = -dive_3(nextboard, checkDEPTH_ - 1, time.time(), tfract)
        elif dive == 4:
            score = -dive_4(nextboard, time.time(), tfract)
        elif dive == 5:
            score = -dive_5(nextboard, checkDEPTH_ - 1)

        if score == 1:
            # print("This move can force a win")#debug!!!!!!!
            return move
        elif score == 0:
            mehlist.append((score, move))
        elif score > -1:
            bahlist.append((score, move))
    if len(mehlist):
        return mehlist[0][1]
    elif len(bahlist):
        bahlist.sort()
        return bahlist[-1][1]
    else:
        return atomlist[0][1]


""" Different versions of quiescent searches below """

def dive_1(board, dlimit):
    bestmove = topatoms(board, 1)[0][1]
    newboard = board.move(bestmove)
    if newboard.win:
        return 1
    elif not dlimit:
        return 0
    else:
        return -dive_1(newboard, dlimit - 1)


def dive_2(board, dlimit):
    bestmoves = justBestMoves(board, 5)  # maybe widen this window?
    overall = 0.0
    split_factor = 1.0 / len(bestmoves)
    for bmove in bestmoves:
        newboard = board.move(bmove)
        if newboard.win:
            return 1
        elif not dlimit:
            continue
        else:
            score = -dive_2(newboard, dlimit - 1)
            if score == 1:
                return 1
            else:
                overall += split_factor * score
    return overall


def dive_3(board, dlimit, start_tyme, tlimit):
    bestmove = topatoms(board, 1)[0][1]
    newboard = board.move(bestmove)
    if newboard.win:
        return 1
    elif time.time() - start_tyme > tlimit or not dlimit:
        return 0
    else:
        return -dive_3(newboard, dlimit - 1, start_tyme, tlimit)


def dive_4(board, start_tyme, tlimit):
    bestmove = topatoms(board, 1)[0][1]
    newboard = board.move(bestmove)
    if newboard.win:
        return 1
    elif time.time() - start_tyme > tlimit:
        return 0
    else:
        return -dive_4(newboard, start_tyme, tlimit)


def dive_5(board, dlimit):
    TOPCHECK = 3
    bestmoves = topatoms(board, TOPCHECK)
    overall = 0.0
    split_factor = 1.0 / len(bestmoves)
    for bmove in bestmoves:
        newboard = board.move(bmove[1])
        if newboard.win:
            return 1
        elif not dlimit:
            return 0
        else:
            score = -dive_5(newboard, dlimit - 1)
            if score == 1:
                return 1
            elif not score:
                return 0
            else:
                overall += split_factor
    return overall
 '''
