# doc: git.io/vy4co
import sys
sys.setrecursionlimit(2300)  # for largest input 1000


def graph(inp):
    """ Given text representation of input, compute graph:
        Graph is a dictionary of nodes (name -> node)
        Node is a set of edges (-> other node name)
    """
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


def trace_from(nodes, start, exclude=None):
    """ Given a starting point, find longest trace through the tree/graph """
    traces = [trace_from(nodes, n, exclude=start) for n in nodes[start] if n is not exclude]
    return (start,) + max(traces, key=len, default=())


def diameter(nodes):
    """ Find a longest path in the graph:
        Start with a random node, and find a longest trace from it.
        Re-start from the end of that trace and find a lognest trace.
        This will be the longest path in a graph, if graph is a tree. """
    start = next(iter(nodes))
    restart = trace_from(nodes, start)[-1]
    return trace_from(nodes, restart)


def tree(nodes, start, exclude=None):
    """ Recreate a tree as tuple of tuple of ... """
    return tup([tree(nodes, n, exclude=start) for n in nodes[start] if n is not exclude])


class tup(tuple):
    """ Tree as a tuple of tuples of tuples of ...  For example, o->o->o becomes (((), ), )
        Data structure is immutable, thus trees can be referred to by Python builtin hash
    """
    def __new__(cls, arg=()):
        # `sorted(arg)` can be used below, as order of subtrees is irrelevant
        # sorting subtrees makes partial result cache smaller,
        # however extra processing proved a larger factor than cache size
        rv = super().__new__(cls, arg)
        rv.height = (1 + min((t.height[0] for t in rv), default=-1),
                     1 + max((t.height[1] for t in rv), default=-1))
        rv.edges = len(rv) + sum(t.edges for t in rv)
        return rv


def combinations(nodes):
    """ Count up possible arrow combinations for a graph, see README.md """
    path = diameter(nodes)
    D = len(path)
    C = D // 2
    root = path[D // 2]  # left side is longest (or equal)
    if D % 2:
        # longest path has odd number of nodes, thus even number of edges
        # thus "left" and "right" sides are equal length, and C == D / 2
        # this places strict constraints on coloring longest branches:
        # these are length C and color uptions sum up to C
        thetree = tree(nodes, root)
        return sum(enum(limits, thetree) for limits in zip(range(C + 1), reversed(range(C + 1))))
    else:
        # longest path has even number of nodes, odd number of edges
        # thus, C == (D + 1) / 2
        # this allows more possibilities when coloring branches:
        # e.g. left branch length C, color options C; right branch length C-1, color options C
        # or left branch length C, color opionts C+1; right branch length C-1, color options C-1
        left = path[D // 2 - 1]
        # left branch as a virtual tree (root->left->left's children)
        left_tree = tup([tree(nodes, left, exclude=root)])
        # all right branches (root->(children - left))
        right_tree = tree(nodes, root, exclude=left)

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
            # See README.md for explanation
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
    return tup([tree(nodes, branch, exclude=root)])


def enum(limits, shape, _cache=dict()):
    """ Enumerate possible unique colorings within limits (red, blue) for a tree of given shape """
    limits = tuple(sorted(limits))  # doesn't matter which is red or blue
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
    key = hash((r, b, shape))
    if key not in _cache:
        tot = 1
        for subtree in shape:
            acc = 0
            for sublimit in ((r - 1, b), (r, b - 1)):
                acc += enum(sublimit, subtree)
            tot *= acc
        _cache[key] = tot
    return _cache[key]
