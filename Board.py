from collections import OrderedDict

class Board:
    def __init__(self):
        self.rows_pos = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"]
        self.columns_pos = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O"]
        self.board = OrderedDict()
        for i in self.columns_pos:
            for j in self.rows_pos:
                new_board_cell = Board_Cell(i,j)
                self.board[i+j] = new_board_cell
    def make_move(self,column_pos,row_pos,color,second_move = False):
        self.board[column_pos + row_pos].play_on_cell(Checker(color),second_move = second_move)
    def check_cell(self,column_pos,row_pos):
        return self.board[column_pos + row_pos].cell_status()
    def print_board(self):
        for key,value in self.board.items():
            print(key,value.color)


                


class Board_Cell:
    def __init__(self,column,row):
        if self.check_valid(column,row):
            self.column = column
            self.row = row
            self.is_empty = True
            self.color = "empty"
        else:
            print("invalid input(s), leaving constructor")

    def play_on_cell(self,checker,second_move = False):
        if isinstance(checker,Checker):
            if self.is_empty:
                self.is_empty = False
                self.checker = checker
                self.color = self.checker.color
                print("played on this cell: ",self.column + self.row)
            elif (not self.is_empty) and second_move == True:
                print("second move of the game, overwrites the move of the first player")
                self.is_empty = False
                self.checker = checker
                self.color = self.checker.color
            else:
                print("cannot play on this cell, it is occupied by color: ",self.color)
                
    def cell_status(self):
        if self.is_empty:
            print("cell is empty")
            return "empty"
        else:
            print("cell is occupied by one checker of color: ",self.checker.color)
            return self.checker.color
            
    def check_valid(self,column,row):
        if isinstance(column,str) and isinstance(row,str):
            if is_integer(row):
                row1 = int(row)
                if row1 <=15 and row1 >=1 and (column in ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O"]):
                    #print("valid cell position")
                    return True
                else:
                    print("expecting an numeric string(integer) from 1 to 15 and a string-letter from A to O")
                    return False                
            else:
                print("error, expects numeric string as row")
                return False 
        else:
            print("error, constructor expects 2 strings")
            return False

class Checker:
    def __init__(self,color):
        if self.check_valid(color):
            self.color = color
        else:
            print("error, invalid input color")
            
    def return_color(self):
        #print(self.color)
        return color
    
    def check_valid(self,color_in):
        if color_in in ["white","black"]:
            return True
        else:
            print("invalid color, expecting white/black")
            return False
            

        




def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        pass
        
        


        
