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
    cor_dict = dict()

    board = np.negative(board)
    for y in range(board.shape[0]):
        for x in range(board.shape[1]):
            coordinate = (y,x)
            if board[y][x] == -1:
                for pent in pents:
                    idx = get_pent_idx(pent)
                    rot_flip_list = generate_ori(pent)
                    for ori_pent, label in rot_flip_list:
                        cor_add_list =  check_placement(board, ori_pent, coordinate)
                        if cor_add_list != []:
                            if label not in pent_dict.keys(): # add coordinate to pent_coor list
                                pent_dict[label] = (coordinate, cor_add_list)
                            #     pent_dict[label] = dict()
                            # pent_dict[label][coordinate] = cor_add_list

                            for c in cor_add_list:
                                if c not in cor_dict.keys(): # add pents to coor_pent list
                                    cor_dict[c] = dict()
                                pidx = get_pent_idx(ori_pent)
                                if pidx not in cor_dict[c].keys():
                                    cor_dict[c][idx] = [label]
                                else:
                                    cor_dict[c][idx].append(label)
    
    pents_remain = []
    for p in pents:
        pents_remain.append(get_pent_idx(p))

    
    solution = recursion(board, pents, [], pent_dict, cor_dict, pents_remain)
    print(solution)
    # # if app is not None:
    # #     app.draw_solution_and_sleep(solution, 1)
    return solution
def get_pent(label, pents):
    ori_pent = None
    for pent in pents:
        idx = get_pent_idx(pent)
        if idx == label[0]:
            ori_pent = np.rot90(pent, label[1])
            if label[2] == 1:
                ori_pent = np.flip(ori_pent)
            return ori_pent
    print(1/0)
    return None
            
def recursion(board, pents, solution, pent_dict, cor_dict, pents_remain):

    for coor in sorted(cor_dict.keys(), key=lambda coor: len(cor_dict[coor]), reverse=False):
        for pidx in cor_dict[coor].keys():
            label_list = cor_dict[coor][pidx]
            for label in label_list:
                if label[0] not in pents_remain:
                    continue
                
                missing_cor = False
                start_cor, cor_add_list = pent_dict[label]
                for cor_needed in cor_add_list:
                    if cor_needed not in cor_dict.keys():
                        missing_cor = True
                        break
                if missing_cor:
                    continue
                
                pent = get_pent(label, pents)
            
                new_board = board.copy()
                add_pentomino(new_board, pent, start_cor)
                print(new_board)

                new_solution = solution.copy()
                new_solution.append((pent, start_cor))

                new_pents_remain = pents_remain.copy()
                new_pents_remain.remove(label[0])

                if len(new_solution) == len(pents):
                    return new_solution
            
                new_cor_dict = cor_dict.copy()

                for c in cor_add_list:
                    if c in new_cor_dict.keys():
                        new_cor_dict.pop(c)

                result = recursion(new_board, pents, new_solution, pent_dict, new_cor_dict, new_pents_remain)
                if result != None:
                    return result

    # for pidx in sorted(pent_dict, key=lambda pidx: len(pent_dict[pidx]), reverse=False):
        
            # for pent in cor_dict[coor][pidx]:
                
            #     new_board = None
            #     cor_add_list = None
            #     if check_placement(board, pent, coor):
            #         new_board = board.copy()
            #         cor_add_list = add_pentomino(new_board, pent, coor)
            #     else:
            #         continue

            #     print(new_board)

                # new_solution = solution.copy()
                # new_solution.append((pent, coor))

                # if len(new_solution) == len(pents):
                #     return new_solution
                
                # new_pent_dict = pent_dict.copy()
                # new_pent_dict.pop(pidx)

                # zero_list = []
                # for p in new_pent_dict.keys():
                #     new_pent_dict[p] = pent_dict[p].copy()
                #     for coor_added in cor_add_list:
                #         if coor_added in new_pent_dict[p]:
                #             new_pent_dict[p].remove(coor_added)
                #             if (len(new_pent_dict[p]) == 0):
                #                     zero_list.append(p)
                
                # for z in zero_list:
                #     new_pent_dict.pop(z)            
                
                # new_cor_dict = cor_dict.copy()
                # for coor_added in cor_add_list:
                #     if coor_added in new_cor_dict.keys():
                #         new_cor_dict.pop(coor_added)

                # for c in new_cor_dict.keys():
                #     new_cor_dict[c] = cor_dict[c].copy()
                #     if pidx in new_cor_dict[c].keys():
                #         new_cor_dict[c].pop(pidx)
            
                # result = recursion(new_board, pents, new_solution, new_pent_dict, new_cor_dict)
                # if result != None:
                #     return result

    return None
            
