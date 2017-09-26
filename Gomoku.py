# CS 4341 Project 2
# Last updated: 9/26/2017
# Chad Underhill, Daniel Kim, Spyridon Antonatos
# Main file for our project 2 program
# Gomoku.py

# For polling .go file
import glob
import os
import time
import Board
import abPruning
import FileIO

# Team name
groupname = "AgentSmith"


def main():
    # Have our Agent class do all of the following:

    # Poll for the .go file with our groupname
    move = pollForTurn()
    if (move == None):
        # End game
        return
    else:
        # Store & make move
        Board.makeMove(move)
        best_state = abPruning(currentBoard)
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
