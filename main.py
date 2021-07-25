import sys

import matplotlib.pyplot as plt
import xlsxwriter

from GraphManipulation import BasicDimacs

file = BasicDimacs.Entry('as_graph.txt')

adjList = BasicDimacs.AdjacencyList(file)

# Matrix representation costs too much and can crash your computer
# adjMatrix = BasicDimacs.AdjacencyMatrix(file)

# mostGraded = BasicDimacs.MostGraded(file)
# leastGraded = BasicDimacs.LeastGraded(file)
# avarageGrade = BasicDimacs.AverageGrade(file)
# relativeFrequency = BasicDimacs.RelativeFrequency(adjList)

BasicDimacs.BreadthFirstSearch(adjList, 1)

BasicDimacs.DepthFirstSearch(adjList, 1)

# relatedComponents = BasicDimacs.RelatedComponents(adjList)

file.close()
