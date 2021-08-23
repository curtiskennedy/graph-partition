# Curtis Kennedy, Terence Pun
# ckennedy@ualberta.ca

from graph_partition.classes.graph import Graph


def readInstance(path):
    
    with open(path, "r") as infile:
        data = infile.readlines()
    graph = Graph({})
    nnodes = int(data[1].split()[0])
    # node id and weight
    for line in data[3:nnodes+3]:
        id = int(line.split()[0])
        weight = int(line.split()[3])
        graph.addVertex(id, [], weight)
    # edges
    for line in data[nnodes+4:]:
        dest1 = int(line.split()[0])
        dest2 = int(line.split()[1])
        graph.addEdge(dest1, dest2)
        graph.addEdge(dest2, dest1)
    return graph
