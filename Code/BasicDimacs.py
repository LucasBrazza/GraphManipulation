import sys


def Entry(fileName):
    """Receive a file name and turns it into a list of string"""
    return open(fileName, 'r')


def AdjacencyList(file):
    """Receive a text file and turns it into a graph of adjacency list"""
    file.seek(0)
    size = int(file.readline().split()[0])
    list = [[] for _ in range(size)]

    line = file.readline()
    while line != '':
        node = int(line.split()[0])
        list[node].append((int(line.split()[1]), float(line.split()[2])))
        node = int(line.split()[1])
        list[node].append((int(line.split()[0]), float(line.split()[2])))
        line = file.readline()
    return list


def AdjacencyMatrix(file):
    """Receive a file and turns it into a graph of adjacency matrix"""
    file.seek(0)
    size = int(file.readline().split()[0])
    matrix = [[0 for _ in range(size)] for _ in range(size)]

    line = file.readline()
    while line != '':
        matrix[int(line.split()[0])][int(line.split()[1])] = int(line.split()[2])
        matrix[int(line.split()[1])][int(line.split()[0])] = int(line.split()[2])
        line = file.readline()
    return matrix


def MostGraded(adjList):
    """Search for the most graded node of a graph"""
    grade = 0
    node = 0

    for current in range(len(adjList)):
        toCompare = len(adjList[current])
        if toCompare > grade:
            node = current
            grade = toCompare

    return grade, node


def LeastGraded(adjList):
    """Search for the least graded node of a graph"""
    grade = len(adjList)
    node = 0

    for current in range(len(adjList)):
        toCompare = len(adjList[current])
        if toCompare < grade:
            node = current
            grade = toCompare

    return grade, node


def AverageGrade(adjList):
    """Calculates the average grade of a graph"""
    size = len(adjList)
    averageGrade = 0

    for i in range(size):
        averageGrade += len(adjList[i])
    averageGrade /= size

    return averageGrade


def RelativeFrequency(adjList):
    """Calculates the relative frequency of a graph and returns a list of [grade, frequency]"""
    size = len(adjList)
    list = []
    index = 0
    for k in range(size):
        nodesQtt = 0
        for i in range(size):
            temp = len(adjList[i])
            if temp == k:
                nodesQtt += 1
        frequency = nodesQtt / size
        if frequency != 0:
            list.append((k, frequency))
            index += 1

    # Remove null values
    for key in range(len(list) - 1, -1, -1):
        if not list[key][1]:
            list.pop(key)

    return list


def BreadthFirstSearch(Graph, init):
    """Write in a text file the nodes of a graph and it position on the search tree"""
    visited = [init]
    queue = [init]

    level = [-1 for _ in range(len(Graph))]
    level[init] = 0

    temp = []
    while queue:
        u = queue.pop(0)
        for v in Graph[u]:
            nodeV = v[0]
            if nodeV not in visited:
                level[nodeV] = level[u] + 1
                visited.append(nodeV)
                queue.append(nodeV)
        temp.append((u, level[u]))

    file = open('BFS_Result.txt', 'w')
    temp = QuickSortTuple(temp)
    while temp:
        u = temp.pop(0)
        file.write(f'{u[0]} : {u[1]}\n')
    file.close()


def DepthFirstSearch(G, init, mark=0):
    """Write in a text file the nodes of a graph and it position on the search tree"""
    visited = [0 for _ in range(len(G))]
    visited[init] = 1
    if mark != 0:
        visited[init] = mark
    Stack = [init]
    R = [init]
    level = [-1 for _ in range(len(G))]
    level[init] = 0

    temp = [(init, level[init])]

    while Stack:
        u = Stack[-1]
        unstack = True
        for v in G[u]:
            nodeV = v[0]
            if visited[nodeV] == 0:
                unstack = False
                Stack.append(nodeV)
                R.append(nodeV)
                visited[nodeV] = 1
                level[nodeV] = level[u] + 1
                temp.append((nodeV, level[nodeV]))
                break
        if unstack:
            Stack.pop()
    temp = QuickSortTuple(temp)
    file = open('DFS_Result.txt', 'w')
    while temp:
        u = temp.pop(0)
        file.write(f'{u[0]} : {u[1]}\n')
    file.close()


def DepthFirstSearchRecursive(Graph, init, visited, mark):
    """Recursive Depth First Search"""
    visited[init] = mark
    for v in Graph[init]:
        nodeV = v[0]
        if visited[nodeV] == 0:
            DepthFirstSearchRecursive(Graph, nodeV, visited, mark)
    return visited


