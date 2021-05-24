#!/usr/bin/python3
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight', 'ratio', 'taken'])


class Node:
    def __init__(self, parent=None, number=0, value=0, weight=0, estimate=0):
        self.left = None
        self.right = None
        self.parent = parent
        self.value = value
        self.weight = weight
        self.estimate = estimate
        self.number = number

    def get_parent(self):
        return self.parent

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
        items.append(Item(i-1, int(parts[0]), int(parts[1]), float((float(parts[0]) / float(parts[1]))), 0))

    items1 = items[:]
    items1.sort(key=lambda x: x[3], reverse=True)

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

    root = Node()
    current = root
    current.estimate = estimate(0, capacity)
    current_taken = [0]*len(items)
    value = 0
    best_taken = [0]*len(items)
    while(True):
        #print(current.number, current_taken)
        if current.right is None:
            current.right = Node(current, current.number + 1, current.value + items1[current.number].value,
                                 current.weight + items1[current.number].weight, current.estimate)
            current_taken[current.number] = 1
            current = current.right

        elif current.left is None:
            current.left = Node(current, current.number + 1, current.value,
                                current.weight, current.value + estimate(current.number+1, capacity - current.weight))
            current_taken[current.number] = 0
            current = current.left
        else:
            if current.number == 0:
                break
            current = current.parent
            continue
        #print('number=', current.number, 'value=', current.value, 'weight=', current.weight, 'estimate=', current.estimate, current_taken)
        if current.weight > capacity:
            current = current.parent
            continue

        if current.number == item_count:
            if value < current.value:
                value = current.value
                best_taken = current_taken[:]
            current = current.parent
        else:
            if current.estimate <= value:
                current = current.parent
            else:
                pass
        #input('pass')

    taken = [0]*len(items)
    for i in range(0, len(best_taken)):
            if best_taken[i] == 1:
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