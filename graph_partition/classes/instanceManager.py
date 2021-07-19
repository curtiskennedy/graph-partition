# Curtis Kennedy
# ckennedy@ualberta.ca

from graph_partition.classes.graph import Graph


def readInstance(path):
    '''
    Notes:
    '''      
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


if __name__ == "__main__":

    ##################################
    Instance_Name = "gg_05_05_a_1"
    #################################

    Folder_Name = "test-instances"
    File_Extension = ".in"
    path = '../{}/{}{}'.format(Folder_Name, Instance_Name, File_Extension)
    graph = readInstance(path)


    print(graph)
