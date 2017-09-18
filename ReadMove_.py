#developped by spiros antonatos

def read_move(moveline,groupname):
    if moveline == "":
        print("make first move")
        #time.sleep(7)
    else:
        #time.sleep(7)
        string_parts = moveline.split(" ")
        if len(string_parts) == 3:
            groupname_move = string_parts[0]
            if groupname_move.strip() == groupname.strip():
                column = string_parts[1]
                row = string_parts[2]
                print("opponent's move: ","column: ",column,"row: ",row)
            else:
                print("expected oppopnent's move, found the move of this group: ",groupname_move)
                #put_in_tree(row,colum)
        else:
            print("invalid move line expected 3 parts, found: ",len(string_parts))




        
    
    
            
    
