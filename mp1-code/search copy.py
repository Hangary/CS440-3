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

class State():
    def __init__(self, pos, obj):
        self.pos = pos
        self.obj = obj

    def __hash__(self):
        self.hash = hash((tuple(self.obj), self.pos))
        return self.hash



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

def bfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    num_states_explored = 0
    start = maze.getStart()
    path = [start]
    obj = maze.getObjectives()
    visited = {}
    queue = deque([(State(start, obj), path)])
    while queue:
        cur, path= queue.popleft()
        if hash(cur) in visited.keys():
            continue
        visited[hash(cur)] = 1
        num_states_explored += 1
        if cur.pos in cur.obj:
            if len(cur.obj) == 1:
                print(path)
                return path, num_states_explored
            cobj = cur.obj.copy()
            cobj.remove(cur.pos)
            queue.append((State(cur.pos, cobj), path))
            continue
        nei = maze.getNeighbors(cur.pos[0], cur.pos[1])
        for n in nei:
            s = State(n, cur.obj)
            if hash(s) in visited.keys():
                continue
            queue.append((s, path + [n]))
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
            return cost
        nei = maze.getNeighbors(cur[0], cur[1])
        for n in nei:
            if n in visited:
                continue
            heappush(queue, (cost + mht_dis(n, end), cost + 1, n))
    return [], 0

def mst(maze):
    start = maze.getStart()
    obj = maze.getObjectives()
    dic = {}
    l = 0
    dic2 = {}
    c = 0
    dic[start] = (0,None)
    for x in obj:
        dic[x] = (float('inf'), None)
    while dic:
        min = float('inf')
        minx = None
        for x in dic:
            if dic[x][0] < min:
                min = dic[x][0]
                minx = x
        dic.pop(minx)
        l += min
        cur = minx
        for x in dic:
            dis = get_dis(cur, x, maze)
            dic2[(cur,x)] = dis
            dic2[(x,cur)] = dis
            if dis < dic[x][0]:
                dic[x] = (dis, cur)
    return l, dic2

def mst2(maze, obj, dic2):
    if len(obj) <= 1:
        return 0
    dic = {}
    l = 0
    count = 0
    for x in obj:
        if count == 0:
            dic[x] = (0, None)
            count = 1
            continue
        dic[x] = (float('inf'), None)
    while dic:
        min = float('inf')
        minx = None
        for x in dic:
            if dic[x][0] < min:
                min = dic[x][0]
                minx = x
        dic.pop(minx)
        l += min
        cur = minx
        for x in dic:
            if (cur,x) not in dic2.keys():
                dic2[(cur,x)] = get_dis(cur, x, maze)
                dic2[(x, cur)] = dic2[(cur,x)]
            dis = dic2[(cur,x)]
            if dis < dic[x][0]:
                dic[x] = (dis, cur)
    return l




def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    num_states_explored = 0
    start = maze.getStart()
    path = [start]
    obj = maze.getObjectives()
    visited = {}
    dic2 = {}
    queue = []
    dic = {}
    t_obj = tuple(obj)
    dic[t_obj] = mst2(maze, obj, dic2)
    heappush(queue, (0, 0, path, State(start, obj)))
    while queue:
        _, cost, path, cur = heappop(queue)
        if hash(cur) in visited.keys():
            continue
        visited[hash(cur)] = cost
        num_states_explored += 1
        if cur.pos in cur.obj:
            if len(cur.obj) == 1:
                return path, num_states_explored
            cobj = cur.obj.copy()
            cobj.remove(cur.pos)
            if tuple(cur.obj) not in dic.keys():
                dic[tuple(cur.obj)] = mst2(maze, cur.obj, dic2)
            l = dic[tuple(cur.obj)]
            heappush(queue, (cost +l , cost, path, State(cur.pos, cobj)))
            continue
        nei = maze.getNeighbors(cur.pos[0], cur.pos[1])
        if tuple(cur.obj) not in dic.keys():
            dic[tuple(cur.obj)] = mst2(maze, cur.obj, dic2)
        l = dic[tuple(cur.obj)]
        for n in nei:
            min_md = float('inf')
            for x in cur.obj:
                if mht_dis(n, x) < min_md:
                    end = x
                    min_md = mht_dis(n, x)
                    if min_md == 0:
                        break
            s = State(n, cur.obj)
            if hash(s) in visited.keys():
                continue
            heappush(queue, (cost + min_md + l , cost + 1, path + [n], s))
    return [], 0
