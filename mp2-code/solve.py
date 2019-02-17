# -*- coding: utf-8 -*-
import time
import random
import numpy as np
import instances


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

    # raise NotImplementedError

    start_time = time.time()
    board = board.copy() - 1  # avoid conflict ones
    result = []
    candidates = flip_and_rotate(pents)
    shuffleCandidates(candidates)
    backtrack(board, candidates, result)
    print(board)
    print("Time: %.4f seconds" % (time.time() - start_time))
    return result


def backtrack(board, candidates, result):
    position = None
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if (board[i, j] == 0):
                position = (i, j)
                break
        if position:
            break
    # print(candidates)
    if position == None:
        return True
    for idx in range(len(candidates)):
        if candidates[idx] == None:
            continue
        pent_group = candidates[idx]
        candidates[idx] = None
        for pent in pent_group:
            try_result = try_tile(pent, position, board)
            if (try_result != None):
                result.append(try_result)
                if backtrack(board, candidates, result):
                    return True
                else:
                    result.pop()
                    remove_tile(try_result[0], try_result[1], board)
        candidates[idx] = pent_group

    return False


def flip_and_rotate(pents):
    """
    Each pentomino is turned into a list of its rotated & flipped pentominos
    """
    result = []
    for pent in pents:
        transformed = []
        transformed += [np.rot90(pent, i) for i in range(4)]
        flipped = np.flip(pent, axis=1)
        transformed += [np.rot90(flipped, i) for i in range(4)]
        new_transformed = []
        for p1 in transformed:
            flag = True
            for p2 in new_transformed:
                if (np.array_equal(p1, p2)):
                    flag = False
            if flag:
                new_transformed.append(p1)
        result.append(new_transformed)
    return result


def try_tile(pent, position, board):
    """
    Try to put pent onto board at position
    """
    offset = np.argmax(pent[0:])  # the position of the top-left element of the pentomino
    coord = (position[0], position[1] - offset)
    if (coord[1] < 0):
        return None
    if (coord[0] + pent.shape[0] > board.shape[0] or coord[1] + pent.shape[1] > board.shape[1]):
        return None
    for i in range(pent.shape[0]):
        for j in range(pent.shape[1]):
            if (pent[i, j] != 0 and board[coord[0] + i, coord[1] + j] != 0):
                return None
    for i in range(pent.shape[0]):
        for j in range(pent.shape[1]):
            if (pent[i, j] != 0):
                board[coord[0] + i, coord[1] + j] = pent[i, j]
    # print(board)
    return (pent, coord)


def remove_tile(pent, coord, board):
    for i in range(pent.shape[0]):
        for j in range(pent.shape[1]):
            if (pent[i, j] != 0):
                board[coord[0] + i, coord[1] + j] = 0


def shuffleCandidates(candidates):
    for group in candidates:
        random.shuffle(group)
    random.shuffle(candidates)
