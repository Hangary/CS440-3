# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Rahul Kunji (rahulsk2@illinois.edu) on 01/16/2019

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""


# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod)(maze)

from collections import deque

def bfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    start = maze.getStart()
    queue = deque([start])
    visited = set()
    parents = dict()

    result_path = [start]
    targets = maze.getObjectives()
    num_states = 0

    while queue:
        cur_pos = queue.popleft()
        
        if cur_pos in visited:
            continue 

        if cur_pos in targets:
            
            path = [cur_pos]
            pos = cur_pos
            targets.remove(cur_pos)

            while pos != start:
                parent = parents[pos]
                path.append(parent)
                pos = parent
            
            path.pop()
            path.reverse()
                
            result_path += path
            if len(targets) == 0:
                return result_path, num_states

            queue = deque([cur_pos])
            visited = set()
            parents = dict()
            start = cur_pos
            continue

        visited.add(cur_pos)
        num_states += 1
        neighbors = maze.getNeighbors(cur_pos[0], cur_pos[1])

        for n in neighbors:
            if n in visited:
                continue

            parents[n] = cur_pos
            queue.append(n)
            
    return [], 0


def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    start = maze.getStart()
    stack = [start]
    visited = set()
    parents = dict()

    result_path = [start]
    targets = maze.getObjectives()
    num_states = 0

    while stack:
        cur_pos = stack.pop()
        
        if cur_pos in visited:
            continue 

        if cur_pos in targets:
            
            path = [cur_pos]
            pos = cur_pos
            targets.remove(cur_pos)

            while pos != start:
                parent = parents[pos]
                path.append(parent)
                pos = parent
            
            path.pop()
            path.reverse()
                
            result_path += path
            if len(targets) == 0:
                return result_path, num_states

            stack = deque([cur_pos])
            visited = set()
            parents = dict()
            start = cur_pos
            continue

        visited.add(cur_pos)
        num_states += 1
        neighbors = maze.getNeighbors(cur_pos[0], cur_pos[1])

        for n in neighbors:
            if n in visited:
                continue

            parents[n] = cur_pos
            stack.append(n)
            
    return [], 0


def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0


def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0
