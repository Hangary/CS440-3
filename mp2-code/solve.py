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

    return recursion(board, pents)
            
def recursion(board, pents, solution = None):
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
    
    for coor in sorted(cor_dict, key=lambda coor: len(cor_dict[coor]), reverse=True):
        pents_list = cor_dict[coor]
        for pent in sorted(pents_list, key=lambda pent: len(pent_dict[get_pent_idx(pent)], reverse=False)):
            p_idx = get_pent_idx(pent)
            new_board = board.copy()
            new_pents = pent.copy()
            add_pentomino(new_board, pent, coor, check_pent=True, valid_pents=new_pents)

            result = solution.copy()
            result.append((pent, coor))

            if len(new_pents) == 1:
                return result
            
            for i in range(len(new_pents)): #remove added pentomino from pents
                if get_pent_idx(new_pents[i]) == p_idx:
                    new_pents.pop(pents[i])
                    break
            
            return recursion(new_board, new_pents, solution = result)
            
def add_pentomino(board, pent, coord, check_pent=False, valid_pents=None):
    """
    Adds a pentomino pent to the board. The pentomino will be placed such that
    coord[0] is the lowest row index of the pent and coord[1] is the lowest 
    column index. 
    
    check_pent will also check if the pentomino is part of the valid pentominos.
    """
    if check_pent and not is_pentomino(pent, valid_pents):
        return False
    for row in range(pent.shape[0]):
        for col in range(pent.shape[1]):
            if pent[row][col] != 0:
                if board[coord[0]+row][coord[1]+col] != 0: # Overlap
                    return False
                else:
                    board[coord[0]+row][coord[1]+col] = pent[row][col]
    return True

def is_pentomino(pent, pents):
    """
    Checks if a pentomino pent is part of pents
    """
    pidx = get_pent_idx(pent)
    if pidx == -1:
        return False
    true_pent = pents[pidx]
    
    for flipnum in range(3):
        p = np.copy(pent)
        if flipnum > 0:
            p = np.flip(pent, flipnum-1)
        for rot_num in range(4):
            if np.array_equal(true_pent, p):
                return True
            p = np.rot90(p)
    return False

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

