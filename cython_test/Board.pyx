#!python
#cython: language_level=3, boundscheck=False
from collections import OrderedDict
import time
#import math

class Board:
    def __init__(self,our_color):
        self.rows_pos = ["1", "2", "3", "4", "5", "6", "7",
                         "8", "9", "10", "11", "12", "13", "14", "15"]
        self.columns_pos = ["A", "B", "C", "D", "E", "F",
                            "G", "H", "I", "J", "K", "L", "M", "N", "O"]
        self.board = OrderedDict()
        self.width = 15
        self.height = 15
        self.color_turn = "white"
        self.color_next_turn = "black"
        self.our_color = our_color

        self.number_total_cells = self.width*self.height
        self.number_empty_cells = self.width*self.height
        self.number_filled_cells = 0
        self.number_black_moves = 0
        self.number_white_moves = 0
        self.connect = 5
        self.length_to_win = 5
        self.turns = 0
        for i in self.columns_pos:
            for j in self.rows_pos:
                new_board_cell = Board_Cell(i, j)
                self.board[i + j] = new_board_cell

    def make_move(self, column_pos, row_pos, color = "sample",second_move=False):
        #print("making move")
        #self.board_status()
        if color == "sample":   
            color = self.color_turn
        if color in ["white","black"]:
            if color == "white" and self.color_turn == "white":
                self.number_white_moves+=1
                #self.color_turn = "black"
            elif color == "black" and self.color_turn == "black":
                self.number_black_moves+=1
                #self.color_turn = "white"
            else:
                #print("normally not this color's turn ")
                if color == "white":
                    self.number_white_moves+=1
                else:
                    self.number_black_moves+=1
                #return
        else:
            print("invalid color")
        a = self.board[column_pos + row_pos].play_on_cell(color, second_move1=second_move)
        if a != 1:
            self.number_filled_cells+=1
            self.number_empty_cells-=1
        self.color_turn , self.color_next_turn = self.color_next_turn, self.color_turn 
        #self.print_board()
        self.turns+=1
        t = self.check_terminal_move(self.columns_pos.index(column_pos)+1,self.rows_pos.index(row_pos)+1)
        #print("t:",t)
        return t
        #self.board_status()
        #print("end making move")
 

    def get_children(self):
        children = []
        for key, value in self.board.items():
            if value.color == "empty":
                child_board = self.copy()
                child_board.make_move(key[0],key[1:])
                children.append(child_board)
        return children


    def check_cell(self, column_pos, row_pos):
        return self.board[column_pos + row_pos].cell_status()
    def cell_exists(self,column_index,row_index):
        if 1 <= column_index <=15 and 1<= row_index <= 15:
            return True
        else:
            return False
    def get_cell(self,column_index,row_index):
        if self.cell_exists(column_index,row_index):
            return self.board[self.columns_pos[column_index-1]+self.rows_pos[row_index-1]]
        else:
            print("requested cell doesn't exist, boundaries out of board")
            return

    def get_filled_coordinates(self):
        coords = []
        for i in self.columns_pos:
            for j in self.rows_pos:
                color = self.board[i + j].color
                if color != "empty":
                    x = self.columns_pos.index(i)
                    y = self.rows_pos.index(j)
                    a = (x+1,y+1)
                    coords.append(a)
        return coords

    def is_full(self):
        if self.number_filled_cells >= self.number_total_cells:
            return True
        else:
            return False


    def check_terminal_state(self):

        #board = self.board
        for x in range(1,self.width+1):
            for y in range(1,self.height+1):
                win = False
                if self.get_cell(x,y).color != "empty":
                    this_color = self.get_cell(x,y).color
                    #print("here")
                    # Are these boundaries computed right??
                    x_fits_on_board = ( x + self.length_to_win < self.width )
                    y_fits_on_board = ( y + self.length_to_win < self.height )
                    diagf_fits_on_board = ( x + self.length_to_win < self.width ) and ( y + self.length_to_win < self.height )
                    diagb_fits_on_board = ( x + self.length_to_win < self.width ) and ( y - self.length_to_win > 0 )

                    # Generate lists of pieces on board
                    c = 0
                    if x_fits_on_board:
                        x_set = list(set([self.get_cell(x + delta,y) for delta in range(self.length_to_win)]))
                        win = True
                        for i in range(len(x_set)):
                            #print("i: ",x_set[i].color)
                            if this_color != x_set[i].color:
                                win = False
                    if win:
                        if this_color == self.our_color:
                            return 100
                        else:
                            return -100


                    if y_fits_on_board:
                        y_set = list(set([self.get_cell(x,y + delta) for delta in range(self.length_to_win)]))
                        win = True
                        for i in range(len(y_set)):
                            #print("i: ",y_set[i].color)
                            if this_color != y_set[i].color:
                                win = False
                    if win:
                        if this_color == self.our_color:
                            return 100
                        else:
                            return -100

                    if diagf_fits_on_board:
                        diagf_set = list(set([self.get_cell(x + delta,y + delta) for delta in range(self.length_to_win)]))
                        win = True
                        for i in range(len(diagf_set)):
                            #print("i: ",diagf_set[i].color)
                            if this_color != diagf_set[i].color:
                                win = False
                    if win:
                        if this_color == self.our_color:
                            return 100
                        else:
                            return -100



                    if diagb_fits_on_board:
                        diagb_set = list(set([self.get_cell(x + delta,y - delta) for delta in range(self.length_to_win)]))
                        win = True
                        for i in range(len(diagb_set)):
                            #print("i: ",diagb_set[i].color)
                            if this_color != diagb_set[i].color:
                                win = False
                    if win:
                        if this_color == self.our_color:
                            return 100
                        else:
                            return -100
                    #print("win: ",win)

        if self.is_full():
            print("board is full")
            return "tie"

        return False

    def check_terminal_move(self,column_index,row_index):
        x = column_index
        y = row_index
        this_color = self.get_cell(x,y).color
        #print("checking for x,y: ",x,y)

        #x_fits_on_board = ( x + self.length_to_win < self.width )
        #y_fits_on_board = ( y + self.length_to_win < self.height )
        #diagf_fits_on_board = ( x + self.length_to_win < self.width ) and ( y + self.length_to_win < self.height )
        #diagb_fits_on_board = ( x + self.length_to_win < self.width ) and ( y - self.length_to_win > 0 )

        # Generate lists of pieces on board
        win = False
        #if x_fits_on_board:
        xlow = x - 4
        xhigh = x + 4
        if xlow < 1:
            xlow = 1
        if xhigh > 15:
            xhigh = 15
        #x_set = list(set([self.get_cell(x + delta,y) for delta in range(xlow-x,xhigh+1-x)]))
        x_set = []
        for i in range(xlow,xhigh+1):
            x_set.append(self.get_cell(i,y))
        win = True
        c1 = 0
        for i in range(len(x_set)):
            #print("column i: ",x_set[i].color)
            c1+=1
            if this_color != x_set[i].color:
                c1 = 0
                win = False
            if c1 >= 5:
                if this_color == self.our_color:
                    return 100
                else:
                    return -100

        ylow = y - 4
        yhigh = y + 4
        if ylow < 1:
            ylow = 1
        if yhigh > 15:
            yhigh = 15
        #if y_fits_on_board:
        #y_set = list(set([self.get_cell(x,y + delta) for delta in range(ylow-y,yhigh+1-y)]))
        y_set = []
        for j in range(ylow,yhigh+1):
            y_set.append(self.get_cell(x,j))
        win = True
        c2 = 0
        for i in range(len(y_set)):
            #print("row i: ",y_set[i].color)
            c2+=1
            if this_color != y_set[i].color:
                c2 = 0
                win = False
            if c2 >=5:
                if this_color == self.our_color:
                    return 100
                else:
                    return -100

        #if diagf_fits_on_board:
        diag1xlow = x - (min(x,y)-1)
        diag1ylow = y - (min(x,y)-1)
        diag1xhigh = x + min(15-max(x,y),4)
        diag1yhigh = y + min(15-max(x,y),4)
        #print(diag1xlow,diag1ylow,diag1xhigh,diag1yhigh)
        ##diag1high = min(xhigh,yhigh)
        #diag1r1 = min(x,y)
        #print(diag1low,diag1high,diag1r1)
        diagf_set = []
        c3 = 0
        #print("ylistb: ",list(range(diag1ylow,diag1yhigh+1)))
        #print("xlistb: ",list(range(diag1xlow,diag1xhigh+1)))
        for i in range(len(range(diag1xlow,diag1xhigh+1))):
            diagf_set.append(self.get_cell(list(range(diag1xlow,diag1xhigh+1))[i],list(range(diag1ylow,diag1yhigh+1))[i]))
        #diagf_set = list(set([self.get_cell(x + delta,y + delta) for delta in range(diag1low-diag1r1,diag1high+1-diag1r1)]))
        win = True
        for i in range(len(diagf_set)):
            #print("diagf i: ",diagf_set[i].color)
            c3+=1
            if this_color != diagf_set[i].color:
                c3 = 0
                win = False
            if c3 >=5:
                if this_color == self.our_color:
                    return 100
                else:
                    return -100



        #if diagb_fits_on_board:
        diag2xlow = x - min(15-y,x-1)
        diag2ylow = y - min(15-x,y-1)
        diag2xhigh = x + min(y-1,15-x)
        diag2yhigh = y + min(x-1,15-y)
        #diagb_set = list(set([self.get_cell(x + delta,y - delta) for delta in range(diag1low-diag1r1,diag1high+1-diag1r1)]))
        diagb_set = []
        c4 = 0
        ylist = list(range(diag2ylow,diag2yhigh+1))
        ylist.reverse()
        #print("ylistb: ",ylist)
        #print("xlistb: ",list(range(xlow,xhigh+1)))
        #for i in range(xlow,xhigh+1),ylist:
        for i in range(len(range(diag2xlow,diag2xhigh+1))):
            diagb_set.append(self.get_cell(list(range(diag2xlow,diag2xhigh+1))[i],ylist[i]))
        win = True
        for i in range(len(diagb_set)):
            #print("diagb i: ",diagb_set[i].color)
            c4+=1
            if this_color != diagb_set[i].color:
                c4 = 0
                win = False
            if c4>=5:
                if this_color == self.our_color:
                    return 100
                else:
                    return -100

        if self.is_full():
            return "tie"
        return False

    def print_board(self):
        for i in ["   "] + self.columns_pos:
            print(i,end=" ")
        print("")
        for j in self.rows_pos:
            if int(j) < 10:
                end1 = "  "
            else:
                end1 = " "
            print(j,"",end=end1)
            for k in self.columns_pos:
                color = self.board[k+j].color
                if color == "white":
                    symbol = "X"
                elif color == "black":
                    symbol = "O"
                else:
                    symbol = "_"
                print(symbol + "",end = " ")
            print("")
                
        
        #for key, value in self.board.items():
        #    print(key, value.color)
    def board_status(self):
        print("number of filled cells: ",self.number_filled_cells)
        print("number of empty cells: ",self.number_empty_cells)
        print("number of white-filled cells: ",self.number_white_moves)
        print("number of black cells: ",self.number_black_moves)
        print("color of this player's turn: ",self.color_turn)


    def get_player_turn(self):
        return self.color_turn


    def copy(self):
        new_board = Board(self.our_color)
        for i in new_board.columns_pos:
            for j in new_board.rows_pos:
                new_board.board[i + j] = self.board[i + j].copy()
        new_board.number_filled_cells = self.number_filled_cells
        new_board.number_empty_cells = self.number_empty_cells
        new_board.number_filled_cells = self.number_filled_cells 
        new_board.number_black_moves = self.number_black_moves 
        new_board.number_white_moves = self.number_white_moves
        new_board.color_turn = self.color_turn
        new_board.color_next_turn = self.color_next_turn
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
            elif (not self.is_empty) and second_move1 == True:
                print("second move of the game, overwrites the move of the first player")
                self.is_empty = False
                #self.checker = checker
                self.color = color
                return 1
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

