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
groupname = "AgentSmith"


def main():
    # Have our Agent class do all of the following:
    board = Board.Board("white")

    # Poll for the .go file with our groupname
    move = pollForTurn()
    if move is None:
        # End game
        return
    else:
        # Store & make move
        board.make_move(move.x, move.y, board.our_color)
        best_state = minimaxABPruning(board)

    # Overwrite to the move file
    writeMoveFile(best_state_move)

    # Repeat
    main()


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
