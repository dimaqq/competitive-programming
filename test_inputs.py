import pytest
import subtree


@pytest.fixture
def sample_data1():
    data = """4
              1 2
              1 3
              1 4""".strip().splitlines()
    return subtree.build_graph(data)


@pytest.fixture
def nodes(sample_data1):
    nodes = sample_data1
    return nodes


@pytest.fixture
def nodes2():
    nodes = subtree.build_graph("""4
                                  1 2
                                  2 3
                                  3 4""".strip().splitlines())
    return nodes


@pytest.fixture
def nodes3():
    nodes = subtree.build_graph("""6
                                  1 2
                                  1 3
                                  1 4
                                  2 5
                                  2 6""".strip().splitlines())
    return nodes


@pytest.fixture
def nodes4():
    nodes = subtree.build_graph("""10
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


def test_com(nodes, nodes2, nodes3, nodes4):
    assert subtree.combinations(nodes) == 2
    assert subtree.combinations(nodes2) == 6
    assert subtree.combinations(nodes3) == 14
    assert subtree.combinations(nodes4) == 102
