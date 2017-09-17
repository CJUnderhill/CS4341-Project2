# Developer: Chad Underhill on 9/17/2017
# 

from copy import deepcopy
from itertools import chain
from random import choice

# Class outlining the Minimax algorithm, which attempts to minimize the possible loss in a worst-case scenario.
# The algorithm assumes that the first place is maximizing their chance of winning, and the opponent is trying
#	to minimize the first player's chance of winning.
class Minimax():

	# Improves the runtime and memory usage of the traditional Minimax algorithm by systematically eliminating
	#	nodes we can prove do not need to be evaluated.
	# @param:	self	A Minimax object
	# @param:	board	The Board object
	# @param:	depth	The depth of the current move within the AB Pruning tree
	# @param:	alpha	The tracked A value
	# @param:	beta	The tracked B value
	# @param:	player	The current player making a move
	# @returns:	Tuple containing determined score and next move
	def abPruning(self, board, depth, alpha, beta, player):

		# Get map from board
		# TODO: Turn this into individual function calls
		# TODO: Get filled_spaces and empty_neighbors from board
		filled_spots = list(chain.from_iterable(board.filled_spaces(board.board, i) for i in [1, -1]))
		empty_neighbors = list(chain.from_iterable(board.empty_neighbors(board.board, i, 1) for i in filled_spots))

		# Determine moves from empty board
		all_empty = board.filled_spaces(board.board, 0)
		moves = sorted(list(set(all_empty).intersection(empty_neighbors)))

		# If no moves exist, then final moves list is empty
		final_move_list = all_empty if not moves else moves

		# If we're at our last possible move
		if depth == 0:
			final_val = board.evaluate(board.board, player)
			if len(final_move_list) == 0 or board.draw():
				# It's a tie/draw!
			if board.victory():
				final_val += 2**32
			return final_val, final_move_list[0]

		move = None

		# Loop through list of possible final moves
		while final_move_list:

			# Pick a new move and clone the board
			# TODO: Replace place_stone function with something better (named)
			new_move = choice(final_move_list)
			temp_board = deepcopy(board)
			temp_board.place_stone(player, new_move)

			#
			if temp_board.victory():
				return 2**32, new_move

			# Recursively call abPruning function
			temp = self.abPruning(temp_board, depth - 1, alpha, beta, -player)

			# Handle scorekeeping for each player
			if player == -1:
				if temp_score > alpha:
					alpha = temp_score
					move = new_move
				if alpha >= beta:
					break
			elif player == 1:
				if temp_score < beta:
					beta = temp_score
					move = new_move
				if alpha >= beta:
					break

			# Remove this move and try the next
			final_move_list.remove(new_move)

		# Determine score based on final player
		score = alpha if player == -1 else beta

		return score, move