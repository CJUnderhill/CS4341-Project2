from Board import *

'''
class Tree:
    def __init__(self, board, color):
        self.initial_board = board
        self.our_color = color
        if color == "white":
            self.o_color = "black"
        else:
            self.o_color = "white"
        self.root = Node(board, self.our_color)

    def develop_tree(self):
        self.root.calculate_possible_children()

    def calculate_move(self):
        print("")
'''
#d= 0
class Node:
    def __init__(self, board, color):
        self.board = board
        self.children = []
        self.value = -1
        if color == "white":
            self.o_color = "black"
        else:
            self.o_color = "white"
        self.color = color

    def add_child(self, another_node, dev=False):
        if (another_node.color != self.color) and dev == False:
            self.children.append(another_node)
        elif (another_node.color != self.color) and dev == True:
            self.children.append(another_node)
            self.children[-1].calculate_possible_children()
            self.children[-1].board.board_status()
        else:
            print("cant add child with the same color")

    def calculate_possible_children(self):
        child_board = self.board.copy()
        keys = []
        end = False
        c = 0
        for key, value in self.board.board.items():
            #print(value)
            if value.color == "empty" and (key not in keys):
                c+=1
                keys.append(key)
                child_board.make_move(key[0],key[1:],self.o_color)
                new_child = Node(child_board, self.o_color)
                self.add_child(new_child, True)
                print()
        if(c != 0):
            #d+=1
            print("board is full",d)

b1 = Board()
b1.make_move("A","5","white")
#b1.print_board()
n1 = Node(b1,"white")
n1.calculate_possible_children()
