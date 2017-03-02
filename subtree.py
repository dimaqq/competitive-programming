from operator import mul
from functools import reduce


def build_graph(inp):
    nodes = dict()
    names = dict()
    N = None

    for line in inp:
        # special handling for first line of input -- seed vertices
        if N is None:
            N = int(line.strip())
            for k in range(1, N + 1):
                nodes[k] = set()
                names[id(nodes[k])] = nodes[k]
            continue

        # create edges
        i, k = map(int, line.split())
        nodes[i].add(k)
        nodes[k].add(i)

    return nodes, names


def longest_trace_from(nodes, start, exclude=None):
    traces = [longest_trace_from(nodes, n, exclude=start) for n in nodes[start] if n is not exclude] + [()]
    return (start,) + max(traces, key=len)


def longest_path(nodes):
    """ Find a longest path in the graph:
        Start with a random node, and find a longest trace from it.
        Re-start from the end of that trace and find a lognest trace.
        This will be the longest path in a graph, if graph is a tree. """
    if not nodes:
        return ()
    random = next(iter(nodes))
    start = longest_trace_from(nodes, random)[-1]
    return longest_trace_from(nodes, start)


def shape3(nodes, start, exclude=None):
    parts = [shape3(nodes, n, exclude=start) for n in nodes[start] if n is not exclude]
    return tuplex(parts)


class tuplex(tuple):
    def __new__(cls, arg=()):
        rv = super().__new__(cls, arg)
        # rv = super().__new__(cls, sorted(arg))
        rv.height = (1 + min((t.height[0] for t in rv), default=-1),
                     1 + max((t.height[1] for t in rv), default=-1))
        rv.edges = len(rv) + sum(t.edges for t in rv)
        return rv


