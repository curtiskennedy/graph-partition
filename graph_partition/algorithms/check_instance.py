# Curtis Kennedy, Terence Pun
# ckennedy@ualberta.ca


def approx1Check(graph):
    # requirements:
    # - biconnected
    # - 2 or more nodes
    return graph.is2Connected() and len(graph.nodes) >= 2


def approx2Check(graph):
    # requirements:
    # - connected
    # - 3 or more nodes
    return graph.isConnected() and len(graph.nodes) >= 3


def approx3Check(graph):
    # requirements:
    # - biconnected
    # - 3 or more nodes
    return graph.is2Connected() and len(graph.nodes) >= 3


def approx4Check(graph):
    # requirements:
    # - connected
    # - two biconnected components
    # - one cut vertex
    return (graph.isConnected()) and (len(graph.getBicomponents()) == 2) and (len(graph.cutVerticies()) == 1)


def approx5Check(graph):
    # requirements:
    # - connected
    # - more than two biconnected components
    return graph.isConnected() and len(graph.getBicomponents()) >= 2


def approx6Check(graph):
    # requirements:
    # - biconnected
    # - 3 or more nodes
    return graph.is2Connected() and len(graph.nodes) >= 3


def approx7Check(graph):
    # requirements:
    # - connected
    # - two biconnected components
    # - one cut vertex
    return (graph.isConnected()) and (len(graph.getBicomponents()) == 2) and (len(graph.cutVerticies()) == 1)


def approx8Check(graph):
    # requirements:
    # - connected
    # - more than two biconnected components
    return graph.isConnected() and len(graph.getBicomponents()) >= 2


def checkAll(graph):
    '''
    Retuns a list of algorithms that are supported for this instance
    '''
    result = []

    if approx1Check(graph,True):
        result.append("Approx-1 for MAX-MIN k=2 (recommended)")
    if approx2Check(graph,True):
        result.append("Approx-2 for MAX-MIN k=2")
    if approx3Check(graph,True):
        result.append("Approx-3 for MIN-MAX k=3 (recommended)")
    if approx4Check(graph,True):
        result.append("Approx-4 for MIN-MAX k=3")
    if approx5Check(graph,True):
        result.append("Approx-5 for MIN-MAX k=3")
    if approx6Check(graph,True):
        result.append("Approx-6 for MAX-MIN k=3 (recommended)")
    if approx7Check(graph,True):
        result.append("Approx-7 for MAX-MIN k=3")
    if approx8Check(graph,True):
        result.append("Approx-8 for MAX-MIN k=3")

    return result
    