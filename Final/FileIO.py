# CS 4341 Project 2
# Last updated: 9/26/2017
# Chad Underhill, Daniel Kim, Spyridon Antonatos
#
# Usage:
#       Contains methods for reading the move_file, writing to the move_file,
#       and checking for the end_game file.
#       This file also contains a Move class to help pass moves between methods
import os
import logging
import glob

# Class for creating moves to pass between methods


class Move(object):
    # Constructor
    def __init__(self, team_name, x_loc, y_loc):
        self.team_name = team_name
        self.x = x_loc
        self.y = y_loc

    # void -> string:
    # @return - string form of the move to write to the move_sfile
    def __str__(self):
        return "%s %s %s" % (self.team_name, self.x, self.y)

# void -> Move:
# @return - Move read from move_file


def readMoveFile(move_file="move_file"):

    # Open move_file and read line in file
    with open(move_file) as move_fid:
        line = move_fid.readline()

    # Check for empty file
    if line is None:
        # Make first move in the center of the board
        return Move("AgentSmith", "H", 8)

    # Split the line read from the file
    line_parts = line.split()
    team_name = line_parts[0]
    move_x = line_parts[1]
    move_y = int(line_parts[2], 10)

    # Create a move and return it
    move = Move(team_name, move_x, move_y)
    return move

# Move -> float:
# @return - Timestamp of when move_file was last updated (after this method)


def writeMoveFile(move, move_file="move_file"):

    # Open move_file and overwrite the file with the given move
    with open(move_file, 'w') as move_fid:
        move_text = str(move)
        #logging.debug("Writing move text \"%s\" to %s" % (move_text, move_file))
        move_fid.write(move_text)
        move_fid.write("\n")
        move_fid.flush()

    return os.stat(move_file).st_mtime

# void -> Boolean:
# @return - True if the end_game file was found, False otherwise


def checkEndGameFile(end_game="end_game"):

    # List of files in current directory matching specified string
    end_game_list = glob.glob("end_game")

    # Check list of matched files
    if(len(end_game_list) == 0):
        return False
    else:
        return True