def RelatedComponents(G):
    """Returns a vector with the number of nodes on each related component"""
    visited = [0 for _ in range(len(G))]
    mark = 0
    for i in range(len(G)):
        if visited[i] == 0:
            mark += 1
            DepthFirstSearchRecursive(G, i, visited, mark)

    temp = []
    components = []
    for i in range(len(visited)):
        related = 0
        if visited[i] not in temp:
            temp.append(visited[i])
            for j in range(len(visited)):
                if visited[i] == visited[j]:
                    related += 1
        if related != 0:
            components.append(related)
    return components


# Minimal Paths Algorithms

def BellmanFord(Graph, origin, mode='distance'):
    """Calculates the minimal path of a graph according to the origin node provided"""
    "Returns the number of nodes, the minimal path or the minimal weight to the origin according to the mode " \
    "provided, by default returns the weight."
    distance = [sys.maxsize for _ in range(len(Graph))]
    path = [None for _ in range(len(Graph))]
    distance[origin] = 0
    steps = [sys.maxsize for _ in range(len(Graph))]
    steps[origin] = 0

    for node in range(len(Graph)):
        for link in Graph[node]:
            if distance[link[0]] > distance[node] + link[1]:
                distance[link[0]] = distance[node] + link[1]
                path[link[0]] = node
            if steps[link[0]] > steps[node] + 1:
                steps[link[0]] = steps[node] + 1

    for n in range(len(Graph)):
        if distance[n] == sys.maxsize:
            distance[n] = -1
        if steps[n] == sys.maxsize:
            steps[n] = -1

    if mode == 'steps':
        return steps
    if mode == 'path':
        return path

    return distance


def WeightlessAdjacencyList(file):
    """Receive a text file and turns it into a graph of weightless adjacency list"""
    file.seek(0)
    size = int(file.readline().split()[0])
    lines = file.readlines()
    list = [[] for _ in range(size)]

    for i in range(size - 1):
        line = lines[i]
        node = int(line.split()[0])
        list[node].append(int(line.split()[1]))
        node = int(line.split()[1])
        list[node].append(int(line.split()[0]))

    return list


# To order by grade, change where [0] -> [1]
def QuickSortTuple(array):
    """Sort the array of tuples by using quicksort"""
    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if x[0] < pivot[0]:
                less.append(x)
            if x[0] == pivot[0]:
                equal.append(x)
            if x[0] > pivot[0]:
                greater.append(x)
        return QuickSortTuple(less) + equal + QuickSortTuple(greater)
    else:
        return array


# The following methods were discontinued because they use a adjacency matrix to get the results
# but this is a too complex approach

def MostGradedDiscontinued(file):
    """Search for the most graded node of a graph"""
    file.seek(0)
    size = int(file.readline().split()[0])
    matrix = AdjacencyMatrix(file)

    node = 0
    grade = 0
    for i in range(size):
        temp = 0
        for j in range(size):
            if matrix[i][j] != 0:
                temp += 1
        if temp > grade:
            grade = temp
            node = i
    return [node, grade]


def LeastGradedDiscontinued(file):
    """Search for the least graded node of a graph"""
    file.seek(0)
    size = int(file.readline().split()[0])
    matrix = AdjacencyMatrix(file)

    node = 0
    grade = size
    for i in range(size):
        temp = 0
        for j in range(size):
            if matrix[i][j] != 0:
                temp += 1
        if temp < grade:
            grade = temp
            node = i
    return [node, grade]


def AverageGradeDiscontinued(file):
    """Calculates the average grade of a graph"""
    file.seek(0)
    size = int(file.readline().split()[0])
    matrix = AdjacencyMatrix(file)

    averageGrade = 0
    for i in range(size):
        for j in range(size):
            if matrix[i][j] != 0:
                averageGrade += 1
    averageGrade /= size
    return averageGrade


def RelativeFrequencyDiscontinued(file):
    """Calculates the relative frequency of a graph and returns a list of [grade, frequency]"""
    file.seek(0)
    size = int(file.readline().split()[0])
    matrix = AdjacencyMatrix(file)
    list = [[] for _ in range(size)]
    index = 0
    for k in range(size):
        nodesQtt = 0
        for i in range(size):
            temp = 0
            for j in range(size):
                if matrix[i][j] != 0:
                    temp += 1
            if temp == k:
                nodesQtt += 1
        frequency = nodesQtt / size
        if frequency != 0:
            list[index].append(k)
            list[index].append(frequency)
            index += 1

    for key in range(len(list) - 1, -1, -1):
        if not list[key]:
            list.pop(key)

    return list
