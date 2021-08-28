from graph_partition import __version__, Graph


def test_version():
    assert __version__ == '2021.8.27'

def test_graph_weight():
    mockGraph = Graph()
    mockGraph.addVertex(1, [2,3], 98)
    mockGraph.addVertex(2, [1,3], 98)
    mockGraph.addVertex(3, [1,2], 97)
    assert mockGraph.weight() == (98 + 98 + 97)

def test_heaviest_node():
    mockGraph = Graph()
    mockGraph.addVertex(1, [2,3], 98)
    mockGraph.addVertex(2, [1,3], 98)
    mockGraph.addVertex(3, [1,2], 97)
    assert mockGraph[mockGraph.getHeaviestNode()]['weight'] == 98

def test_second_heaviest():
    mockGraph = Graph()
    mockGraph.addVertex(1, [2,3], 98)
    mockGraph.addVertex(2, [1,3], 98)
    mockGraph.addVertex(3, [1,2], 97)
    secondHeaviestNodes = mockGraph.getHeaviestNode([mockGraph.getHeaviestNode()])
    assert mockGraph[secondHeaviestNodes]['weight'] == 98 and secondHeaviestNodes != mockGraph.getHeaviestNode()