def combinations(nodes):
    path = longest_path(nodes)
    L = len(path)
    C = L // 2
    root = path[L // 2]  # left side is longest (or equal)
    if L % 2:
        # longest path has odd number of nodes, thus even number of edges
        tree = shape3(nodes, root)
        for limits in zip(range(C + 1), reversed(range(C + 1))):
            print(limits, tree, enum(limits, tree))
        return sum(enum(limits, tree) for limits in zip(range(C + 1), reversed(range(C + 1))))
    else:
        # longest path has even number of nodes, odd number of edges
        neigh = nodes[root]  # mid-point's neighbours
        left = path[L // 2 - 1]
        # virtual tree (root->left->left's children)
        left_tree = tuplex([shape3(nodes, left, exclude=root)])
        # everything else (root->(children - left))
        right_tree = shape3(nodes, root, exclude=left)
        assert left_tree.height[1] == C
        assert right_tree.height[1] == C - 1


def virtual_tree(nodes, root, branch):
    """ virtual tree rooted at root, where root has only 1 branch, branch """
    return tuplex([shape3(nodes, branch, exclude=root)])


def logged(f):
    def inner(l, s):
        import copy
        rv = f(l, s)
        print(l, s, "=>", rv)
        return rv
    return inner


@logged
def enum(limits, shape):
    limits = tuple(sorted(limits))  # doesn't matter which is red or bla
    r, b = limits
    low, high = shape.height
    assert low <= high
    assert r + b >= high
    assert r <= b

    if r >= high:
        return 2 ** shape.edges  # any combination is possible

    if 0 in limits:
        return 1  # only one color allowed

    assert r
    assert b
    assert shape
    tot = 1
    print("XXstart", hash(shape), limits)
    for subtree in shape:
        print("XXtrying subtree", hash(shape), subtree)
        acc = 0
        for sublimit in ((r - 1, b), (r, b - 1)):
            print("XXtrying sublimit", hash(shape), sublimit)
            x = enum(sublimit, subtree)
            print("XXtrying sublimit", hash(shape), sublimit, "=>", x)
            acc += x
        print("XXtrying subtree", hash(shape), subtree, "=>", acc)
        tot *= acc
    print("XXstart", hash(shape), limits, "=>", tot)
    return tot

    rv = sum(reduce(mul, (enum(sublimit, subtree) for subtree in shape)) for sublimit in ((r - 1, b), (r, b - 1)))

    rv = sum(reduce(mul, (enum(sublimit, subtree) for subtree in shape)) for sublimit in ((r - 1, b), (r, b - 1)))
    return rv


import pytest
import pprint


def test_enum_simple():
    # chain
    assert enum((9, 9), tuplex()) == 1
    assert enum((9, 9), tuplex([tuplex()])) == 2
    assert enum((9, 9), tuplex([tuplex([tuplex()])])) == 4
    assert enum((9, 9), tuplex([tuplex([tuplex([tuplex()])])])) == 8

    # star
    assert enum((9, 9), tuplex([tuplex()])) == 2
    assert enum((9, 9), tuplex([tuplex(), tuplex()])) == 4
    assert enum((9, 9), tuplex([tuplex(), tuplex(), tuplex()])) == 8

    three = tuplex([tuplex([tuplex([tuplex()])])])  # 3 edges, 4 nodes
    assert enum((0, 3), three) == 1
    assert enum((1, 2), three) == 3

    four = tuplex([tuplex([tuplex([tuplex([tuplex()])])])])  # 4 edges, 5 nodes
    assert enum((2, 2), four) == 6

    six = tuplex([tuplex([tuplex([tuplex([tuplex([tuplex([tuplex()])])])])])])  # 6 edges
    assert enum((3, 3), six) == 20


def test_enum_simple_v():
    vthree = tuplex([tuplex([tuplex([tuplex()])]),
                     tuplex([tuplex([tuplex()])])])  # 6 edges
    # assert enum((0, 3), vthree) == 1
    # assert enum((3, 0), vthree) == 1
    print("start")
    assert enum((1, 2), vthree) == 9
    # assert enum((2, 1), vthree) == 9


def test_enum_simple_w():
    wthree = tuplex([tuplex([tuplex([tuplex()])]),
                     tuplex([tuplex([tuplex()])]),
                     tuplex([tuplex([tuplex()])])])  # 6 edges
    # assert enum((0, 3), vthree) == 1
    # assert enum((3, 0), vthree) == 1
    print("start")
    assert enum((1, 2), wthree) == 27
    # assert enum((2, 1), vthree) == 9


def test_enum(leaf_shape, I_shape, Y_shape):
    assert enum((0, 0), leaf_shape) == 1
    assert enum((0, 1), leaf_shape) == 1
    assert enum((9, 9), leaf_shape) == 1

    with pytest.raises(AssertionError):
        enum((0, 0), I_shape)

    assert enum((0, 1), I_shape) == 1
    assert enum((1, 0), I_shape) == 1
    assert enum((2, 0), I_shape) == 1
    assert enum((1, 1), I_shape) == 2
    assert enum((9, 9), I_shape) == 2

    assert enum((2, 0), Y_shape) == 1
    assert enum((0, 2), Y_shape) == 1
    assert enum((1, 1), Y_shape) == 2
    assert enum((2, 1), Y_shape) == 5
    assert enum((1, 2), Y_shape) == 5
    assert enum((2, 2), Y_shape) == 8
    assert enum((3, 3), Y_shape) == 8


def test_enum_tiered(leaf_shape, I_shape, Y_shape):
    t = tuplex([I_shape, Y_shape])

    with pytest.raises(AssertionError):
        enum((2, 0), t)

    with pytest.raises(AssertionError):
        enum((1, 1), t)

    assert enum((3, 0), t) == 1
    assert enum((3, 3), t) == 2 ** 6
    assert enum((2, 1), t) == 5
    

@pytest.fixture
def leaf_shape():
    return tuplex()


@pytest.fixture
def I_shape():
    return tuplex([tuplex()])


@pytest.fixture
def Y_shape():
    return tuplex([tuplex([tuplex(), tuplex()])])


def test_enumerate(leaf_shape, I_shape, Y_shape):
    assert enum((1, 1), leaf_shape) == 1
    assert enum((4, 4), leaf_shape) == 1

    # assert not enum(-1, 1, leaf_shape)
    # assert not enum(1, -1, leaf_shape)

    assert enum((4, 4), I_shape) == 2



@pytest.fixture
def sample_data1():
    data = """4
              1 2
              1 3
              1 4""".strip().splitlines()
    return build_graph(data)


@pytest.fixture
def nodes(sample_data1):
    nodes, name = sample_data1
    return nodes


@pytest.fixture
def nodes2():
    nodes, names = build_graph("""4
                                  1 2
                                  2 3
                                  3 4""".strip().splitlines())
    return nodes


@pytest.fixture
def nodes3():
    nodes, names = build_graph("""6
                                  1 2
                                  1 3
                                  1 4
                                  2 5
                                  2 6""".strip().splitlines())
    return nodes


@pytest.fixture
def nodes4():
    nodes, names = build_graph("""10
                                  2 4
                                  2 5
                                  8 3
                                  10 7
                                  1 6
                                  2 8
                                  9 5
                                  8 6
                                  10 6""".strip().splitlines())
    return nodes


@pytest.fixture
def six_in_line():
    """ 1 line, 6 edges (7 nodes) """
    nodes, names = build_graph("""7
                                  1 2
                                  2 3
                                  3 4
                                  4 5
                                  5 6
                                  6 7""".strip().splitlines())
    return nodes


def test_com_lines(six_in_line):
    assert combinations(six_in_line) == 6 * 5 * 4


def test_com(nodes, nodes2, nodes3, nodes4):
    combinations(nodes) == 2
    combinations(nodes2) == 6
    combinations(nodes3) == 14
    combinations(nodes4) == 102
    assert combinations(nodes) == 2
    # assert combinations(nodes2) == 6
    # assert combinations(nodes3) == 14
    assert combinations(nodes4) == 102


def test_build(nodes):
    # print(nodes)  # visual inspection
    pass


def test_ltf(nodes):
    assert len(longest_trace_from(nodes, 1)) == 2  # e.g. (1, 2)
    assert len(longest_trace_from(nodes, 2)) == 3  # e.g. (2, 1, 3)


def test_lp(nodes):
    assert len(longest_path(nodes)) == 3  # e.g. (2, 1, 3)


# def test_shape3(nodes):
#     assert shape3(nodes, 3, exclude=1) == ()  # 3 is leaf
#     assert shape3(nodes, 1, exclude=3) == ((), ())  # 1 has two leaf childred (2, 4); 3 is excluded
#     tt = shape3(nodes, 1, exclude=3)
#     assert tt.height == 1
#     assert not tt[0].height
#     assert not tt[1].height


def test_tuplex_height():
    rv = \
        tuplex([
            tuplex([
                tuplex(),
                tuplex()]),
            tuplex()])
    assert rv[0][1].height == (0, 0)
    assert rv[0].height == (1, 1)
    assert rv[1].height == (0, 0)
    assert rv.height == (1, 2)

    rv2 = tuplex([tuplex(), rv])
    assert rv2.height == (1, 3)

    rv3 = tuplex([rv, rv2, rv2, rv])
    assert rv3.height == (2, 4)


def test_tuplex_edges(leaf_shape, I_shape, Y_shape):
    assert not leaf_shape.edges
    assert I_shape.edges == 1
    assert Y_shape.edges == 3
# 
# 
# def subtree_limits(path):
#     L = len(path)
#     excl = [frozenset(path[:i][-1:] + path[i + 1:][:1]) for i in range(L)]
#     high = [min(i, L - i - 1) for i in range(L)]
#     lims = [tuple((H - i, i) for i in range(H // 2 + 1)) for H in high]
#     return tuple(dict(start=path[i], exclude=excl[i], limits=lims[i]) for i in range(L))
