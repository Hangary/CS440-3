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
from heapq import heappop, heappush
def mht_dis(pos, goal):
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

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
    num_states_explored = 0
    start = maze.getStart()
    path = [start]
    obj = maze.getObjectives()
    visited = set()
    end = obj[0]
    queue = []
    heappush(queue, (mht_dis(start, end), path, start))
    while queue:
        _, path, cur = heappop(queue)
        if cur in visited:
            continue
        num_states_explored += 1
        visited.add(cur)
        if cur in obj:
            if len(obj) == 1:
                return path, num_states_explored
            obj.remove(cur)
            start = cur
            end = obj[0]
            queue = []
            heappush(queue, (mht_dis(start, end),path, start))
            visited = set()
            continue
        nei = maze.getNeighbors(cur[0], cur[1])
        for n in nei:
            if n in visited:
                continue
            heappush(queue, (mht_dis(n, end), path + [n], n))
    return [], 0

def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    num_states_explored = 0
    start = maze.getStart()
    path = [start]
    obj = maze.getObjectives()
    visited = set()
    end = obj[0]
    queue = []
    heappush(queue, (heuristic(start, obj), 0, path, start))
    while queue:
        _, cost, path, cur = heappop(queue)
        if cur in visited:
            continue
        num_states_explored += 1
        visited.add(cur)
        if cur in obj:
            if len(obj) == 1:
                return path, num_states_explored
            obj.remove(cur)
            start = cur
            end = obj[0]
            queue = []
            heappush(queue, (heuristic(start, obj), 0, path, start))
            visited = set()
            continue
        nei = maze.getNeighbors(cur[0], cur[1])
        for n in nei:
            if n in visited:
                continue
            heappush(queue, (heuristic(start, obj), cost + 1, path + [n], n))
    return [], 0

def estimate(obj): #not in use right now
    cur = obj.pop()
    sum = 0
    while len(obj) >= 1:
        queue = []
        for t in obj:
            heappush(queue, mht_dis(cur, t), t)
        length, next = heappop(queue)
        sum += length
        cur = next
        obj.pop(cur)
    return sum

def heuristic(cur, obj):
    sum = 0
    for t in obj:
        sum += mht_dis(cur, t)
    return sum