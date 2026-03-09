import heapq
import numpy as np

def heuristic(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

def astar(Z,start,goal):

    neighbors = [(1,0),(-1,0),(0,1),(0,-1)]

    close_set = set()

    came_from = {}

    gscore = {start:0}

    fscore = {start:heuristic(start,goal)}

    oheap = []

    heapq.heappush(oheap,(fscore[start],start))

    while oheap:

        current = heapq.heappop(oheap)[1]

        if current == goal:

            data = []

            while current in came_from:
                data.append(current)
                current = came_from[current]

            return data[::-1]

        close_set.add(current)

        for i,j in neighbors:

            neighbor = current[0]+i,current[1]+j

            tentative = gscore[current]+1

            if 0 <= neighbor[0] < Z.shape[0]:

                if 0 <= neighbor[1] < Z.shape[1]:

                    pass
                else:
                    continue
            else:
                continue

            if neighbor in close_set and tentative >= gscore.get(neighbor,0):
                continue

            if tentative < gscore.get(neighbor,0) or neighbor not in [i[1] for i in oheap]:

                came_from[neighbor] = current

                gscore[neighbor] = tentative

                fscore[neighbor] = tentative + heuristic(neighbor,goal)

                heapq.heappush(oheap,(fscore[neighbor],neighbor))

    return []
