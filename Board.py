from collections import OrderedDict


class Board:
    def __init__(self):
        self.rows_pos = ["1", "2", "3", "4", "5", "6", "7",
                         "8", "9", "10", "11", "12", "13", "14", "15"]
        self.columns_pos = ["A", "B", "C", "D", "E", "F",
                            "G", "H", "I", "J", "K", "L", "M", "N", "O"]
        self.board = OrderedDict()
        self.number_empty_cells = 15*15
        self.number_filled_cells = 0
        self.number_black_moves = 0
        self.number_white_moves = 0
        self.color_turn = "white"
        for i in self.columns_pos:
            for j in self.rows_pos:
                new_board_cell = Board_Cell(i, j)
                self.board[i + j] = new_board_cell

    def make_move(self, column_pos, row_pos, color, second_move=False):
        if color == "white":
            self.number_white_moves+=1
            self.color_turn = "black"
        elif color == "black":
            self.number_black_moves+=1
            self.color_turn = "white"
        else:
            print("error unrecognized color")
            return
        self.board[column_pos +
                   row_pos].play_on_cell(color, second_move1=second_move)
        self.number_filled_cells+=1
        self.number_empty_cells-=1



    def get_children(self):
        children = []
        for key, value in self.board.items():
            if value.color == "empty":
                child_board = self.copy()
                child_board.make_move(key[0],key[1:],self.o_color)
                children.append(child_board)
        return children


    def check_cell(self, column_pos, row_pos):
        return self.board[column_pos + row_pos].cell_status()

    def print_board(self):
        for key, value in self.board.items():
            print(key, value.color)
    def board_status(self):
        print("number of filled cells: ",self.number_filled_cells)
    def get_player_turn(self):
        return self.color_turn


    def copy(self):
        new_board = Board()
        for i in new_board.columns_pos:
            for j in new_board.rows_pos:
                new_board.board[i + j] = self.board[i + j].copy()
        new_board.number_filled_cells = self.number_filled_cells
        new_board.number_empty_cells = self.number_empty_cells
        return new_board


class Board_Cell:
    def __init__(self, column, row, is_empty=True, color="empty"):
        if self.check_valid(column, row):
            self.column = column
            self.row = row
            self.is_empty = is_empty
            self.color = color
            #self.checker = checker
        else:
            print("invalid input(s), leaving constructor")

    def play_on_cell(self, color, second_move1=False):
        if isinstance(color, str):
            if self.is_empty:
                self.is_empty = False
                #self.checker = checker
                self.color = color
                #print("played on this cell: ", self.column + self.row)
            elif (not self.is_empty) and second_move == True:
                print("second move of the game, overwrites the move of the first player")
                self.is_empty = False
                #self.checker = checker
                self.color = color
            else:
                print("cannot play on this cell, it is occupied by color: ", self.color)

    def copy(self):
        new_cell = Board_Cell(self.column, self.row,
                              self.is_empty, self.color)
        return new_cell

    def cell_status(self):
        if self.is_empty:
            print("cell is empty")
            return "empty"
        else:
            print("cell is occupied by one checker of color: ", self.checker.color)
            return self.color

    def check_valid(self, column, row):
        if isinstance(column, str) and isinstance(row, str):
            if is_integer(row):
                row1 = int(row)
                if row1 <= 15 and row1 >= 1 and (column in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]):
                    #print("valid cell position")
                    return True
                else:
                    print(
                        "expecting an numeric string(integer) from 1 to 15 and a string-letter from A to O")
                    return False
            else:
                print("error, expects numeric string as row")
                return False
        else:
            print("error, constructor expects 2 strings")
            return False

'''
class Checker:
    def __init__(self, color):
        if self.check_valid(color):
            self.color = color
        else:
            print("error, invalid input color")

    def return_color(self):
        # print(self.color)
        return self.color

    def check_valid(self, color_in):
        if color_in in ["white", "black"]:
            return True
        else:
            print("invalid color, expecting white/black")
            return False

'''
def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        pass
