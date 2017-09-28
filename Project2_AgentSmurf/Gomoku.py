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
            if move == "first":
                board.make_move("h","8")
                best_first_move = Move(groupname, "h", "8")
                writeMoveFile(best_first_move)
                continue
            elif turn == 2 and move.x == "h" and move.y == "8":
                board.make_move("h", "8")
                board.make_move("h","8",second_move = True)
                best_second_move = Move(groupname, "h", "8")
                writeMoveFile(best_second_move)
                turn += 1
                continue
            else:
                # Store opponent's move
                board.make_move(move.x, move.y)
            # Make our move
            best_state = minimaxABPruning(board)
            best_move_tuple = best_state.get_last_move()
            best_state_move = Move(groupname, best_move_tuple[0], best_move_tuple[1])
            best_move2 =  board.make_move(best_state_move.x,best_state_move.y)
            best_state_move = Move(groupname, best_move2[0], best_move2[1])
        # Overwrite to the move file
        writeMoveFile(best_state_move)
        # Repeat


def pollForTurn(team_go=(groupname + ".go")):
    go_files = glob.glob("../*.go")
    prev_mod_time = 0
    print(go_files)
    while(not checkEndGameFile()):
        go_files = glob.glob("../*.go")
        if len(go_files) >= 1 and os.path.basename(go_files[0]) == team_go:
            if os.stat(go_files[0]).st_mtime != prev_mod_time:
                prev_mod_time = os.stat(go_files[0]).st_mtime
                return readMoveFile()
    return None

if __name__ == "__main__":
	main()
