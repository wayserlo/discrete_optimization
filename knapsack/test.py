
"""from collections import namedtuple
Item = namedtuple("Item", ['index', 'ratio', 'div'])

Items = [Item(0, 10, 1/2), Item(1, 20, 1/6), Item(2, 1, 1/9), Item(3, 0, 1/45), Item(4, 40, 1/99)]

Items.sort(key=lambda x: x[1])
copy1 = Items[:]
Items.sort(key=lambda x: x[0], reverse=True)
copy2 = Items[:]

print(copy1, '\n')
print(copy2, '\n')"""
a = 5
b = a
a = 20
print(a, b)
