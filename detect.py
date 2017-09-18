#developped by spiros antonatos

from ReadMove_ import *


def main():
    #groupname = input("What is the name of this player?: ")
    our_groupname = "ourgroup"
    opp_groupname = "opponent"
    filename = our_groupname + ".go"
    while(True):
        try:
            group_file = open(filename,"r+")
            mv_file = open("move_file.txt","r+")
            moveline = mv_file.readline()
            read_move(moveline,opp_groupname)
            mv_file.close()
        except OSError as e:
            print("file not found")
            print(e)


if __name__ == '__main__':
  main()
