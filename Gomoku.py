# Main file for our project 2 program
# Gomoku.py

# For polling .go file
import glob
import os
# Testing
import time

team_name = "AgentSmith"

def main():
    # Have our Agent class do all of the following:
    
    # Poll for the .go file with our groupname
    # Read the move file
    # Store the move
    # Make a move - only different thing (call ab pruning, then make our move)
    # Overwrite to the move file
    # Repeat
    pass


def pollForTurn(team_go=(team_name + ".go")):
    testTime = time.time()
    remOpp = False
    print(testTime)
    go_files = glob.glob("*.go")
    while(len(go_files) == 1):
        go_files = glob.glob("*.go")
        # TESTING
        currTime = time.time()
        if currTime - testTime > 3 and not remOpp:
            print(currTime)
            os.remove("Opponent.go")
            print("Removed")
            open(team_go, 'w')
            print("Added")
            remOpp = True
        # END TESTING
        if os.path.basename(go_files[0]) == team_go:
            # Make a move using minimax, ab pruning, eval function
            print("Move")
            break
    return "move" # Return move made for storing
