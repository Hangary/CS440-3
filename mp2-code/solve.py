# -*- coding: utf-8 -*-

def solve(board, pents):
    """
    This is the function you will implement. It will take in a numpy array of the board
    as well as a list of n tiles in the form of numpy arrays. The solution returned
    is of the form [(p1, (row1, col1))...(pn,  (rown, coln))]
    where pi is a tile (may be rotated or flipped), and (rowi, coli) is 
    the coordinate of the upper left corner of pi in the board (lowest row and column index 
    that the tile covers).
    
    -Use np.flip and np.rot90 to manipulate pentominos.
    
    -You can assume there will always be a solution.
    """

    initial = state(board, pents)
    stack = [initial]
    visited = dict()
    while stack:
        cur = stack.pop()
        if hash(cur) in visited.keys():
            continue
        visited[hash(cur)] = 1

        board = cur.board
        pents = cur.pents

        if (len(pents) == 0):
            return board
        
    return []

def check_placement(board, pent, coord):
    for row in range(pent.shape[0]):
        for col in range(pent.shape[1]):
            if pent[row][col] != 0:
                if coord[0]+row >= board.shape[0] or coord[1]+col >= board.shape[1]: # outside board
                    return False
                if board[coord[0]+row][coord[1]+col] != 0: # Overlap
                    return False
    return True

class state():
    def __init__(self, board, pents):
        self.board = board
        self.pents = pents

    def __hash__(self):
        self.hash = hash((self.board, self.pents))
        return self.hash
