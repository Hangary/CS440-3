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
                    for ori_pent in rot_flip_list:
                        if check_placement(board, ori_pent, coordinate):
                            if idx not in pent_dict.keys(): # add coordinate to pent_coor list
                                pent_dict[idx] = [coordinate]
                            else:
                                if coordinate not in pent_dict[idx]:
                                    pent_dict[idx].append(coordinate)
                            
                            if coordinate not in cor_dict.keys(): # add pents to coor_pent list
                                cor_dict[coordinate] = dict()
                            pidx = get_pent_idx(ori_pent)
                            if pidx not in cor_dict[coordinate].keys():
                                cor_dict[coordinate][idx] = [ori_pent]
                            else:
                                cor_dict[coordinate][idx].append(ori_pent)
    pent_seq = sorted(pent_dict, key=lambda pidx: len(pent_dict[pidx]), reverse=False)
    
    solution = recursion(board, pents, [], pent_dict, cor_dict, pent_seq)
    print(solution)
    # # if app is not None:
    # #     app.draw_solution_and_sleep(solution, 1)
    return solution
            
def recursion(board, pents, solution, pent_dict, cor_dict, pent_seq):

    # if check_board(board, pents):
    #     return None

    # for pidx in list(sorted(pent_dict, key=lambda pidx: len(pent_dict[pidx]), reverse=False)):
        # for coor in list(sorted(pent_dict[pidx], key=lambda coor: len(cor_dict[coor]), reverse=False)):
    for pidx in pent_seq:
        for coor in pent_dict[pidx]:
            for pent in cor_dict[coor][pidx]:
                
                new_board = None

                if check_placement(board, pent, coor):
                    new_board = board.copy()
                    add_pentomino(new_board, pent, coor, check_pent=True, valid_pents=pents)
                else:
                    continue

                print(new_board)

                new_solution = solution.copy()
                new_solution.append((pent, coor))

                if len(pent_seq) == 1:
                    return new_solution
                    
                # new_pent_dict = pent_dict.copy()
                # new_pent_dict.pop(pidx)

                new_pents = pents.copy()
            
                for i in range(len(new_pents)): #remove added pentomino from pents
                    if get_pent_idx(new_pents[i]) == pidx:
                        new_pents.pop(i)
                        break
                
                new_pent_seq = pent_seq.copy()
                new_pent_seq.remove(pidx)
                    
                if check_board(new_board, new_pents):
                    break
            
                result = recursion(new_board, new_pents, new_solution, pent_dict, cor_dict, new_pent_seq)
                if result != None:
                    return result

    return None
    # for coor in list(sorted(cor_dict, key=lambda coor: len(cor_dict[coor]), reverse=False)):
    #     pents_list = cor_dict[coor].copy()

    #     # print(coor)
    #     # print(len(pents_list))

    #     for pent in list(sorted(pents_list, key=lambda pent: len(pent_dict[get_pent_idx(pent)]), reverse=False)):
    #         p_idx = get_pent_idx(pent)
    #         new_board = board.copy()
    #         new_pents = pents.copy()

    #         add_pentomino(new_board, pent, coor, check_pent=True, valid_pents=new_pents)

    #         print(new_board)

    #         result = solution.copy()
    #         result.append((pent, coor))

    #         if len(new_pents) == 1:
    #             return result
            
    #         for i in range(len(new_pents)): #remove added pentomino from pents
    #             if get_pent_idx(new_pents[i]) == p_idx:
    #                 new_pents.pop(i)
    #                 break
            
    #         recursion(new_board, new_pents, solution = result)
            
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
                if board[coord[0]+row][coord[1]+col] != -1: # Overlap
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

def generate_ori(pent):
    l = []
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
            l.append(rot_pent)
        if not flip_exits:
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
    # shuffle(l)
    return l

def check_placement(board, pent, coord):
    for row in range(pent.shape[0]):
        for col in range(pent.shape[1]):
            if pent[row][col] != 0:
                if coord[0]+row >= board.shape[0] or coord[1]+col >= board.shape[1]: # outside board
                    return False
                if board[coord[0]+row][coord[1]+col] >= 0: # Overlap
                    return False
    return True

# def check_board(board):
#     for row in range(board.shape[0] - 1):
#         for col in range(board.shape[1] - 1):
#             if row - 1 >= 0 and col - 1 >= 0:
#                 if board[row][col] == -1 and board[row+1][col] != -1 and board[row][col+1] !=-1 and board[row-1][col] != -1 and board[row][col-1] != -1:
#                     return True
#             if row - 1 >= 0:
#                 if board[row][col] == -1 and board[row+1][col] != -1 and board[row][col+1] !=-1 and board[row-1][col] != -1:
#                     return True

#             if col - 1 >= 0:
#                 if board[row][col] == -1 and board[row+1][col] != -1 and board[row][col+1] !=-1 and board[row][col-1] != -1:
#                     return True
#     return False

def check_board(board, pents):

    ori_dict = dict()
    new_board = board.copy()
    ori_pents_list = []
    for pent in pents:
         ori_pents_list += generate_ori(pent)
         ori_dict[get_pent_idx(pent)] = generate_ori(pent)

    for row in range(board.shape[0]):
        for col in range(board.shape[1]):

            # for pent in ori_pents_list:
            #     if check_placement(new_board, pent, (row, col)):
            #         for y in range(pent.shape[0]):
            #             for x in range(pent.shape[1]):
            #                 if pent[y][x] != 0:
            #                     new_board[row+y][col+x] = -2

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

    # print(new_board)

    # for y in range(new_board.shape[0]):
    #     for x in range(new_board.shape[1]):
    #         if new_board[y][x] == -1:
    #             return True

    return not len(ori_dict) == 0

    # new_board = board.copy()
    # new_pents = pents.copy()

    # for y in range(new_board.shape[0]):
    #     for x in range(new_board.shape[1]):
    #         if board[y][x] == -1:   
    #             for i in range(len(new_pents)):
    #                 ori_pents = generate_ori(new_pents[i])
    #                 can_add = False
    #                 for pent in ori_pents:
    #                     if check_placement(new_board, pent, (y, x)):
    #                         can_add = True
    #                         break
    #                 if can_add:
    #                     new_pents.pop(i)
    #                     break
    # return not has_corner and (len(new_pents) == 0)


                            
                
                   