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
    # cor_dict = dict()

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
                            # if label not in pent_dict.keys(): # add coordinate to pent_coor list
                            #     pent_dict[label] = dict()
                            #     pent_dict[label][coordinate] = [cor_add_list]
                            # else:
                            #     if coordinate not in pent_dict[label].keys():
                            #         pent_dict[label][coordinate] = [cor_add_list]
                            #     else:
                            #         pent_dict[label][coordinate].append(cor_add_list)
                            #     pent_dict[label] = dict()
                            # pent_dict[label][coordinate] = cor_add_list

                            # if coordinate not in cor_dict.keys(): # add pents to coor_pent list
                            #     cor_dict[coordinate] = dict()
                            # pidx = get_pent_idx(ori_pent)
                            # if pidx not in cor_dict[coordinate].keys():
                            #     cor_dict[coordinate][pidx] = [label]
                            # else:
                            #     cor_dict[coordinate][pidx].append(label)

                            # for c in cor_add_list:
                            #     if c not in cor_dict.keys(): # add pents to coor_pent list
                            #         cor_dict[c] = dict()
                            #     pidx = get_pent_idx(ori_pent)
                            #     if pidx not in cor_dict[c].keys():
                            #         cor_dict[c][pidx] = [label]
                            #     else:
                            #         if label not in cor_dict[c][pidx]:
                            #             cor_dict[c][pidx].append(label)
    
    pents_remain = []
    for p in pents:
        pents_remain.append(get_pent_idx(p))
    
    solution = recursion(board, pents, [], pent_dict, coor_remain, pents_remain)
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

def find_least(cor_dict):
    smallest = None
    for coor in cor_dict.keys():
        if len(cor_dict[coor]) == 0:
            return None
        if smallest == None:
            smallest = coor
            continue
        if len(cor_dict[coor]) < len(cor_dict[smallest]):
            smallest = coor
    return smallest

def add_pent(board, pidx, cor_add_list):
    for c in cor_add_list:
        row = c[0]
        col = c[1]
        if board[row][col] != -1:
            print ("                                                       error")

        board[row][col] = (pidx + 1)
            
def recursion(board, pents, solution, pent_dict, coor_remain, pents_remain):
    cor_dict = dict()

    for coordinate in coor_remain:
        if coordinate == (1,1):
            print(1)
        if coordinate not in cor_dict.keys():
            cor_dict[coordinate] = dict()
        for pidx in pents_remain:
            if coordinate not in pent_dict[pidx].keys():
                continue
            for pent, cor_add_list in pent_dict[pidx][coordinate]:
                valid = True
                for c in cor_add_list:
                    if c not in coor_remain:
                        valid = False
                        break
                if valid:
                    for c in cor_add_list:
                        if c not in cor_dict.keys():
                            cor_dict[c] = dict()
                        if pidx not in cor_dict[c].keys():
                            cor_dict[c][pidx] = [(pent, cor_add_list)]
                        else:
                            cor_dict[c][pidx].append((pent, cor_add_list))

                        # if pidx not in cor_dict[coordinate].keys():
                        #     cor_dict[coordinate][pidx] = [(pent, cor_add_list)]
                        # else:
                        #     cor_dict[coordinate][pidx].append((pent, cor_add_list))
    # for row in range(board.shape[0]):
    #     for col in range(board.shape[1]):
    #         coordinate = (row, col)
    #         if coordinate not in cor_dict.keys() and coordinate not in cor_taken:
    #             cor_dict[coordinate] = dict()
    #         for pidx in pents_remain:
    #             ori_pents_list = generate_ori(pents[pidx])
    #             for ori_pent, label in ori_pents_list:
    #                 cor_add_list = check_placement(board, ori_pent, coordinate)
    #                 invalid = False
    #                 for c in cor_add_list:
    #                     if c in cor_taken:
    #                         invalid = True
    #                         break
                    # if invalid:
                    #     continue
                            
                    # for c in cor_add_list:
                    #     if c not in cor_dict.keys():
                    #         cor_dict[c] = dict()
                    #     if pidx not in cor_dict[c].keys():
                    #         cor_dict[c][pidx] = [(ori_pent, cor_add_list)]
                    #     else:
                    #         cor_dict[c][pidx].append((ori_pent, cor_add_list))

    while len(cor_dict) != 0:
        least_coor = find_least(cor_dict)
        if least_coor == None:
            return None

        for pidx in cor_dict[least_coor].keys():
            for ori_pent, cor_add_list in cor_dict[least_coor][pidx]:
                solution.append((ori_pent, cor_add_list[0]))
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
        cor_dict.pop(least_coor)
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