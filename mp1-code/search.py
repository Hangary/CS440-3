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

import collections as col

def bfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    queue = col.deque([])
    visited = []
    parents = dict()
    cur_shortest = []
    targets = maze.getObjectives()
    start = maze.getStart()

    parents[start] = (-1, -1)
    queue.append(start)

    while len(queue) != 0:
        cur_pos = queue.popleft()
        cur_visited = []
        neighbors = maze.getNeighbors(cur_pos[0], cur_pos[1])

        for neighbor in neighbors:
            if neighbor in visited:
                continue
            cur_visited.append(neighbor)
            parents[neighbor] = cur_pos
            queue.append(neighbor)
            if neighbor == targets[0]:
                path = [targets[0]]
                pos = targets[0]

                while pos != start:
                    parent = parents[pos]
                    path.append(parent)
                    pos = parent

                if (len(cur_shortest) == 0) or (len(path) < len(cur_shortest)):
                    cur_shortest = path

                break
        visited = visited + cur_visited

    return cur_shortest, len(visited)


def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    stack = []
    visited = []
    parents = dict()
    
    targets = maze.getObjectives()
    start = maze.getStart()

    parents[start] = (-1, -1)
    stack.append(start)

    while len(stack) != 0:
        cur_pos = stack.pop()
        neighbors = maze.getNeighbors(cur_pos[0], cur_pos[1])

        for neighbor in neighbors:
            if neighbor in visited:
                continue

            parents[neighbor] = cur_pos
            stack.append(neighbor)
            visited.append(neighbor)
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