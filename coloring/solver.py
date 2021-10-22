#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import defaultdict


class Graph:
    def __init__(self, n, m, nodes):
        self.n = n
        self.m = m
        self.nodes = nodes

    def check(self, node, color):
        for v in node.neighbours:
            if self.nodes[v].color == color:
                return False
        #degree = number of not painted vertices
        for v in node.neighbours:
            self.nodes[v].degree -= 1
        return True

    def get_solution(self):
        solution = [v.color for v in self.nodes]
        return max(solution) + 1, solution


class Node:
    def __init__(self, name, neighbours):
        self.name = name
        self.neighbours = neighbours
        self.degree = len(neighbours)
        self.color = -1
        

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    #element = set of neighbours of vertex
    edges = defaultdict(set)
    #adding neighbors into the sets according to the edge
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges[int(parts[0])].add(int(parts[1]))
        edges[int(parts[1])].add(int(parts[0]))

    '''algorithm: сортируем по убыванию степени (а степень - это количество неокрашенных соседей),
    первую вершину красим в 0 цвет (если она не окрашена уже) и по ходу массива окрашиваем в 0 цвет все неокрашенные
    и несмежные с ней вершины. Сортируем еще раз по степени, увеличиваем цвет и повторяем процедуру'''

    nodes = []
    for v in edges:
        nodes.append(Node(v, edges[v]))

    graph = Graph(node_count, edge_count, sorted(nodes, key=lambda v: v.name))

    sorted_nodes = sorted(nodes, key=lambda v : v.degree, reverse=True)

    color = 0
    stop = 1
    while stop > 0:
        stop = 0
        for node in sorted_nodes:
            if node.color == -1:
                if graph.check(node, color):
                    node.color = color
                    stop += 1
        color += 1
        sorted_nodes = sorted(nodes, key=lambda v: v.degree, reverse=True)

    solution = graph.get_solution()

    # prepare the solution in the specified output format
    output_data = str(solution[0]) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution[1]))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')
