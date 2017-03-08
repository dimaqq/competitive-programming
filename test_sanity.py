import pytest
from test_inputs import nodes, sample_data1
from subtree import tup, enum, shape3, build_graph, longest_trace_from, longest_path, combinations


def test_enum_simple():
    # chain
    assert enum((9, 9), tup()) == 1
    assert enum((9, 9), tup([tup()])) == 2
    assert enum((9, 9), tup([tup([tup()])])) == 4
    assert enum((9, 9), tup([tup([tup([tup()])])])) == 8

    # star
    assert enum((9, 9), tup([tup()])) == 2
    assert enum((9, 9), tup([tup(), tup()])) == 4
    assert enum((9, 9), tup([tup(), tup(), tup()])) == 8

    three = tup([tup([tup([tup()])])])  # 3 edges, 4 nodes
    assert enum((0, 3), three) == 1
    assert enum((1, 2), three) == 3

    four = tup([tup([tup([tup([tup()])])])])  # 4 edges, 5 nodes
    assert enum((2, 2), four) == 6

    six = tup([tup([tup([tup([tup([tup([tup()])])])])])])  # 6 edges
    assert enum((3, 3), six) == 20


def test_enum_simple_v():
    vthree = tup([tup([tup([tup()])]),
                     tup([tup([tup()])])])  # 6 edges
    assert enum((0, 3), vthree) == 1
    assert enum((3, 0), vthree) == 1
    assert enum((1, 2), vthree) == 9
    assert enum((2, 1), vthree) == 9


def test_enum_simple_w():
    wthree = tup([tup([tup([tup()])]),
                     tup([tup([tup()])]),
                     tup([tup([tup()])])])  # 6 edges
    assert enum((0, 3), wthree) == 1
    assert enum((3, 0), wthree) == 1
    assert enum((1, 2), wthree) == 27
    assert enum((2, 1), wthree) == 27


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
    t = tup([I_shape, Y_shape])

    with pytest.raises(AssertionError):
        enum((2, 0), t)

    with pytest.raises(AssertionError):
        enum((1, 1), t)

    assert enum((3, 0), t) == 1
    assert enum((3, 3), t) == 2 ** 6
    

@pytest.fixture
def leaf_shape():
    return tup()


@pytest.fixture
def I_shape():
    return tup([tup()])


@pytest.fixture
def Y_shape():
    return tup([tup([tup(), tup()])])


def test_enumerate(leaf_shape, I_shape, Y_shape):
    assert enum((1, 1), leaf_shape) == 1
    assert enum((4, 4), leaf_shape) == 1

    assert enum((4, 4), I_shape) == 2


@pytest.fixture
def six_in_line():
    """ 1 line, 6 edges (7 nodes) """
    nodes = build_graph("""7
                                  1 2
                                  2 3
                                  3 4
                                  4 5
                                  5 6
                                  6 7""".strip().splitlines())
    return nodes


def test_com_lines(six_in_line):
    assert combinations(six_in_line) == 20  # C(3,6)


def test_build(nodes):
    # print(nodes)  # visual inspection
    pass


def test_ltf(nodes):
    assert len(longest_trace_from(nodes, 1)) == 2  # e.g. (1, 2)
    assert len(longest_trace_from(nodes, 2)) == 3  # e.g. (2, 1, 3)


def test_lp(nodes):
    assert len(longest_path(nodes)) == 3  # e.g. (2, 1, 3)


def test_shape3(nodes):
    assert shape3(nodes, 3, exclude=1) == ()  # 3 is leaf
    assert shape3(nodes, 1, exclude=3) == ((), ())  # 1 has two leaf childred (2, 4); 3 is excluded
    tt = shape3(nodes, 1, exclude=3)
    assert tt.height == (1, 1)
    assert tt[0].height == (0, 0)
    assert tt[1].height == (0, 0)


def test_tup():
    rv = \
        tup([
            tup([
                tup(),
                tup()]),
            tup()])
    assert rv[0][1].height == (0, 0)
    assert rv[0].height == (1, 1)
    assert rv[1].height == (0, 0)
    assert rv.height == (1, 2)

    rv2 = tup([tup(), rv])
    assert rv2.height == (1, 3)

    rv3 = tup([rv, rv2, rv2, rv])
    assert rv3.height == (2, 4)


def test_tup_edges(leaf_shape, I_shape, Y_shape):
    assert not leaf_shape.edges
    assert I_shape.edges == 1
    assert Y_shape.edges == 3
