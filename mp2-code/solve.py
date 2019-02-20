# -*- coding: utf-8 -*-
import numpy as np
from random import shuffle

def solve(board, pents, app = None):
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

    coor_remain = []

    board = np.negative(board)
    for y in range(board.shape[0]):
        for x in range(board.shape[1]):
            coordinate = (y,x)
            coor_remain.append(coordinate)
            if board[y][x] == -1:
                for pent in pents:
                    idx = get_pent_idx(pent)
                    rot_flip_list = generate_ori(pent)
                    for ori_pent, label in rot_flip_list:
                        cor_add_list =  check_placement(board, ori_pent, coordinate)
                        if cor_add_list != []:
                            if idx not in pent_dict.keys():
                                pent_dict[idx] = dict()
                            if coordinate not in pent_dict[idx].keys():
                                pent_dict[idx][coordinate] = [(ori_pent, cor_add_list)]
                            else:
                                pent_dict[idx][coordinate].append((ori_pent, cor_add_list))
                        
    pents_remain = []
    for p in pents:
        pents_remain.append(get_pent_idx(p))
    
    solution = recursion(board, pents, [], pent_dict, coor_remain, pents_remain)
    print(solution)
    return solution

def add_pent(board, pidx, cor_add_list):
    for c in cor_add_list:
        row = c[0]
        col = c[1]
        if board[row][col] != -1:
            print ("                                                       error")

        board[row][col] = (pidx + 1)
            
def recursion(board, pents, solution, pent_dict, coor_remain, pents_remain):
    cor_dict = dict()
    cor_pidx_dict = dict()
    for coordinate in coor_remain:
        cor_dict[coordinate] = []
        cor_pidx_dict[coordinate] = set()

    for coor in coor_remain:
        for pidx in pents_remain:
            if coor not in pent_dict[pidx].keys():
                continue
            for pent, cor_add_list in pent_dict[pidx][coor]:
                valid = True
                for c in cor_add_list:
                    if c not in coor_remain:
                        valid = False
                        break
                if valid:
                    for c in cor_add_list:
                        cor_dict[c].append((coor, pent, cor_add_list))
                        cor_pidx_dict[c].add(pidx)

    least_coor = min(cor_pidx_dict.keys(), key=lambda least_coor: len(cor_pidx_dict[least_coor]))
    if len(cor_pidx_dict[least_coor]) == 0:
        return None

    for assignment_cor, ori_pent, cor_add_list in cor_dict[least_coor]:
        pidx = get_pent_idx(ori_pent)
        solution.append((ori_pent, assignment_cor))
        pents_remain.remove(pidx)
                
        for c in cor_add_list:
            coor_remain.remove(c)
                
        add_pent(board, pidx, cor_add_list)

        print(board)

        if len(solution) == len(pents):
            return solution

        result = recursion(board, pents, solution, pent_dict, coor_remain, pents_remain)
        if result != None:
            return result
        else:
            solution.pop()
            pents_remain.append(pidx)

            coor_remain += cor_add_list

            board[board == (pidx+1)] = -1
    return None

def check_placement(board, pent, coord):
    cor_add_list = []
    for row in range(pent.shape[0]):
        for col in range(pent.shape[1]):
            if pent[row][col] != 0:
                if coord[0]+row >= board.shape[0] or coord[1]+col >= board.shape[1]: # outside board
                    return []
                if board[coord[0]+row][coord[1]+col] >= 0: # Overlap
                    return []
                cor_add_list.append((coord[0]+row, coord[1]+col))
    return cor_add_list

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

def generate_ori(pent): # idx, rot:(0 - 3), flip:(0: non_flip; 1:fliped)
    result = []
    pent_exits = []
    idx = get_pent_idx(pent)

    for i in range(4):
        rot_pent = np.rot90(pent, i)
        rot_exits = False
        for p in pent_exits:
            if np.array_equal(p, rot_pent):
                rot_exits = True
                break
        if not rot_exits:
            pent_exits.append(rot_pent)
            result.append((rot_pent, (idx, i, 0)))

    
    for i in range(4):
        rot_pent = np.rot90(pent, i)
        flip_pent = np.flip(rot_pent)

        flip_exits = False

        for p in pent_exits: # detect duplicates
            if np.array_equal(p, flip_pent):
                flip_exits = True
                break

        if not flip_exits:
            pent_exits.append(flip_pent)
            result.append((flip_pent, (idx, i, 1)))

    return result