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
    queue = deque([(start, [start])])
    visited = set()
    targets = maze.getObjectives()
    num_states = 0

    while queue:
        cur,path = queue.popleft()
        if cur in visited:
            continue
        if cur in targets:
            if len(targets) == 1:
                return path, num_states
            targets.remove(cur)
            queue = deque([(cur, path)])
            visited = set()
    
        visited.add(cur)
        num_states += 1
        neighbors = maze.getNeighbors(cur[0], cur[1])
        for n in neighbors:
            if n in visited:
                continue
            queue.append((n, path+[n]))

    return [], 0


def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    stack = []
    visited = set()
    parents = dict()
    
    targets = maze.getObjectives()
    start = maze.getStart()

    parents[start] = (-1, -1)
    stack.append(start)

    while len(stack) != 0:
        cur_pos = stack.pop()
        neighbors = maze.getNeighbors(cur_pos[0], cur_pos[1])
        visited.add(cur_pos)
        for neighbor in neighbors:
            if neighbor in visited:
                continue

            parents[neighbor] = cur_pos
            stack.append(neighbor)
            if neighbor == targets[0]:
                path = [targets[0]]
                pos = targets[0]

                while pos != start:
                    parent = parents[pos]
                    path.append(parent)
                    pos = parent

                return path, len(visited)


def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0


def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0
