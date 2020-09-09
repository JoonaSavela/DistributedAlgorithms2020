import numpy as np

def print_nodes(nodes):
    print(' - '.join([str(n) for n in nodes]))

def get_neighbours(nodes, i, stopped = None):
    if stopped is None:
        neigh = []
        if i > 0:
            neigh.append(nodes[i - 1])
        if i < len(nodes) - 1:
            neigh.append(nodes[i + 1])

        return np.array(neigh)
    else:
        neigh = []
        stopp = []
        if i > 0:
            neigh.append(nodes[i - 1])
            stopp.append(stopped[i - 1])
        if i < len(nodes) - 1:
            neigh.append(nodes[i + 1])
            stopp.append(stopped[i + 1])

        return np.array(neigh), np.array(stopp).astype(np.bool)

def get_node_and_neighbors(nodes, as_index = False, stopped = None):
    if stopped is None:
        if as_index:
            return [(i, get_neighbours(nodes, i)) for i in range(len(nodes))]
        return [(nodes[i], get_neighbours(nodes, i)) for i in range(len(nodes))]
    else:
        if as_index:
            return [(i, ) + get_neighbours(nodes, i, stopped) for i in range(len(nodes))]
        return [(nodes[i], ) + get_neighbours(nodes, i, stopped) for i in range(len(nodes))]


def is_valid(nodes):
    node_and_neigh = get_node_and_neighbors(nodes)
    return all([(n == 1 and 1 not in neigh) or (n == 0 and 1 in neigh) for n, neigh in node_and_neigh])

def test(algo_fn):
    np.random.seed(0)

    for i in range(3):
        nodes = np.unique(np.random.randint(0, 10, size = 6))
        np.random.shuffle(nodes)
        nodes = np.append(nodes, 0)
        print_nodes(nodes)
        nodes = algo_fn(nodes)
        print_nodes(nodes)
        print(is_valid(nodes))
        print()

    for i in range(100):
        nodes = np.unique(np.random.randint(0, 2 ** 32, size = 100))
        np.random.shuffle(nodes)
        nodes = np.append(nodes, 0)
        nodes = algo_fn(nodes)
        if not is_valid(nodes):
            print(i)
            return

    print("All tests passed")

def test2(algo_fn):
    np.random.seed(0)

    for i in range(3):
        nodes = np.unique(np.random.randint(0, 256, size = 6))
        np.random.shuffle(nodes)
        nodes = np.append(nodes, 0)
        print_nodes(nodes)
        nodes = algo_fn(nodes)
        print_nodes(nodes)
        print(is_valid(nodes))
        print()

    for i in range(100):
        nodes = np.unique(np.random.randint(0, 2 ** 32, size = 100))
        np.random.shuffle(nodes)
        nodes = np.append(nodes, 0)
        nodes = algo_fn(nodes)
        if not is_valid(nodes):
            print(i)
            return

    print("All tests passed")



def algorithm1(nodes):
    def _inner(nodes):
        node_and_neigh = get_node_and_neighbors(nodes, True)
        for i, neigh in node_and_neigh:
            if (nodes[i] > neigh.max() and 1 not in neigh):
                nodes[i] = 1
            elif 1 in neigh:
                nodes[i] = 0
            elif np.all(neigh == 0):
                nodes[i] = 1

    while np.any(nodes > 1):
        _inner(nodes)
        # print_nodes(nodes)

    _inner(nodes)

    return nodes


x = 128

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

def get_succcessor(nodes, i):
    if i < len(nodes) - 1:
        succ = nodes[i + 1]
    else:
        succ = nodes[i] + 1

    return succ

def get_node_and_succcessor(nodes, as_index = False):
    if as_index:
        return [(i, get_succcessor(nodes, i)) for i in range(len(nodes))]
    return [(nodes[i], get_succcessor(nodes, i)) for i in range(len(nodes))]

def algorithm2(nodes):
    def _inner(nodes):
        node_and_succ = get_node_and_succcessor(nodes, True)
        for n_i, succ in node_and_succ:
            i = get_differing_index(nodes[n_i], succ)
            nodes[n_i] = 2 * i + get_bit_at_i(nodes[n_i], i)

    def _inner2(nodes):
        node_and_neigh = get_node_and_neighbors(nodes, True)
        for i, neigh in node_and_neigh:
            if (nodes[i] > neigh.max() and 1 not in neigh):
                nodes[i] = 1
            elif 1 in neigh:
                nodes[i] = 0
            elif np.all(neigh == 0):
                nodes[i] = 1

    for i in range(4):
        _inner(nodes)
        # print_nodes(nodes)

    for i in range(4):
        _inner2(nodes)
        # print_nodes(nodes)

    return nodes


def algorithm3(nodes):
    stopped = np.zeros((len(nodes),)).astype(np.bool)

    def _inner(nodes, stopped):
        node_and_neigh = get_node_and_neighbors(nodes, True, stopped)
        for i, neigh, stopp in node_and_neigh:
            if (nodes[i] == 1 and np.all(neigh == 0)) or \
                    (nodes[i] == 0 and any([neigh[j] == 1 and stopp[j] for j in range(len(neigh))])):
                stopped[i] = True
            if not stopped[i]:
                nodes[i] = np.random.randint(0, 2)

    count = 0
    while not np.all(stopped):
        _inner(nodes, stopped)
        count += 1
        # print_nodes(nodes)
    print(count)

    return nodes

test2(algorithm3)
