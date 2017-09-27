#!python
#cython: language_level=3, boundscheck=False

# CS 4341 Project 2
# Last updated: 9/26/2017
# Chad Underhill, Daniel Kim, Spyridon Antonatos
# Main file for our project 2 program
# Gomoku.py

# For polling .go file
import glob
import os
import Board
from abPruning import *
from FileIO import *

# Team name
groupname = "AgentSmurf"


def main():
    turn = 1
    board = None
    while (True):
        # Have our Agent class do all of the following:
        #board = Board.Board("white")
        our_color = "black"
        # Poll for the .go file with our groupname
        move = pollForTurn()
        if move == "first":
            our_color = "white"
        if move is None:
            # End game
            return
        else:
            # Store & make move
            if turn == 1:
                board = Board.Board(our_color)
                turn += 1
            if move != "first":
                # Store opponent's move
                board.make_move(move.x, move.y, board.our_color)
            # Make our move
            best_state = minimaxABPruning(board)
            best_move_tuple = best_state.get_last_move()
            best_state_move = Move(groupname, best_move_tuple[0], best_move_tuple[1])

        # Overwrite to the move file
        writeMoveFile(best_state_move)
        # Repeat


def pollForTurn(team_go=(groupname + ".go")):
    go_files = glob.glob("*.go")
    while(len(go_files) == 1):
        go_files = glob.glob("*.go")
        if os.path.basename(go_files[0]) == team_go:
            if checkEndGameFile():
                # End game
                break
            else:
                return readMoveFile()
    return None

main()
