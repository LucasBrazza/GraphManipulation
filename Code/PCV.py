import BasicDimacs
import time

start_time = time.time()
current_time = time.time()
elapsed_time = current_time - start_time
seconds = 0


def findPath():
    """Runs the Nearest Neighbour and Refine the result path using 2-OPT strategy"""
    global seconds
    fileName = input('ARCHIVE NAME: ')
    file = open(fileName, 'r')
    seconds = int(input('EXECUTION TIME LIMIT (s): '))

    adjList = BasicDimacs.AdjacencyList(file)

    path = nearestNeighbour(adjList)
    path = twoOpt(path, adjList)

    print(path)
    pathCost(path, adjList)
    file.close()


def nearestNeighbour(adjList):
    """Runs the Nearest Neighbour algorithm to a given graph"""
    global current_time
    global elapsed_time
    global start_time

    start_time = time.time()
    current_time = time.time()
    elapsed_time = current_time - start_time

    u = (0)
    path = [u]
    notVisited = [i for i in range(len(adjList))]
    notVisited.pop(0)
    smallerNode = None

    while notVisited and (elapsed_time < seconds):
        smallerWeight = float('inf')
        for node in adjList[u]:
            if node[0] in notVisited:
                currentWeight = node[1]
                if smallerWeight > currentWeight:
                    smallerWeight = currentWeight
                    smallerNode = node[0]

        path.append(smallerNode)
        notVisited.remove(smallerNode)
        u = smallerNode
        current_time = time.time()
        elapsed_time = current_time - start_time

    path.append(adjList[smallerNode][0][0])
    return path


def twoOpt(path, adjList):
    """Runs the 2-OPT refine strategy to a given path of a given graph"""
    global current_time
    global elapsed_time

    current_time = time.time()
    elapsed_time = current_time - start_time
    best = path
    improved = True

    while improved and (elapsed_time < seconds):
        improved = False
        if elapsed_time > seconds:
            print(f"ITERATION FINISHED IN:  {int(elapsed_time)} seconds.")
            break

        for i in range(1, len(path) - 2):
            for j in range(i + 1, len(path)):
                if j - i == 1:
                    continue

                a = best[i - 1]
                b = best[i]
                c = best[j - 1]
                d = best[j]

                if differenceCost(adjList, a, b, c, d) < 0:
                    best[i:j] = best[j - 1: i - 1: -1]
                    improved = True

        path = best
        current_time = time.time()
        elapsed_time = current_time - start_time

    return best


def differenceCost(adjList, a, b, c, d):
    """Calculates the cost difference between two sets of nodes"""
    ac = 0
    bd = 0
    ab = 0
    cd = 0

    if a > c:
        ac = adjList[a][c][1]
    else:
        ac = adjList[a][c - 1][1]

    if a > b:
        ab = adjList[a][b][1]
    else:
        ab = adjList[a][b - 1][1]

    if b > d:
        bd = adjList[b][d][1]
    else:
        bd = adjList[b][d - 1][1]

    if c > d:
        cd = adjList[c][d][1]
    else:
        cd = adjList[c][d - 1][1]

    result = (ac + bd) - (ab + cd)
    return result


def pathCost(path, adjList):
    """Calculates the total cost of a given path of a given graph"""
    cost = 0
    first = True
    for u in range(len(path)):
        origin = path[u]
        if path[u] == path[0]:
            if first:
                destiny = path[u + 1]
                first = False
                if origin > destiny:
                    cost += adjList[origin][destiny][1]
                else:
                    cost += adjList[origin][destiny - 1][1]
        else:
            destiny = path[u + 1]
            if origin > destiny:
                cost += adjList[origin][destiny][1]
            else:
                cost += adjList[origin][destiny - 1][1]
    cost = round(cost, 2)
    file = open("Results.txt", 'w')
    file.write(str(cost) + "\n")
    file.write(str(path))
    file.close()
    return cost
