from Board import *


class Agent:
    def __init__(self, name, color):
        self.name = name
        self.board = Board()
        if color in ["white", "black"]:
            self.color = color
            if self.color == "white":
                self.o_color = "black"
            else:
                self.o_color = "white"
        else:
            print("invalid color, expected white/black")
            # Note from Chad: Init should never be used to return anything!
            #return False
        print("create new agent; color: ", color, ",name: ", name)

    def read_move(self, moveline, groupname):
        if moveline == "":
            print("make first move")
            # time.sleep(7)
        else:
            # time.sleep(7)
            string_parts = moveline.split(" ")
            if len(string_parts) == 3:
                groupname_move = string_parts[0]
                if groupname_move.strip() == groupname.strip():
                    column = string_parts[1].strip()
                    row = string_parts[2].strip()
                    print("opponent's move: ", "column: ", column, "row: ", row)

                    self.fill_board(column, row)
                else:
                    print(
                        "expected oppopnent's move, found the move of this group: ", groupname_move)
                    # put_in_tree(row,colum)
            else:
                print("invalid move line expected 3 parts, found: ",
                      len(string_parts))

    def fill_board(self, column, row):
        self.board.make_move(column, row, self.o_color)

    def play(self):
        # calculate next move based on tree
        print("")
