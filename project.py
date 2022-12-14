"""
CS311 Final Project

Full Name(s): Jiayi Chen, Siyuan Niu

"""

import random
import itertools
from typing import List, Optional, Sequence, Tuple


# Problem constants
BOARD_SIZE = 9
INITIAL_BOARD = {}

for row in range(0, BOARD_SIZE):
    for col in range(0, BOARD_SIZE):
        INITIAL_BOARD[(row, col)] = 0
    

def draw_board(dic, size):
    """Helper function to draw the current board

    Args:
            dic: current board
            size: size of the bard
    """
    
    lst = list(dic.values())
    for i in range(len(lst)):
        if (i+1)% size ==0:
            print(lst[i])
        else:
            print(lst[i], end = " ")


class Gomoku:
    def __init__(self, state: dict[(int, int): int], parent: "Gomoku" = None, curr_depth=0):
        """Create Node to track particular state and associated parent and cost

        Args:

            state (dict[(int, int): int]): current distribution of stones on the board; 
                                            key as the coordinate (row, col) of the cell and value as the stone (0-empty, 1-black, 2-white);
                                            all values are initialized as 0's
            parent: parent Gomoku, None indicates the root node. Defaults to None.
            gameStatus: (int or string)  = 1 if black wins, = 2 if white wins, = 0 if a draw, otherwise "game_on"
            curr_depth: depth of the Gomoku node in the minimax tree
        """
        self.state = state  # To facilitate "hashable" make state immutable
        self.parent = parent
        self.gameStatus = "game_on" 
        self.curr_depth = curr_depth

        # Store coordinates of all black and white stones
        blacks = []
        whites = []

        for (key, value) in state.items():
            if value == 1:
                blacks.append(key)
            elif value == 2:
                whites.append(key)

        self.blacks = blacks
        self.whites = whites

    
    def is_terminal(self) -> bool:
        """Return True if game terminates"""
        
        board = self.state

        black_five = 0
        white_five = 0

        # Start with black
        # Initialize lists of the combinations of coordinates (sequences) on each direction that make black the winner
        possible_col_seqs = []
        possible_row_seqs = []
        possible_diag1_seqs = []
        possible_diag2_seqs = []

        for black in self.blacks:
            row_num = black[0]
            col_num = black[1]
            
            # Find all possible coordinates that makes black the winner
            possible_col_coordinates = []
            possible_row_coordinates = []
            possible_diag1_coordinates = []
            possible_diag2_coordinates = []

            # Coordinates in the same row or the same column
            for x in range(0, BOARD_SIZE):
                if abs(x - row_num) < 5:
                    possible_col_coordinates.append((x, col_num))
                if abs(x - col_num) < 5:
                    possible_row_coordinates.append((row_num, x))

            # Append the sequence if the coordinates make five-in-a-row or five-in-a-column
            while len(possible_col_coordinates) >= 5:
                possible_col_seqs.append(possible_col_coordinates[0:5])
                possible_col_coordinates.pop(0)
            while len(possible_row_coordinates) >= 5:
                possible_row_seqs.append(possible_row_coordinates[0:5])
                possible_row_coordinates.pop(0)


            # Diagonal 1
            # Upper-left corner coordinates
            row_index = row_num
            col_index = col_num
            while (row_index > -1) and (col_index > -1):
                if (abs(row_index - row_num) + abs(col_index - col_num)) < 5 * 2:
                    possible_diag1_coordinates.insert(0, (row_index, col_index))
                row_index -= 1
                col_index -= 1
            
            # Lower-right corner coordinates
            row_index = row_num
            col_index = col_num
            while (row_index + 1 < BOARD_SIZE) and (col_index + 1 < BOARD_SIZE):
                if (abs(row_index - row_num) + abs(col_index - col_num)) < 5 * 2:
                    possible_diag1_coordinates.append((row_index + 1, col_index + 1))
                row_index += 1
                col_index += 1
            
            # Append the sequence if the coordinates make five-in-a-diagonal
            while len(possible_diag1_coordinates) >= 5:
                possible_diag1_seqs.append(possible_diag1_coordinates[0:5])
                possible_diag1_coordinates.pop(0)

            
            # Diagonal 2
            # Upper-right corner coordinates
            row_index = row_num
            col_index = col_num
            while (row_index > -1) and (col_index < BOARD_SIZE):
                if (abs(row_index - row_num) + abs(col_index - col_num)) < 5 * 2:
                    possible_diag2_coordinates.insert(0, (row_index, col_index))
                row_index -= 1
                col_index += 1
            
            # Lower-left corner coordinates
            row_index = row_num
            col_index = col_num
            while (row_index + 1 < BOARD_SIZE) and (col_index - 1 > -1) and (col_index + 1 < BOARD_SIZE):
                if (abs(row_index - row_num) + abs(col_index - col_num)) < 5 * 2:
                    possible_diag2_coordinates.append((row_index + 1, col_index - 1))
                row_index += 1
                col_index -= 1
            
            # Append the sequence if the coordinates make five-in-a-diagonal
            while len(possible_diag2_coordinates) >= 5:
                possible_diag2_seqs.append(possible_diag2_coordinates[0:5])
                possible_diag2_coordinates.pop(0)

            
        # Remove duplicate sequences
        possible_col_seqs.sort()
        possible_col_seqs = list(possible_col_seqs for possible_col_seqs,_ in itertools.groupby(possible_col_seqs))
        possible_row_seqs.sort()
        possible_row_seqs = list(possible_row_seqs for possible_row_seqs,_ in itertools.groupby(possible_row_seqs))
        possible_diag1_seqs_set = set(tuple(x) for x in possible_diag1_seqs)
        possible_diag1_seqs = [ list(x) for x in possible_diag1_seqs_set ]
        possible_diag2_seqs_set = set(tuple(x) for x in possible_diag2_seqs)
        possible_diag2_seqs = [ list(x) for x in possible_diag2_seqs_set ]


        # Count how many 5 consecutive coordinates - sequences -  in a row, col, or diag
        for possible_col_seq in possible_col_seqs:
            num_black = 0
            for coordinate in possible_col_seq:
                if board[coordinate] == 1:
                    num_black += 1
            if num_black == 5:
                black_five += 1

        for possible_row_seq in possible_row_seqs:
            num_black = 0
            for coordinate in possible_row_seq:
                if board[coordinate] == 1:
                    num_black += 1
            if num_black == 5:
                black_five += 1
        
        for possible_diag1_seq in possible_diag1_seqs:
            num_black = 0
            for coordinate in possible_diag1_seq:
                if board[coordinate] == 1:
                    num_black += 1
            if num_black == 5:
                black_five += 1
        
        for possible_diag2_seq in possible_diag2_seqs:
            num_black = 0
            for coordinate in possible_diag2_seq:
                if board[coordinate] == 1:
                    num_black += 1
            if num_black == 5:
                black_five += 1

        

        # Repeat for white as the winner
        # I realized that there are some duplicate codes here, and I might want to clean it up in the future
        possible_col_seqs = []
        possible_row_seqs = []
        possible_diag1_seqs = []
        possible_diag2_seqs = []

        for white in self.whites:
            row_num = white[0]
            col_num = white[1]
            
            # Find all possible coordinates that makes black the winner
            possible_col_coordinates = []
            possible_row_coordinates = []
            possible_diag1_coordinates = []
            possible_diag2_coordinates = []

            # Coordinates in the same row or the same column
            for x in range(0, BOARD_SIZE):
                if abs(x - row_num) < 5:
                    possible_col_coordinates.append((x, col_num))
                if abs(x - col_num) < 5:
                    possible_row_coordinates.append((row_num, x))

            # Append the sequence if the coordinates make five-in-a-row or five-in-a-column
            while len(possible_col_coordinates) >= 5:
                possible_col_seqs.append(possible_col_coordinates[0:5])
                possible_col_coordinates.pop(0)
            while len(possible_row_coordinates) >= 5:
                possible_row_seqs.append(possible_row_coordinates[0:5])
                possible_row_coordinates.pop(0)


            # Diagonal 1
            # Upper-left corner coordinates
            row_index = row_num
            col_index = col_num
            while (row_index > -1) and (col_index > -1):
                if (abs(row_index - row_num) + abs(col_index - col_num)) < 5 * 2:
                    possible_diag1_coordinates.insert(0, (row_index, col_index))
                row_index -= 1
                col_index -= 1
            
            # Lower-right corner coordinates
            row_index = row_num
            col_index = col_num
            while (row_index + 1 < BOARD_SIZE) and (col_index + 1 < BOARD_SIZE):
                if (abs(row_index - row_num) + abs(col_index - col_num)) < 5 * 2:
                    possible_diag1_coordinates.append((row_index + 1, col_index + 1))
                row_index += 1
                col_index += 1
            
            # Append the sequence if the coordinates make five-in-a-diagonal
            while len(possible_diag1_coordinates) >= 5:
                possible_diag1_seqs.append(possible_diag1_coordinates[0:5])
                possible_diag1_coordinates.pop(0)

            
            # Diagonal 2
            # Upper-right corner coordinates
            row_index = row_num
            col_index = col_num
            while (row_index > -1) and (col_index < BOARD_SIZE):
                if (abs(row_index - row_num) + abs(col_index - col_num)) < 5 * 2:
                    possible_diag2_coordinates.insert(0, (row_index, col_index))
                row_index -= 1
                col_index += 1
            
            # Lower-left corner coordinates
            row_index = row_num
            col_index = col_num
            while (row_index + 1 < BOARD_SIZE) and (col_index - 1 > -1) and (col_index + 1 < BOARD_SIZE):
                if (abs(row_index - row_num) + abs(col_index - col_num)) < 5 * 2:
                    possible_diag2_coordinates.append((row_index + 1, col_index - 1))
                row_index += 1
                col_index -= 1
            
            # Append the sequence if the coordinates make five-in-a-diagonal
            while len(possible_diag2_coordinates) >= 5:
                possible_diag2_seqs.append(possible_diag2_coordinates[0:5])
                possible_diag2_coordinates.pop(0)
            
        # Remove duplicate sequences
        possible_col_seqs.sort()
        possible_col_seqs = list(possible_col_seqs for possible_col_seqs,_ in itertools.groupby(possible_col_seqs))
        possible_row_seqs.sort()
        possible_row_seqs = list(possible_row_seqs for possible_row_seqs,_ in itertools.groupby(possible_row_seqs))
        possible_diag1_seqs_set = set(tuple(x) for x in possible_diag1_seqs)
        possible_diag1_seqs = [ list(x) for x in possible_diag1_seqs_set ]
        possible_diag2_seqs_set = set(tuple(x) for x in possible_diag2_seqs)
        possible_diag2_seqs = [ list(x) for x in possible_diag2_seqs_set ]


        # Count how many 5 in a row, seq, or diag
        for possible_col_seq in possible_col_seqs:
            num_white = 0
            for coordinate in possible_col_seq:
                if board[coordinate] == 2:
                    num_white += 1
            if num_white == 5:
                white_five += 1

        for possible_row_seq in possible_row_seqs:
            num_white = 0
            for coordinate in possible_row_seq:
                if board[coordinate] == 2:
                    num_white += 1
            if num_white == 5:
                white_five += 1

        for possible_diag1_seq in possible_diag1_seqs:
            num_white = 0
            for coordinate in possible_diag1_seq:
                if board[coordinate] == 2:
                    num_white += 1
            if num_white == 5:
                white_five += 1
        
        for possible_diag2_seq in possible_diag2_seqs:
            num_white = 0
            for coordinate in possible_diag2_seq:
                if board[coordinate] == 2:
                    num_white += 1
            if num_white == 5:
                white_five += 1


        #if we have 5 stones of either black or white?        
        if black_five > 0:
            self.gameStatus = 1
            return True
        if white_five > 0:
            self.gameStatus = 2
            return True

        if list(board.values()).count(0) == 0:
            self.gameStatus = 0
            return True

        return False


    def get_threat_patterns(self, color: int, length: int) -> tuple([int, int]):
        """Return the numbers of open and  half open consecutive stones - threat patterns - in a tuple given a player and a pattern size.
         
         Open threat pattern: patterns without opponent stones on both sides

         Half open threat pattern: patterns with an opponent stone on either side

         The size range of a threat pattern is 2 to 4. 
    
         """
         
        board = self.state
        open = 0
        half = 0
        
        possible_col_seqs = []
        possible_row_seqs = []
        possible_diag1_seqs = []
        possible_diag2_seqs = []

        if color == 1:
            stones = self.blacks
            opponent = 2
        else:
            stones = self.whites
            opponent = 1
            
        for stone in stones:
            row_num = stone[0]
            col_num = stone[1]
            
            # Look for possible row, col, and diag sequence of 5 stones
            possible_col_coordinates = []
            possible_row_coordinates = []
            possible_diag1_coordinates = []
            possible_diag2_coordinates = []

            for x in range(0, BOARD_SIZE):
                if abs(x - row_num) < length:
                    possible_col_coordinates.append((x, col_num))
                if abs(x - col_num) < length:
                    possible_row_coordinates.append((row_num, x))
            
            while len(possible_col_coordinates) >= length:
                possible_col_seqs.append(possible_col_coordinates[0:length])
                possible_col_coordinates.pop(0)
            while len(possible_row_coordinates) >= length:
                possible_row_seqs.append(possible_row_coordinates[0:length])
                possible_row_coordinates.pop(0)


            # Diagonal 1
            # Upper-left corner coordinates
            row_index = row_num
            col_index = col_num
            while (row_index > -1) and (col_index > -1):
                if (abs(row_index - row_num) + abs(col_index - col_num)) < length * 2:
                    possible_diag1_coordinates.insert(0, (row_index, col_index))
                row_index -= 1
                col_index -= 1
            
            # Lower-right corner coordinates
            row_index = row_num
            col_index = col_num
            while (row_index + 1 < BOARD_SIZE) and (col_index + 1 < BOARD_SIZE):
                if (abs(row_index - row_num) + abs(col_index - col_num)) < length * 2:
                    possible_diag1_coordinates.append((row_index + 1, col_index + 1))
                row_index += 1
                col_index += 1
            
            # Append the sequence if the coordinates make five-in-a-diagonal
            while len(possible_diag1_coordinates) >= length:
                possible_diag1_seqs.append(possible_diag1_coordinates[0:length])
                possible_diag1_coordinates.pop(0)


            # Diagonal 2
            # Upper-right corner coordinates
            row_index = row_num
            col_index = col_num
            while (row_index > -1) and (col_index < BOARD_SIZE):
                if (abs(row_index - row_num) + abs(col_index - col_num)) < length * 2:
                    possible_diag2_coordinates.insert(0, (row_index, col_index))
                row_index -= 1
                col_index += 1
            
            # Lower-left corner coordinates
            row_index = row_num
            col_index = col_num
            while (row_index + 1 < BOARD_SIZE) and (col_index - 1 > -1) and (col_index + 1 < BOARD_SIZE):
                if (abs(row_index - row_num) + abs(col_index - col_num)) < length * 2:
                    possible_diag2_coordinates.append((row_index + 1, col_index - 1))
                row_index += 1
                col_index -= 1
            
            
            # Append the sequence if the coordinates make five-in-a-diagonal
            while len(possible_diag2_coordinates) >= length:
                possible_diag2_seqs.append(possible_diag2_coordinates[0:length])
                possible_diag2_coordinates.pop(0)

        
        # Remove duplicate sequences
        possible_col_seqs.sort()
        possible_col_seqs = list(possible_col_seqs for possible_col_seqs,_ in itertools.groupby(possible_col_seqs))
        possible_row_seqs.sort()
        possible_row_seqs = list(possible_row_seqs for possible_row_seqs,_ in itertools.groupby(possible_row_seqs))
        possible_diag1_seqs.sort()
        possible_diag1_seqs_set = set(tuple(x) for x in possible_diag1_seqs)
        possible_diag1_seqs = [ list(x) for x in possible_diag1_seqs_set ]
        possible_diag2_seqs_set = set(tuple(x) for x in possible_diag2_seqs)
        possible_diag2_seqs = [ list(x) for x in possible_diag2_seqs_set ]

        
        # Start to count
        # Col
        for possible_col_seq in possible_col_seqs:
            num_stone = 0
            for coordinate in possible_col_seq:
                if board[coordinate] == color:
                    num_stone += 1
            if num_stone == length:
                if length == 5:
                    open += 1
                else: 
                    head = possible_col_seq[0]
                    tail = possible_col_seq[-1]

                    if head[0] != 0 and tail[0] != BOARD_SIZE-1:
                        if board[(head[0]-1, head[1])] == 0 and board[(tail[0]+1, head[1])] == 0:
                            open += 1
                    
                    if head[0] == 0:
                        if board[tail[0]+1, head[1]] == 0:
                            half += 1
                    elif tail[0] == BOARD_SIZE-1:
                        if board[head[0]-1, head[1]] == 0:
                            half += 1
                    else:
                        if board[(head[0]-1, head[1])] == opponent: 
                            if board[(tail[0]+1, head[1])] == 0:
                                half += 1
                        if board[(tail[0]+1, head[1])] == opponent:
                            if board[(head[0]-1, head[1])] == 0:
                                half += 1
        
        # Row
        for possible_row_seq in possible_row_seqs:
            num_stone = 0
            for coordinate in possible_row_seq:
                if board[coordinate] == color:
                    num_stone += 1
            if num_stone == length:
                if length == 5:
                    open += 1
                else:
                    head = possible_row_seq[0]
                    tail = possible_row_seq[-1]

                    if head[1] != 0 and tail[1] != BOARD_SIZE-1:
                        if board[(head[0], head[1]-1)] == 0 and board[(head[0], tail[1]+1)] == 0:
                            open += 1
                    
                    if head[1] == 0:
                        if board[head[0], tail[1]+1] == 0:
                            half += 1
                    elif tail[1] == BOARD_SIZE-1:
                        if board[head[0], head[1]-1] == 0:
                            half += 1
                    else:
                        if board[(head[0], head[1]-1)] == opponent: 
                            if board[(head[0], tail[1]+1)] == 0:
                                half += 1

                        if board[(head[0], tail[1]+1)] == opponent:
                            if board[(head[0], head[1]-1)] == 0:
                                half += 1

        # Diag1
        for possible_diag1_seq in possible_diag1_seqs:
            num_stone = 0
            for coordinate in possible_diag1_seq:
                if board[coordinate] == color:
                    num_stone += 1
            if num_stone == length:
                if length == 5:
                    open += 1
                else:
                    head = possible_diag1_seq[0]
                    tail = possible_diag1_seq[-1]

                    if head[0] != 0 and head[1] != 0 and tail[0] != BOARD_SIZE-1 and tail[1] != BOARD_SIZE-1:
                        if board[(head[0]-1, head[1]-1)] == 0 and board[(tail[0]+1, tail[1]+1)] == 0:
                            open += 1

                    if (head[0] == 0 or head[1] == 0) and (tail[0] != BOARD_SIZE-1 and tail[1] != BOARD_SIZE-1):
                        if board[tail[0]+1, tail[1]+1] == 0:
                            half += 1
                    elif (tail[0] == BOARD_SIZE-1 or tail[1] == BOARD_SIZE-1) and (head[0] != 0 and head[1] != 0):
                        if board[head[0]-1, head[1]-1] == 0:
                            half += 1
                    else:
                        if head[0] != 0 and head[1] != 0 and tail[0] != BOARD_SIZE-1 and tail[1] != BOARD_SIZE-1:
                            if board[(head[0]-1, head[1]-1)] == opponent: 
                                if board[(tail[0]+1, tail[1]+1)] == 0:
                                    half += 1
                            if board[(tail[0]+1, tail[1]+1)] == opponent:
                                if board[(head[0]-1, head[1]-1)] == 0:
                                    half += 1
                    
        # Diag2
        for possible_diag2_seq in possible_diag2_seqs:
            num_stone = 0
            for coordinate in possible_diag2_seq:
                if board[coordinate] == color:
                    num_stone += 1
            if num_stone == length:
                if length == 5:
                    open += 1
                else:
                    head = possible_diag2_seq[0]
                    tail = possible_diag2_seq[-1]

                    if head[0] != 0 and head[1] != BOARD_SIZE-1 and tail[0] != BOARD_SIZE-1 and tail[1] != 0:
                        if board[(head[0]-1, head[1]+1)] == 0 and board[(tail[0]+1, tail[1]-1)] == 0:
                            open += 1

                    if (head[0] == 0 or head[1] == BOARD_SIZE-1) and (tail[0] != BOARD_SIZE-1 and tail[1] != 0):
                        if board[tail[0]+1, tail[1]-1] == 0:
                            half += 1
                            
                    elif (tail[0] == BOARD_SIZE-1 or tail[1] == 0) and (head[0] != 0 and head[1] != BOARD_SIZE-1):
                        if board[head[0]-1, head[1]+1] == 0:
                            half += 1
                            
                    else:
                        if head[0] != 0 and head[1] != BOARD_SIZE-1 and tail[0] != BOARD_SIZE-1 and tail[1] != 0:
                            if board[(head[0]-1, head[1]+1)] == opponent: 
                                if board[(tail[0]+1, tail[1]-1)] == 0:
                                    half += 1
                                    
                            if board[(tail[0]+1, tail[1]-1)] == opponent:
                                if board[(head[0]-1, head[1]+1)] == 0:
                                    half += 1
                                
        return open, half
    

    def get_possible_moves(self) -> List["Gomoku"]:
        """Find the neighbors of all filled cells as all next possible moves,
            return a list of child Gomoku objects with each neighbor filled
        """
        lst = []
        filled = [x for x in self.state if self.state[x] > 0]

        move_coordinates = set()
        
        for (row, col) in filled:
            neighbors = [
                (row + 1, col),
                (row - 1, col),
                (row, col + 1),
                (row, col - 1),
                (row + 1, col - 1),
                (row - 1, col + 1),
                (row + 1, col + 1),
                (row - 1, col - 1)]
                
            for n in neighbors:
                if n[0] < 0 or n[1] < 0 or n[0] > BOARD_SIZE - 1 or n[1] > BOARD_SIZE - 1 :
                    continue
                move_coordinates.add(n)

        for m in move_coordinates:
            state_copy = self.state.copy()
            
            if self.state[m] == 0:
                if len(self.blacks) > len(self.whites):
                    state_copy[m] = 2
                    lst.append(Gomoku(state_copy, self.state, curr_depth=self.curr_depth+1))
                else:
                    state_copy[m] = 1
                    lst.append(Gomoku(state_copy, self.state, curr_depth=self.curr_depth+1))
                
        return lst

    def minimax(self, maximizing: bool, depth: int) -> int:
        """Return the score of min or max depending on the perspective"""
        
        if self.is_terminal() or self.curr_depth > depth:
            # Count black patterns
            [black_open_two, black_half_two] = self.get_threat_patterns(color=1, length=2)
            [black_open_three, black_half_three] = self.get_threat_patterns(color=1, length=3)
            [black_open_four, black_half_four] = self.get_threat_patterns(color=1, length=4)
            [black_open_five, black_half_five] = self.get_threat_patterns(color=1, length=5)
            black_five = black_open_five + black_half_five

            # Count white patterns
            [white_open_two, white_half_two] = self.get_threat_patterns(color=2, length=2)
            [white_open_three, white_half_three] = self.get_threat_patterns(color=2, length=3)
            [white_open_four, white_half_four] = self.get_threat_patterns(color=2, length=4)
            [white_open_five, white_half_five] = self.get_threat_patterns(color=2, length=5)
            white_five = white_open_five + white_half_five

            five_diff = black_five - white_five
            four_open_diff = black_open_four - white_open_four
            four_half_diff = black_half_four - white_half_four
            three_open_diff = black_open_three - white_open_three
            three_half_diff = black_half_three - white_half_three
            two_open_diff = black_open_two - white_open_two
            two_half_diff = black_half_two - white_half_two

            # Compared with another evaluation function
            # return (6000 * five_diff + 
            # 4800 * four_open_diff + 500 * four_half_diff + 
            # 500 * three_open_diff + 200 * three_half_diff + 
            # 50 * two_open_diff + 10 * two_half_diff), self.state
            
            return (10000 * five_diff + 
            5000 * four_open_diff + 2500 * four_half_diff + 
            2000 * three_open_diff + 1000 * three_half_diff + 
            250 * two_open_diff + 50 * two_half_diff), self.state

        scores = []
        for board in self.get_possible_moves():
            scores.append(board.minimax(not maximizing, depth=depth))

        if maximizing:
            return max(scores, key=lambda item:item[0])
        else:
            return min(scores, key=lambda item:item[0])


    def new_minimax(self, maximizing: bool, depth: int, alpha=float('-inf'), beta=float('inf')) -> tuple([int, dict]):
        """With alpha-beta pruning, return the score of min or max depending on the perspective"""
        
        if self.is_terminal() or self.curr_depth > depth:
            # Count black patterns
            [black_open_two, black_half_two] = self.get_threat_patterns(color=1, length=2)
            [black_open_three, black_half_three] = self.get_threat_patterns(color=1, length=3)
            [black_open_four, black_half_four] = self.get_threat_patterns(color=1, length=4)
            [black_open_five, black_half_five] = self.get_threat_patterns(color=1, length=5)
            black_five = black_open_five + black_half_five

            # Count white patterns
            [white_open_two, white_half_two] = self.get_threat_patterns(color=2, length=2)
            [white_open_three, white_half_three] = self.get_threat_patterns(color=2, length=3)
            [white_open_four, white_half_four] = self.get_threat_patterns(color=2, length=4)
            [white_open_five, white_half_five] = self.get_threat_patterns(color=2, length=5)
            white_five = white_open_five + white_half_five

            five_diff = black_five - white_five
            four_open_diff = black_open_four - white_open_four
            four_half_diff = black_half_four - white_half_four
            three_open_diff = black_open_three - white_open_three
            three_half_diff = black_half_three - white_half_three
            two_open_diff = black_open_two - white_open_two
            two_half_diff = black_half_two - white_half_two
            
            return (10000 * five_diff + 
            5000 * four_open_diff + 2500 * four_half_diff + 
            2000 * three_open_diff + 1000 * three_half_diff + 
            250 * two_open_diff + 50 * two_half_diff), self.state


        if maximizing:
            bestValue = (float('-inf'), self.state)
            for board in self.get_possible_moves():
                value = (board.new_minimax(not maximizing, depth=depth, alpha=alpha, beta=beta))
                bestValue = max(bestValue, value, key=lambda item:item[0]) 
                alpha = max(alpha, bestValue[0])
                if beta <= alpha:
                    break

            return bestValue

        else:
            bestValue = (float('inf'), self.state)
            for board in self.get_possible_moves():
                value = (board.new_minimax(not maximizing, depth=depth, alpha=alpha, beta=beta))
                bestValue = min(bestValue, value, key=lambda item:item[0]) 
                beta = min(beta, bestValue[0])
                if beta <= alpha:
                    break

            return bestValue


    def best_move(self, depth) -> tuple([tuple([int, int]), int]):
        """Return the best move for black based on score calculated from minimax"""
        filled = [x for x in self.state if self.state[x] > 0]
        move_coordinates = set()
        
        for (row, col) in filled:
            neighbors = [
                (row + 1, col),
                (row - 1, col),
                (row, col + 1),
                (row, col - 1),
                (row + 1, col - 1),
                (row - 1, col + 1),
                (row + 1, col + 1),
                (row - 1, col - 1)]
                
            for n in neighbors:
                if n[0] < 0 or n[1] < 0 or n[0] > BOARD_SIZE - 1 or n[1] > BOARD_SIZE - 1 :
                    continue
                if self.state[n] == 0:
                    move_coordinates.add(n)

        bestMove = None, 0

        alpha = float('-inf')
        for m in move_coordinates:
            state_copy = self.state.copy()
            state_copy[m] = 1
            gomoku = Gomoku(state=state_copy, curr_depth=self.curr_depth+1)
            score = gomoku.new_minimax(maximizing=False, depth=depth, alpha=alpha)[0]
            if score >= bestMove[1]:
                alpha = max(alpha, score)
                bestMove = m, score
                
        return bestMove

    
    def play(self, depth) -> int:
        """Played on the current board, with black uses minimax with depth and white playing randomly"""
        if self.is_terminal():
            # draw_board(self.state, 9)
            return self.gameStatus
        
        filled = [x for x in self.state if self.state[x] > 0]
        move_coordinates = set()
        
        for (row, col) in filled:
            neighbors = [
                (row + 1, col),
                (row - 1, col),
                (row, col + 1),
                (row, col - 1),
                (row + 1, col - 1),
                (row - 1, col + 1),
                (row + 1, col + 1),
                (row - 1, col - 1)]
                
            for n in neighbors:
                if n[0] < 0 or n[1] < 0 or n[0] > BOARD_SIZE - 1 or n[1] > BOARD_SIZE - 1 :
                    continue
                if self.state[n] == 0:
                    move_coordinates.add(n)
            
            
        move_coordinates2 = list(move_coordinates)
        state_copy = self.state.copy()
        if len(self.blacks) > len(self.whites):
            coordinate = random.choice(move_coordinates2)
            state_copy[coordinate] = 2
            new_board = Gomoku(state=state_copy, curr_depth=self.curr_depth+1)
        else:
            coordinate = self.best_move(depth)[0]
            state_copy[coordinate] = 1
            new_board = Gomoku(state=state_copy, curr_depth=self.curr_depth+1)

        return new_board.play(depth)


    def play_randomly(self) -> int:
        """Played on the current board, with both black and white playing randomly"""
        if self.is_terminal():
            # draw_board(self.state, 9)
            return self.gameStatus
        
        filled = [x for x in self.state if self.state[x] > 0]
        move_coordinates = set()
        
        for (row, col) in filled:
            neighbors = [
                (row + 1, col),
                (row - 1, col),
                (row, col + 1),
                (row, col - 1),
                (row + 1, col - 1),
                (row - 1, col + 1),
                (row + 1, col + 1),
                (row - 1, col - 1)]
                
            for n in neighbors:
                if n[0] < 0 or n[1] < 0 or n[0] > BOARD_SIZE - 1 or n[1] > BOARD_SIZE - 1 :
                    continue
                if self.state[n] == 0:
                    move_coordinates.add(n)
            
            
        move_coordinates2 = list(move_coordinates)
        state_copy = self.state.copy()
        if len(self.blacks) > len(self.whites):
            coordinate = random.choice(move_coordinates2)
            state_copy[coordinate] = 2
            new_board = Gomoku(state=state_copy, curr_depth=self.curr_depth+1)
        else:
            coordinate = random.choice(move_coordinates2)
            state_copy[coordinate] = 1
            new_board = Gomoku(state=state_copy, curr_depth=self.curr_depth+1)

        return new_board.play_randomly()


if __name__ == "__main__":
    pass
