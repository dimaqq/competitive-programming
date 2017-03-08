import pytest
import subtree


@pytest.fixture
def nodes1():
    return subtree.graph("""4
                            1 2
                            1 3
                            1 4""".strip().splitlines())


@pytest.fixture
def nodes2():
    return subtree.graph("""4
                            1 2
                            2 3
                            3 4""".strip().splitlines())


@pytest.fixture
def nodes3():
    return subtree.graph("""6
                            1 2
                            1 3
                            1 4
                            2 5
                            2 6""".strip().splitlines())


@pytest.fixture
def nodes4():
    return subtree.graph("""10
                            2 4
                            2 5
                            8 3
                            10 7
                            1 6
                            2 8
                            9 5
                            8 6
                            10 6""".strip().splitlines())


def test_com(nodes1, nodes2, nodes3, nodes4):
    """ Test vectors from the competition """
    assert subtree.combinations(nodes1) == 2
    assert subtree.combinations(nodes2) == 6
    assert subtree.combinations(nodes3) == 14
    assert subtree.combinations(nodes4) == 102
