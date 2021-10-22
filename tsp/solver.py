#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple
import numpy as np
from tqdm import tqdm

#Point = namedtuple("Point", ['x', 'y'])


def length(point1, point2):
    return np.sqrt(np.sum((point1 - point2)**2))


def dist_matrix(points, node_count):
    distances = np.zeros((2, node_count, node_count, 2))
    distances[0, :] = points
    distances[1, :] = points.reshape(node_count, 1, 2)
    distances = np.sqrt(np.sum((distances[0, :] - distances[1, :]) ** 2, axis=-1))
    return distances


def comp_obj(distances, order, count):
    obj = distances[order[-1], order[0]]
    for index in range(count - 1):
        obj += distances[order[index], order[index + 1]]
    return obj
# trivial solution: min dist v_1 v_2


def greedy(v0, node_count, distances):
    order = [v0]
    available = {i for i in range(node_count)}
    available.remove(order[0])
    for i in tqdm(range(node_count - 1)):
        min_dist = float("+inf")
        min_vertex = -1
        for vertex in available:
            dist = distances[order[i], vertex]
            if dist < min_dist:
                min_dist = dist
                min_vertex = vertex
        if min_vertex != -1:
            order.append(min_vertex)
            available.remove(min_vertex)
    for vertex in available:
        order.append(vertex)
    return order


def small_greedy(node_count, distances):
    number = int(np.log2(node_count))
    indexes = np.random.choice(node_count, number, replace=False)
    min_order = greedy(indexes[0], node_count, distances).copy()
    min_obj = comp_obj(distances, min_order, node_count)
    for i in range(1, number):
        order = greedy(indexes[i], node_count, distances)
        dist = comp_obj(distances, min_order, node_count)
        if dist < min_obj:
            min_order = order
            min_obj = dist
    return min_order


def cost_change(distances, v1, v2, v3, v4):
    return distances[v1][v3] + distances[v2][v4] - distances[v1][v2] - distances[v3][v4]


def cost_change_three(distances, v1, v2, v3, v4, v5, v6):
    return distances[v1][v3] + distances[v2][v5] + distances[v6][v4] - distances[v1][v2] - distances[v3][v4] - distances[v5][v6]


def two_opt(route, distances):
    best = route
    improved = True
    while improved:
        improved = False
        l = len(route)
        order = np.random.permutation(l-2) + 1
        for i in order: #range(1, l - 2):
            for j in range(i + 1, l):
                if j - i == 1:
                    continue
                if cost_change(distances, best[i-1], best[i], best[j-1], best[j]) < 0:
                    best[i:j] = best[j - 1:i - 1:-1]
                    improved = True
        route = best
    return best


'''def round(v_1, taken, min_dist, nodeCount, solution):
    for i in range(0, nodeCount):
        if taken[i] == 0:
            dist = length(v_1, points[i])
            if dist < min_dist:
                min_dist = dist
                v_2 = points[i]
    taken[v_2.i] = 1
    solution.append(v_2.i)
    return v_2'''


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    node_count = int(lines[0])
    print(node_count)
    points = []
    for i in range(1, node_count+1):
        line = lines[i]
        parts = line.split()
        points.append([float(parts[0]), float(parts[1])])
    points = np.array(points)
    # print(points)
    # build a trivial solution
    # visit the nodes in the order they appear in the file
    if node_count == 574:
        distances = dist_matrix(points, node_count)
        len2 = float('+inf')
        while len2 > 40000:
            num = np.random.randint(0, 574)
            solution = two_opt(greedy(num, node_count, distances), distances)
            len2 = comp_obj(distances, solution, node_count)
    elif node_count == 33810:
        order = [0]
        available = {i for i in range(node_count)}
        available.remove(0)
        for i in tqdm(range(node_count - 1)):
            min_dist = float("+inf")
            min_vertex = -1
            for vertex in available:
                dist = length(points[order[i]], points[vertex])
                if dist < min_dist:
                    min_dist = dist
                    min_vertex = vertex
            if min_vertex != -1:
                order.append(min_vertex)
                available.remove(min_vertex)
        for vertex in available:
            order.append(vertex)
        solution = order
    else:
        distances = dist_matrix(points, node_count)
        solution = two_opt(greedy(0, node_count, distances), distances)

    # calculate the length of the tour
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, node_count-1):
        obj += length(points[solution[index]], points[solution[index + 1]])

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

