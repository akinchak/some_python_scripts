# BASIC
# board start view 
print('''
         1 | 2 | 3
         ---------
         4 | 5 | 6
         ---------
         7 | 8 | 9
                  ''')
# values
O = 'O'   # computer move
X = 'X'   # human move
winner = None
empty = ' '
b = [empty for i in range(9)]
b_num = [i for i in range(9)]

# winner variants
winner_board = ((0, 1, 2),
                (3, 4, 5),
                (6, 7, 8),
                (0, 3, 6),
                (1, 4, 7),
                (2, 5, 8),
                (0, 4, 8),
                (2, 4, 6))

# FUNCTIONS
# all starting board values are empty
def board():
    print('\n\t', b[0], '|', b[1], '|', b[2])
    print('\t', '---------')
    print('\t', b[3], '|', b[4], '|', b[5])
    print('\t', '---------')
    print('\t', b[6], '|', b[7], '|', b[8])

# choose your number
def human_number():
    num = int(input("\nNumber: "))
    while num not in range(1, 10) or b[num-1] != empty:
        num = int(input("Choose CORRECT Number: "))
    b[num-1] = X

# computer choose it number    
def comp_number(a):
    for row in winner_board:
        test = [b[row[0]], b[row[1]], b[row[2]]]
        if test.count(a) == 2 and test.count(empty) == 1:
            for i in range(3):
                if b[row[i]] == empty:
                    b[row[i]] = O
            return True            

# if computer have First move or "comp_number" function return None
def first_comp_number():
    import random
    b_num_best = [0, 2, 6, 8, 1, 3, 5, 7, 4]
    b_num_angles = b_num_best[:4]
    random.shuffle(b_num_angles)
    b_num_angles += b_num_best[4:]
    for i in b_num_angles:
        if b[i] == empty:
            b[i] = O
            break        
              
# winner
def winner():
    for row in winner_board:
        if b[row[0]] == b[row[1]] == b[row[2]] != empty:
            if b[row[0]] == X:
                board()
                print("\nHUMAN WIN!")
            else:
                board()
                print("\nCOMP WIN!")
            return True            

# MAIN
# choose your move priority
first_or_second = int(input('Choose your move: First (choose "1") or Second (choose "2") ? '))
while first_or_second not in (1, 2):
        first_or_second = int(input("Choose CORRECT Number: "))

# start play
if first_or_second == 1:
    pass
else:
    first_comp_number()
    board()
    
while empty in b and not winner():
    human_number()
    if winner():        
        break
    if comp_number(O) or comp_number(X) or first_comp_number():        
        pass
    if winner():
        break
    else:
        board()
    
# "if tie" control
if empty not in b and not winner():
    print("\nTIE !!!")
                    
input()
