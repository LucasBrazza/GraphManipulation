def NearestNeighbour(adjList):
    u = (0, 0.0)
    path = [u]
    nVisitados = [i for i in range(len(adjList))]
    nVisitados.pop(0)
    lesserNode = None

    while nVisitados:
        pesoMenor = float('inf')
        for node in adjList[u[0]]:
            if node[0] in nVisitados:
                pesoAtual = node[1]
                if pesoMenor > pesoAtual:
                    pesoMenor = pesoAtual
                    lesserNode = node[0]

        path.append((lesserNode, pesoMenor))
        nVisitados.remove(lesserNode)
        u = (lesserNode, pesoMenor)

    path.append(adjList[lesserNode][0])
    return path


def diferenceCost(zdjList, a, b, c, d):
    print('aaaaaaaaaaaa')
    print(zdjList[a][c-1][1])
    print(zdjList[b][d-1][1])
    print(zdjList[a][b-1][1])
    print(zdjList[c][d-1][1])
    result = (zdjList[a][c-1][1] + zdjList[b][d-1][1]) - (zdjList[a][b-1][1] + zdjList[c][d-1][1])
    return result


def twoOpt(path, adjList):
    best = path
    improved = True
    while improved:
        improved = False
        for i in range(1, len(path) - 2):

            for j in range(i + 1, len(path)):
                if j - i == 1:
                    continue

                a = best[i - 1][0]
                b = best[i][0]
                c = best[j - 1][0]
                d = best[j][0]
                if diferenceCost(adjList, a, b, c, d) < 0:
                    best[i:j] = best[j - 1: i - 1: -1]
                    # print(i, j)
                    # print('bbbbbbbbb', best[i-1][1])
                    # print('bbbbbbbbb', adjList[i-2])
                    # best[i-1][1] = adjList[i-2][i-1][1]
                    improved = True

        path = best
    return best
