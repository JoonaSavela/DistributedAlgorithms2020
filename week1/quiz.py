import random


x = 32

def get_xbit_bin_color(color):
    res = bin(color)[2:]
    res = "0" * (x - len(res)) + res
    return res

def get_differing_index(c1, c2):
    xor_color = c1 ^ c2
    xor_color = get_xbit_bin_color(xor_color)
    return x - 1 - max([i for i in range(x) if xor_color[i] == "1"])

def get_bit_at_i(color, i):
    return int(get_xbit_bin_color(color)[-(i + 1)])

def is_valid(nodes):
    return all([nodes[i].color != nodes[i + 1].color for i in range(len(nodes) - 1)])

class Node(object):
    """docstring for Node."""

    def __init__(self, successor, color):
        super(Node, self).__init__()
        self.successor = successor
        self.color = color
        self.successor_color = None
        self.stopped = False

    def get_successor_color(self):
        if self.successor is None:
            self.successor_color = random.randint(0, 2 ** x - 1)
            while self.color == self.successor_color:
                self.successor_color = random.randint(0, 2 ** x - 1)
        else:
            self.successor_color = self.successor.color

    def update_color(self):
        if self.stopped:
            return
        i = get_differing_index(self.color, self.successor_color)
        # print(i, get_bit_at_i(self.color, i))
        self.color = 2 * i + get_bit_at_i(self.color, i)
        if self.color <= 3:
            self.stopped = True


node3 = Node(None, 274)
node2 = Node(node3, 530)
node1 = Node(node2, 34)

nodes = [node1, node2, node3]

while not is_valid(nodes):
    print('unlikely')
    node3 = Node(None, random.randint(0, 2 ** x - 1))
    node2 = Node(node3, random.randint(0, 2 ** x - 1))
    node1 = Node(node2, random.randint(0, 2 ** x - 1))

    nodes = [node1, node2, node3]

for node in nodes:
    print(node.color)

for i in range(2):
    for node in nodes:
        node.get_successor_color()
    for node in nodes:
        node.update_color()
    print(is_valid(nodes))
    for node in nodes:
        print(node.color)

# while not all([node.stopped for node in nodes]):
#     for node in nodes:
#         node.get_successor_color()
#     for node in nodes:
#         node.update_color()
#     for node in nodes:
#         print(node.color)

print()
print(is_valid(nodes), nodes[0].color, all([node.stopped for node in nodes]))
