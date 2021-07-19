# Curtis Kennedy
# ckennedy@ualberta.ca


def approx1Check(graph, bool=False):
    # requirements:
    # - biconnected
    # - 2 or more nodes
    if bool:
        return graph.is2Connected() and len(graph.nodes) >= 2

    if not graph.is2Connected():
        raise Exception("graph is NOT 2-connected!")
    if len(graph.nodes) < 2:
        raise Exception("graph contains less than 2 nodes!")


def approx2Check(graph, bool=False):
    # requirements:
    # - connected
    # - 3 or more nodes
    if bool:
        return graph.isConnected() and len(graph.nodes) >= 3

    if graph.is2Connected():
        print("WARNING! graph is already 2-connected, run approx1 instead!")
    if not graph.isConnected():
        raise Exception("graph is NOT connected!")
    if len(graph.nodes) < 3:
        raise Exception("graph contains less than 3 nodes!")


def approx3Check(graph, bool=False):
    # requirements:
    # - biconnected
    # - 3 or more nodes
    if bool:
        return graph.is2Connected() and len(graph.nodes) >= 3

    if not graph.is2Connected():
        raise Exception("graph is NOT 2-connected!")
    if len(graph.nodes) < 3:
        raise Exception("graph contains less than 3 nodes!")


def approx4Check(graph, bool=False):
    # requirements:
    # - connected
    # - 3 or more nodes ?
    # - two biconnected components
    if bool:
        return (graph.isConnected()) and (len(graph.getBicomponents()) == 2) and (len(graph.cutVerticies()) == 1)

    if graph.is2Connected():
        print("WARNING! graph is already 2-connected, run approx3 instead!")
    if not graph.isConnected():
        raise Exception("graph is NOT connected!")
    if len(graph.nodes) < 4:
        raise Exception("graph contains less than 4 nodes!")
    if len(graph.getBicomponents()) != 2:
        # for comp in graph.getBicomponents():
        #     print(comp)
        raise Exception("graph does NOT have two biconnected components!")
    if len(graph.cutVerticies()) != 1:
        raise Exception("graph does NOT have one cut vertex!")


def approx5Check(graph, bool=False):
    # requirements:
    # - connected
    # - more than two biconnected components
    # - 6 or more nodes?
    if bool:
        return graph.isConnected() and len(graph.getBicomponents()) >= 2

    # twoConnectedCompList, cutVertices = V.findAll2Components()
    # if len(twoConnectedCompList) > len(V.nodes) - 1:
    #     raise Exception("The number of 2 connected components is greater than V -1")

    pass


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

    return result