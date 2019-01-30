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
from collections import deque
from heapq import heappop, heappush
def mht_dis(pos, goal):
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod)(maze)


def bfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    num_states_explored = 0
    start = maze.getStart()
    path = [start]
    obj = maze.getObjectives()
    visited = set()
    queue = deque([(start, path)])
    while queue:
        cur, path = queue.popleft()
        if cur in visited:
            continue
        visited.add(cur)
        num_states_explored += 1
        if cur in obj:
            if len(obj) == 1:
                return path, num_states_explored
            visited = set()
            queue = deque([(cur, path)])
            obj.remove(cur)
            continue
        nei = maze.getNeighbors(cur[0], cur[1])
        for n in nei:
            if n in visited:
                continue
            queue.append((n, path + [n]))
    return [], 0


def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    num_states_explored = 0
    start = maze.getStart()
    path = [start]
    obj = maze.getObjectives()
    visited = set()
    stack = [(start, path)]
    while stack:
        cur, path = stack.pop()
        if cur in visited:
            continue
        visited.add(cur)
        num_states_explored += 1
        if cur in obj:
            if len(obj) == 1:
                return path, num_states_explored
            visited = set()
            stack = [(cur, path)]
            obj.remove(cur)
            continue
        nei = maze.getNeighbors(cur[0], cur[1])
        for n in nei:
            if n in visited:
                continue
            stack.append((n, path + [n]))
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

def get_dis(start, end, maze):
    visited = set()
    queue = []
    heappush(queue, (mht_dis(start, end), 0, start))
    while queue:
        _, cost, cur = heappop(queue)
        if cur in visited:
            continue
        visited.add(cur)
        if cur == end:
            return cost+1
        nei = maze.getNeighbors(cur[0], cur[1])
        for n in nei:
            if n in visited:
                continue
            heappush(queue, (cost + mht_dis(n, end), cost + 1, n))
    return [], 0

def mst(maze):
    start = maze.getStart()
    obj = maze.getObjectives()
    mst = {}
    mst[start] = []
    dic = {}
    dic[start] = (0, None)
    l = 0
    dic2 = {}
    for x in obj:
        mst[x] = []
        dic[x] = (float('inf'), None)
    while dic:
        min = float('inf')
        minx = None
        for x in dic:
            if dic[x][0] < min:
                min = dic[x][0]
                minx = x
        par = dic[x][1]
        dic.pop(minx)
        l += min
        if par is not None:
            mst[minx].append((min, par))
            mst[par].append((min, minx))
        cur = minx
        for x in dic:
            dis = get_dis(cur, x, maze)
            dic2[(cur,x)] = dis
            dic2[(x,cur)] = dis
            if dis < dic[x][0]:
                dic[x] = (dis, cur)
    return mst, l, dic2

def astar1(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    num_states_explored = 0
    start = maze.getStart()
    path = [start]
    obj = maze.getObjectives()
    visited = set()
    end = obj[0]
    queue = []
    heappush(queue, (mht_dis(start, end), 0, path, start))
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
            heappush(queue, (mht_dis(start, end), 0, path, start))
            visited = set()
            continue
        nei = maze.getNeighbors(cur[0], cur[1])
        for n in nei:
            if n in visited:
                continue
            heappush(queue, (cost + mht_dis(n, end), cost + 1, path + [n], n))
    return [], 0

def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    if len(maze.getObjectives() == 1):
        return astar1(maze)
    num_states_explored = 0
    start = maze.getStart()
    path = [start]
    obj = maze.getObjectives()
    visited = set()
    mst_dic, l, dic = mst(maze)
    min = float('inf')
    for x in mst_dic[start]:
        if x[0] < min:
            min = x[0]
            end = x[1]
    queue = []
    heappush(queue, (mht_dis(start, end)+min, 0, path, start))
    while queue:
        _, cost, path, cur = heappop(queue)
        if cur in visited:
            continue
        num_states_explored += 1
        visited.add(cur)
        min_md = float('inf')
        for x in obj:
            if mht_dis(cur, x) < min_md:
                end = x
                min_md = mht_dis(cur, x)
        min = dic[(start, end)]
        if cur in obj:
            if len(obj) == 1:
                return path, num_states_explored
            obj.remove(cur)
            l -= dic[(start, end)]
            start = cur
            min = float('inf')
            for x in mst_dic[start]:
                if x[0] < min and x[1] in obj:
                    min = x[0]
                    end = x[1]
            queue = []
            heappush(queue, (mht_dis(start, end) + l - min, 0, path, start))
            visited = set()
            continue
        nei = maze.getNeighbors(cur[0], cur[1])
        for n in nei:
            if n in visited:
                continue
            heappush(queue, (cost + mht_dis(n, end) + l - min, cost + 1, path + [n], n))
    return [], 0