'''
b1 = Board("black")

b1.make_move("A","1","black")
b1.make_move("A","2","white")

b1.make_move("A","3","black")

b1.make_move("A","4","white")

b1.make_move("A","5","white")
b1.make_move("B","2","black")
b1.make_move("C","3","white")
b1.make_move("D","4","white")
b1.make_move("E","5","black")
b1.make_move("F","6","black")
b1.make_move("G","7","white")
b1.make_move("B","3","white")
b1.make_move("D","3","white")
b1.make_move("E","3","black")
b1.make_move("G","3","white")
b1.make_move("H","3","white")
b1.make_move("F","3","white")
b1.make_move("F","2","white")

b1.make_move("G","1","white")
b1.make_move("C","5","white")
b1.make_move("G","6","black")
b1.make_move("H","6","black")
b1.make_move("I","6","black")
b1.make_move("J","6","black")
b1.make_move("K","6","black")











b1.make_move("B","2")
b1.make_move("C","3")
b1.make_move("D","4")
b1.make_move("D","5")

b1.make_move("D","6")

b1.make_move("D","7")
b1.make_move("D","8")

b1.make_move("E","5")
b1.make_move("F","6")

b1.print_board()
start = time.time()
b1.board["A2"].color
#print(b1.check_terminal_state())
print(b1.get_filled_coordinates())
#c = b1.get_children()
#c[-1].print_board()
b1.board_status()
end = time.time()
print(end - start)
'''

