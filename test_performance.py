import pytest
import itertools
import subtree


def tuple_to_list(t):
    """ Helper to rebuild input representation from tuple tree
        Output as an array of edges """
    names = itertools.count(1)
    edges = list()

    def rec(this, name):
        for sub in this:
            n = next(names)
            edges.append((name, n))
            rec(sub, n)

    rec(t, next(names))
    return edges


def tuple_to_graph(t):
    """ Outout as a dictionary or sets """
    edges = tuple_to_list(t)
    rv = {i: set() for i in range(1, len(edges) + 2)}
    for i, k in edges:
        rv[i].add(k)
        rv[k].add(i)
    return rv


def tuple_to_text(t):
    """ Output text that can be fed to stdin """
    edges = tuple_to_list(t)
    return "%s\n%s" % (len(edges) + 1, "\n".join(" ".join(map(str, e)) for e in edges))


def test_tuple_to_list():
    assert not tuple_to_list(())
    assert tuple_to_list(((), )) == [(1, 2)]
    assert tuple_to_list(((), ())) == [(1, 2), (1, 3)]


def test_tuple_to_text():
    assert tuple_to_text(((), ())) == "3\n1 2\n1 3"


def tentacle(n):
    """ narrow branch / finger """
    rv = ()
    for i in range(n):
        rv = (rv, )
    return rv


def haircomb(n, k):
    """Total ~n edges: long main spine, with k-length ribs protruding from each vertebrae"""
    rv = ()
    for i in range(n // (k + 1)):
        rv = (rv, tentacle(k))
    return rv


def test_straight_1000(benchmark):
    n = tuple_to_graph(tentacle(100))
    benchmark(subtree.combinations, n)


def test_straight_999(benchmark):
    n = tuple_to_graph(tentacle(99))
    benchmark(subtree.combinations, n)


def test_short_haircomb_1000(benchmark):
    n = tuple_to_graph(haircomb(1000, 1))
    benchmark(subtree.combinations, n)


def test_short_haircomb_1001(benchmark):
    n = tuple_to_graph(haircomb(1001, 1))
    benchmark(subtree.combinations, n)


def test_med_haircomb_1000(benchmark):
    n = tuple_to_graph(haircomb(1000, 5))
    benchmark(subtree.combinations, n)


def test_long_haircomb_1000(benchmark):
    n = tuple_to_graph(haircomb(1000, 30))
    benchmark(subtree.combinations, n)


def test_hub4(benchmark):
    """ Wheel hub with 4 long spokes """
    spoke = tentacle(250)
    t = (spoke, spoke, spoke, spoke)
    n = tuple_to_graph(t)
    benchmark(subtree.combinations, n)


def test_hub4_uneven(benchmark):
    """ Wheel hub with 4 long spokes, where one is longer than others """
    spoke = tentacle(250)
    t = (spoke, spoke, spoke, tentacle(251))
    n = tuple_to_graph(t)
    benchmark(subtree.combinations, n)


def unique_trees():
    """ A random tree composed of unique subtrees, total weight ~1000 """
    import random
    basics = [tentacle(i) for i in range(10)]
    level2 = []
    for i, b in enumerate(basics):
        for bb in basics[i:]:
            level2.append((b, bb))
    level3 = {tuple(random.sample(level2, 5)) for i in range(20)}
    return tuple(random.sample(level3, 17))


def test_unique_trees(benchmark):
    t = unique_trees()
    n = tuple_to_graph(t)
    benchmark(subtree.combinations, n)


def test_unique_trees_long(benchmark):
    t = (unique_trees(), tentacle(20), tentacle(21))
    n = tuple_to_graph(t)
    benchmark(subtree.combinations, n)
