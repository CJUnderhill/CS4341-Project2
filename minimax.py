""" Developer: Chad Underhill on 9/17/2017 """
"""
Functionality we need from Board:
filledSpaces: a list of filled spaces on the board
emptyNeighbors: a list of empty neighbors given a starting coordinate
eval: a numeric "score" for the board state given the combinations of already-placed stones
isTie: checks if board is filled and no winner has been determined. True if tie.
isVictory: checks if board has a winner. True if winner has emerged.
placeStone: plays stone on board
"""
from random import choice
from copy import deepcopy
from itertools import chain


class Minimax:
    """
    Class outlining the Minimax algorithm, which attempts to minimize the possible loss in a worst-case scenario.
    The algorithm assumes that the first place is maximizing their chance of winning, and the opponent is trying
        to minimize the first player's chance of winning.
    """

    VIC_SCORE = 2**32

    def filledSpots(self, board):
        """
        Finds the filled spots on the board.
        @param: board   The board to read.
        @returns:   A list containing all the filled spaces on the board.
        """
        # i: current position being evaluated on the board
        return list(chain.from_iterable(board.filledSpaces(board.board, i) for i in [1, -1]))

    def emptyNeighbors(self, board, filled_spots):
        """
        Finds the empty neighbors on the board.
        @param: board           The board to read.
        @param: filled_spots    A list of filled spots on the board.
        @returns:   A list containing all the empty neighbors on the board.
        """
        # i: current position being evaluated on the board
        # 1: radius being evaluated
        return list(chain.from_iterable(board.emptyNeighbors(board.board, i, 1) for i in filled_spots))

    def abPruning(self, board, depth, alpha, beta, player):
        """
        Improves the runtime and memory usage of the traditional Minimax algorithm by systematically eliminating
            nodes we can prove do not need to be evaluated.
        @param:	self	A Minimax object
        @param:	board	The Board object
        @param:	depth	Max depth to explore before ending recursion
        @param:	alpha	Max score that Max player is tracking
        @param:	beta	Min score that Min player is tracking
        @param:	player	The current player making a move
        @returns:	Tuple containing determined score and next move
        """

        """
        Get map from board
        TODO: Get filled_spaces and empty_neighbors from board
        """
        filled_spots = self.filledSpots(board)
        empty_neighbors = self.emptyNeighbors(board, filled_spots)

        # Determine moves from list of empty neighbors
        empty_board = board.filledSpaces(board.board, 0)
        pot_moves = sorted(
            list(set(empty_board).intersection(empty_neighbors)))

        # If no moves exist, then final moves list is empty
        if pot_moves:
            final_moves = pot_moves
        else:
            final_moves = empty_board

        # If we're at our last possible move before ending recursion
        # TODO: Ensure Board has proper evaluate function
        if depth == 0:
            final_val = board.eval(board.board, player)

            if len(final_moves) == 0 or board.isTie():
                # It's a tie/draw!
                print("Draw!")

            if board.isVictory():
                final_val += self.VIC_SCORE

            return final_val, final_moves[0]

        move = None

        # Loop through list of possible final moves
        while final_moves:

            # Pick a new move and clone the board
            # TODO: Replace place_stone function with something better (named)
            next_move = choice(final_moves)
            tmp_board = deepcopy(board)
            tmp_board.placeStone(player, next_move)

            #
            if tmp_board.isVictory():
                return self.VIC_SCORE, next_move

            # Check next depth
            tmp = self.abPruning(tmp_board, depth - 1, alpha, beta, -player)
            tmp_score = tmp[0]

            # Handle scorekeeping for each player through AB Pruning
            if player == 1:  # Max
                if tmp_score < beta:
                    beta = tmp_score
                    move = next_move
                if alpha >= beta:
                    break
            elif player == -1:  # Min
                if tmp_score > alpha:
                    alpha = tmp_score
                    move = next_move
                if alpha >= beta:
                    break

            # Remove this move and try the next
            final_moves.remove(next_move)

        # Determine score based on final player
        if player == 1:
            score = beta
        else:
            score = alpha

        return score, move
