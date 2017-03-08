# doc: git.io/vy4co
import sys
sys.setrecursionlimit(2300)  # for largest input 1000


def build_graph(inp):
    nodes = dict()
    N = None

    for line in inp:
        # special handling for first line of input -- seed vertices
        if N is None:
            N = int(line.strip())
            for k in range(1, N + 1):
                nodes[k] = set()
            continue

        # create edges
        i, k = map(int, line.split())
        nodes[i].add(k)
        nodes[k].add(i)

    return nodes


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
        return sum(enum(limits, tree) for limits in zip(range(C + 1), reversed(range(C + 1))))
    else:
        # longest path has even number of nodes, odd number of edges
        left = path[L // 2 - 1]
        # virtual tree (root->left->left's children)
        left_tree = tuplex([shape3(nodes, left, exclude=root)])
        # everything else (root->(children - left))
        right_tree = shape3(nodes, root, exclude=left)
        assert left_tree.height[1] == C
        assert right_tree.height[1] == C - 1
        lg = [i // 2 for i in range(1, C * 2 + 2)]
        ll = list(zip(lg, reversed(lg)))
        rg = [i // 2 for i in range(C * 2 + 1)]
        rl = list(zip(rg, reversed(rg)))
        tot = 0
        lrvs = dict()
        rrvs = dict()
        for i in range(len(ll)):
            left_limits = ll[i]
            right_limits = rl[i]
            if sum(left_limits) > C:
                neigh = ll[i - 1: i] + ll[i + 1: i + 2]
                lrv = lrvs[left_limits] = enum(left_limits, left_tree) - sum(enum(ne, left_tree) for ne in neigh)
            else:
                lrv = lrvs[left_limits] = enum(left_limits, left_tree)
            rrv = rrvs[right_limits] = enum(right_limits, right_tree)
            tot += lrv * rrv
        return tot


def virtual_tree(nodes, root, branch):
    """ virtual tree rooted at root, where root has only 1 branch, branch """
    return tuplex([shape3(nodes, branch, exclude=root)])


def enum(limits, shape, _cache=dict()):
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
    if (r, b, shape) not in _cache:
        tot = 1
        for subtree in shape:
            acc = 0
            for sublimit in ((r - 1, b), (r, b - 1)):
                x = enum(sublimit, subtree)
                acc += x
            tot *= acc
        _cache[(r, b, shape)] = tot
    return _cache[(r, b, shape)]
