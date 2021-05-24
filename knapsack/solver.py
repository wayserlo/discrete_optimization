#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight', 'ratio'])
class Node:
    def __init__(self):
        self.number = 0
        self.estimate = 0
        self.value = 0
        self.rest_capacity = 0
        self.taken = []
    def __str__(self):
        return f"Я узел под номером {self.number} с оценкой {self.estimate} и ценностью {self.value}, осталось места {self.rest_capacity}"

class Best:
    def __init__(self):
        self.value = 0
        self.taken = []
    def __str__(self):
        return f"Best value {self.value}, беру {self.taken}"

def solve_it(input_data):
# Modify this code to run your optimization algorithm

# parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1]), float((float(parts[0]) / float(parts[1])))))

    items1 = items[:]
    items1.sort(key=lambda x: x[3], reverse=True)
    print(items1)
    """
    max_estimate = 0
    for item in items1:
        max_estimate += item.value"""
    def estimate(k, capacity):
        weight1 = 0
        estimate1 = 0
        for j in range(k, item_count):
            if weight1 + items1[j].weight <= capacity:
                estimate1 += items1[j].value
                weight1 += items1[j].weight
            else:
                estimate1 += (float(items1[j].value) * float(capacity - weight1)) / float(items1[j].weight)
                break
        return estimate1

    def DFS(node, best, left):
        print(node)
        print(best)
        if node.number >= item_count:
            if node.value >= best.value:
                best.value = node.value
                best.taken = node.taken[:]
        else:
            if left == 1:
                if node.rest_capacity - items1[node.number].weight >= 0:
                    node.value += items1[node.number].value
                    node.taken[node.number] = 1
                    node.rest_capacity -= items1[node.number].weight
                    node.number += 1
                    best1 = DFS(node, best, 1)
                    best2 = DFS(node, best, 0)
                    if max(best1.value, best2.value) > best.value:
                        if best1.value >= best2.value:
                            best.value = best1.value
                            best.taken = best1.taken[:]
                        else:
                            best.value = best2.value
                            best.taken = best2.taken[:]
                else:
                    best = DFS(node, best, 0)
            else:
                if node.value + estimate(node.number + 1, node.rest_capacity) >= best.value:
                    node.estimate = node.value + estimate(node.number + 1, node.rest_capacity)
                    node.number += 1
                    best1 = DFS(node, best, 1)
                    best2 = DFS(node, best, 0)
                    if max(best1.value, best2.value) >= best.value:
                        if best1.value >= best2.value:
                            best.value = best1.value
                            best.taken = best1.taken[:]
                        else:
                            best.value = best2.value
                            best.taken = best2.taken[:]
        return best

    root = Node()
    root.number = 0
    root.rest_capacity = capacity
    root.estimate = estimate(0, root.rest_capacity)
    root.taken = [0]*len(items1)
    print(estimate(3, 2))

    best0 = Best()
    best0.taken = [0] * len(items1)
    best0.value = 0

    best1 = DFS(root, best0, 1)
    best2 = DFS(root, best0, 0)
    taken = [0]*item_count

    if best1.value >= best2.value:
        value = best1.value
        for i in range(0, len(best1.taken)):
            if best1.taken[i] == 1:
                for item in items:
                    if item == items1[i]:
                        taken[item.index] = 1
    else:
        value = best2.value
        for i in range (0, len(best2.taken)):
            if best2.taken[i] == 1:
                for item in items:
                    if item == items1[i]:
                        taken[item.index] = 1


# prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file. Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')