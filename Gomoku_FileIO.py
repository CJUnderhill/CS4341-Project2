import os
import logging
from Gomoku_Board import *

def readMoveFile(move_file="move_file"):
    with open(move_file) as move_fid:
        line = move_fid.readline()
    if line is None:
        logging.error("Move file empty!")

    logging.debug("Read from %s: \"%s\"" % (move_file, line))

    line_parts = line.split()
    team_name = line_parts[0]
    move_x = line_parts[1]
    move_y = int(line_parts[2], 10)

    move = Move(team_name, move_x, move_y)
    
    return move

def writeMoveFile(move, move_file="move_file"):
    with open(move_file, 'w') as move_fid:
        move_text = str(move)
        logging.debug("Writing move text \"%s\" to %s" % (move_text, move_file))
        move_fid.write(move_text)
        move_fid.write("\n")
        move_fid.flush()
    return os.stat(move_file_name).st_mtime
