# -*- coding: utf-8 -*-
import numpy as np

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

    pent_dict = dict()
    cor_dict = dict()

    for y in range(board.shape[0]):
        for x in range(board.shape[1]):
            coordinate = (y,x)
            if board[y][x] == 1:
                for pent in pents:
                    idx = get_pent_idx(pent)
                    rot_flip_list = generate_ori(pent)
                    for ori_pent in rot_flip_list:
                        if check_placement(board, ori_pent, coordinate):
                            if idx not in pent_dict.keys(): # add coordinate to pent_coor list
                                pent_dict[idx] = [coordinate]
                            else:
                                if coordinate not in pent_dict[idx]:
                                    pent_dict[idx].append(coordinate)
                            
                            if coordinate not in cor_dict.keys(): # add pents to coor_pent list
                                cor_dict[coordinate] = [ori_pent]
                            else:
                                cor_dict[coordinate].append(ori_pent)


def get_pent_idx(pent):
    """
    Returns the index of a pentomino.
    """
    pidx = 0
    for i in range(pent.shape[0]):
        for j in range(pent.shape[1]):
            if pent[i][j] != 0:
                pidx = pent[i][j]
                break
        if pidx != 0:
            break
    if pidx == 0:
        return -1
    return pidx - 1

def generate_ori(pent):
    l = []
    for i in range(4):
        rot_pent = np.rot90(pent, i)
        flip_pent = np.flip(rot_pent)
        if rot_pent not in l:
            l.append(rot_pent)
        if flip_pent not in l:
            l.append(flip_pent)
    # l = [pent]
    # l.append(np.rot90(pent, 1))
    # l.append(np.rot90(pent, 2))
    # l.append(np.rot90(pent, 3))
    # flip = np.flip(pent)
    # l.append(flip)
    # l.append(np.rot90(flip, 1))
    # l.append(np.rot90(flip, 2))
    # l.append(np.rot90(flip, 3))
    return l

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