def add_pentomino(board, pent, coord):
    cor_add_list = []
    for row in range(pent.shape[0]):
        for col in range(pent.shape[1]):
            if pent[row][col] != 0:
                if board[coord[0]+row][coord[1]+col] != -1: # Overlap
                    return False
                else:
                    board[coord[0]+row][coord[1]+col] = pent[row][col]
                    cor_add_list.append((coord[0]+row, coord[1]+col))
    return cor_add_list

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

def is_pentomino(pent, pents):
    """
    Checks if a pentomino pent is part of pents
    """
    pidx = get_pent_idx(pent)
    if pidx == -1:
        return False

    idx = None
    for i in range(len(pents)):
        if get_pent_idx(pents[i]) == pidx:
            idx = i
            break
    true_pent = pents[idx]
    
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

def generate_ori(pent): # idx, rot:(0 - 3), flip:(0: non_flip; 1:fliped)
    l = []
    idx = get_pent_idx(pent)
    for i in range(4):
        rot_pent = np.rot90(pent, i)
        flip_pent = np.flip(rot_pent)

        rot_exits = False
        flip_exits = False

        for p in l: # detect duplicates
            if np.array_equal(p, rot_pent):
                rot_exits = True
            if np.array_equal(p, flip_pent):
                flip_exits = True
            if rot_exits and flip_exits:
                break

        if not rot_exits:
            l.append((rot_pent, (idx, i, 0)))
        if not flip_exits:
            l.append((flip_pent, (idx, i, 1)))

    return l

def check_board(board, pents):

    ori_dict = dict()
    new_board = board.copy()
    ori_pents_list = []
    for pent in pents:
         ori_pents_list += generate_ori(pent)
         ori_dict[get_pent_idx(pent)] = generate_ori(pent)

    for row in range(board.shape[0]):
        for col in range(board.shape[1]):

            pop_list = []
            for pidx in ori_dict.keys():
                for pent in ori_dict[pidx]:
                    if check_placement(board, pent, (row, col)):
                        pop_list.append(pidx)
                        break
            for idx in pop_list:
                ori_dict.pop(idx)

            if row == board.shape[0] - 1 and col == board.shape[1] - 1:
                if board[row][col] == -1 and board[row - 1][col] != -1 and board[row][col - 1] !=-1:
                    return True 
                else: continue

            if row == board.shape[0] - 1:
                if board[row][col] == -1 and board[row][col - 1] != -1 and board[row][col+1] !=-1 and board[row-1][col] != -1:
                    return True
                else: continue

            if col == board.shape[1] - 1:
                if board[row + 1][col] == -1 and board[row - 1][col] != -1 and board[row][col-1] !=-1:
                    return True
                else: continue

            if row == 0 and col == 0:
                if board[row][col] == -1 and board[row+1][col] != -1 and board[row][col+1] !=-1:
                    return True
                else: continue

            if row == 0:
                if board[row][col] == -1 and board[row+1][col] != -1 and board[row][col+1] !=-1 and board[row][col-1] != -1:
                    return True
                else: continue

            if col == 0:
                if board[row][col] == -1 and board[row+1][col] != -1 and board[row-1][col] !=-1 and board[row][col+1] != -1:
                    return True
                else: continue
            
            if board[row][col] == -1 and board[row+1][col] != -1 and board[row-1][col] !=-1 and board[row][col+1] != -1 and board[row][col-1] != -1:
                    return True

    return not len(ori_dict) == 0