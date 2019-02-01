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

class state:
    def __init__(self, cur, explored):
        self.cur = cur
        self.explored = explored
    
    def __eq__(self, other):
        return self.cur == other.cur and self.explored == other.explored

    def __hash__(self):
        return hash(str(self.explored))

def bfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    num_states_explored = 0
    start = maze.getStart()
    path = [start]
    obj = maze.getObjectives()
    visited = []
    explored = set()
    # initial = state(start, explored)
    queue = deque([(start, explored, obj, path)])
    while queue:
        cur, explored, obj, path = queue.popleft()
        # if ([(6,3), (6,2), (5,2), (5,1)] in path):
        #     print(path)
        obj_left = obj.copy()
        cur_explored = explored.copy()
        cur_explored.add(cur)
        cur_state = (cur, cur_explored)
        visited.append(cur_state)
        num_states_explored += 1
        if cur in obj_left:
            obj_left.remove(cur)
            print(len(obj_left))
            if len(obj_left) == 0:
                return path, num_states_explored
        nei = maze.getNeighbors(cur[0], cur[1])
        for n in nei:
            # temp_explored = cur_explored.copy()
            # temp_explored.add(n)
            n_state = (n, cur_explored)
            if n_state in visited:
                # print("n in visited")
                continue
            queue.append((n, cur_explored, obj_left, path + [n]))
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
    visited = dict()
    end = obj[0]
    queue = []
    min = float('inf')
    for x in obj:
        if mht_dis(start, x) < min:
            min = mht_dis(start, x)
            end = x
    heappush(queue, (mht_dis(start, end), 0, path, start))
    while queue:
        _, cost, path, cur = heappop(queue)
        # if cur in visited.keys() and new_heu >= visited[cur]:
        #     continue
        num_states_explored += 1
        min_md = float('inf')
        # for x in obj:
        #     if mht_dis(cur, x) < min_md:
        #         end = x
        #         min_md = mht_dis(cur, x)
        if cur in obj:
            if len(obj) == 1:
                return path, num_states_explored
            obj.remove(cur)
            start = cur
            end = obj[0]
            min = float('inf')
            for x in obj:
                if mht_dis(start, x) < min:
                    min = mht_dis(start, x)
                    end = x
            queue = []
            heappush(queue, (cost + mht_dis(start, end), cost + 1, path, start))
            visited = dict()
            continue
        nei = maze.getNeighbors(cur[0], cur[1])
        for n in nei:
            # if n in visited:
            #     continue
            if n in visited.keys() and cost + mht_dis(n, end) >= visited[n]:
                continue
            visited[n] = cost + mht_dis(n, end)
            heappush(queue, (cost + mht_dis(n, end), cost + 1, path + [n], n))
    return [], 0