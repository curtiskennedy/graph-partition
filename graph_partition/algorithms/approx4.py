# Curtis Kennedy, Terence Pun
# ckennedy@ualberta.ca
# Note: input graph V is not altered?


def approx4(V):
    u = V.getHeaviestNode()
    graphWeight = V.weight()

    # Step 1
    if V.nodes[u]['weight'] >= (2/5) * graphWeight:
        V3 = V.createView([u])
        V1, V2 = V.slash([u]).anyBipartition()
        # print("Terminated in step 1")
        return V1, V2, V3
    
    # Step 2
    # Find H1 and H2
    compList = V.getBicomponents()
    H1 = compList[0]
    H2 = compList[1]
    v1 = V.cutVerticies().pop()

    
    if (H1.weight() >= (1/2) * graphWeight) and (H2.weight() >= (1/2) * graphWeight):
        # V3 = V.newPartition(v1, True)
        V3 = V.createView([v1])
        # print("Terminated in step 2")
        return H1.slash([v1]), H2.slash([v1]), V3
    
    # Step 3
    # check if assumption is wrong and handle accordingly
    if H2.weight() < (1/2) * graphWeight:
        temp = H1
        H1 = H2
        H2 = temp

    # Step 4
    V1 = H1
    V2 = V.slash(H1)

    # Step 5
    v2 = H2.slash(H1).getHeaviestNode()
    while (V2.weight() > (1/2) * graphWeight):
        applicable, u = V2.pull2(V1, graphWeight, v2)

        if not applicable:
            # print("pull 2 ran until not applicable")
            break

    
    # Step 6
    # print("Terminated in step 6")
    return V.createView([u]), V1.union(H1), V2.slash([u])


if __name__ == "__main__":
    from graph_partition.classes.instanceManager import readInstance
    from graph_partition.algorithms.check_instance import approx4Check
    import time

    ##################################
    Instance_Name = "custom"
    #################################

    Folder_Name = "test-instances"
    File_Extension = ".in"
    path = '../{}/{}{}'.format(Folder_Name, Instance_Name, File_Extension)
    graph = readInstance(path)
    approx4Check(graph)

    # print(graph)
    w = graph.weight()
    
    start = time.time()
    V1, V2, V3 = approx4(graph)
    end = time.time()

    print("\nInstance name =", Instance_Name)
    print("Time taken =", end-start, "seconds")
    print("V1 weight =", V1.weight())
    print("V2 weight =", V2.weight())
    print("V3 weight =", V3.weight())

    # print(graph)
    print("\nV1 =", V1.nodeView())
    print("V2 =", V2.nodeView())
    print("V3 =", V3.nodeView())

    if V1.weight() + V2.weight() + V3.weight() != w:
        print("ERROR")