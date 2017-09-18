from Board import *

class Tree:
    def __init__(self,board,color):
        self.initial_board = board
        self.our_color = color
        if color == "white":
            self.o_color = "black"
        else:
            self.o_color = "white"
        self.root = Node(board,self.our_color)
    def develop_tree(self):
        self.root.calculate_possible_children()
    def calculate_move(self):
        print("")






class Node:
    def __init__(self,board,color):
        self.board = board
        self.children = []
        self.value = -1
        if color == "white":
            self.o_color = "black"
        else:
            self.o_color = "white"
        self.color = color
        
    def add_child(self,another_node, dev = False):
        if (another_node.color != self.color) and dev == False:
            self.children.append(another_node)
        elif (another_node.color != self.color) and dev == True:
            self.children.append(another_node)
            self.children[-1].calculate_possible_children()
        else:
            print("cant add child with the same color")
            
    def calculate_possible_children(self):
        child_board = self.board.copy()
        keys = []
        end = False
        for key,value in self.board:
            if value.color == "empty" and (key not in keys):
                keys.append(key)
                child_board.board[key] = value
                new_child = Node(child_board,self.o_color)
                self.add_child(new_child,True)
                
        




 


        
