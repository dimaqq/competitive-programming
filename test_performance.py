import pytest
import itertools
import subtree


def tuple_to_list(t):
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
    edges = tuple_to_list(t)
    rv = {i: set() for i in range(1, len(edges) + 2)}
    for i, k in edges:
        rv[i].add(k)
        rv[k].add(i)
    return rv


def tuple_to_text(t):
    edges = tuple_to_list(t)
    return "%s\n%s" % (len(edges) + 1, "\n".join(" ".join(map(str, e)) for e in edges))


def test_tuple_to_list():
    assert not tuple_to_list(())
    assert tuple_to_list(((), )) == [(1, 2)]
    assert tuple_to_list(((), ())) == [(1, 2), (1, 3)]


def test_tuple_to_text():
    assert tuple_to_text(((), ())) == "3\n1 2\n1 3"


def tentacle(n):
    rv = ()
    for i in range(n):
        rv = (rv, )
    return rv


def test_straight_yyy():
    import time
    for i in (11, 21, 31, 41, 51, 61):
        started = time.time()
        n = tuple_to_graph(tentacle(i))
        subtree.combinations(n)
        print(i, time.time() - started)


def test_straight_xxx():
    import time
    for i in (10, 20, 30, 40, 50, 60):
        started = time.time()
        n = tuple_to_graph(tentacle(i))
        subtree.combinations(n)
        print(i, time.time() - started)


def test_straight_1000(benchmark):
    # FIXME python stack limit is 1000, recursive build and diameter determination fail here
    n = tuple_to_graph(tentacle(100))
    benchmark(subtree.combinations, n)


def fixme_straight_999(benchmark):
    n = tuple_to_graph(tentacle(99))
    benchmark(subtree.combinations, n)
