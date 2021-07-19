# Curtis Kennedy, Terence Pun
# ckennedy@ualberta.ca


def approx3(V):

    graphWeight = V.weight()
    heaviest = V.getHeaviestNode()
    v1 = V.createView([heaviest]) # v1 is a graph object containing one node (heaviest)
    v2 = V.getHeaviestNode(set([heaviest])) # v2 is the second heaviest nodeID

    # Step 1
    if (v1.weight() >= (2/5) * graphWeight):
        V1, V2 = V.slash(v1).anyBipartition()
        # print("termination in step 1")
        return V1, V2, v1
    
    # Step 2
    V1 = v1
    V2 = V.slash(v1)

    # Step 3
    while (V2.weight() > (1/2) * graphWeight):
        applicable, u = V2.pull2(V1, graphWeight, v2)

        if not applicable:
            # print("last checked Pull-2 operation not executed")
            return V2.createView([u]), V1, V2.slash([u])

    # Step 4
    # print("termination due to moving u from V2 to V1")
    return V1.createView([u]), V1.slash([u]), V2



if __name__ == "__main__":
    from graph_partition.classes.instanceManager import readInstance
    from graph_partition.algorithms.check_instance import approx3Check
    import time

    ##################################
    Instance_Name = "gg_05_05_a_1"
    #################################

    Folder_Name = "test-instances"
    File_Extension = ".in"
    path = '../{}/{}{}'.format(Folder_Name, Instance_Name, File_Extension)
    graph = readInstance(path)
    approx3Check(graph)

    # print(graph)
    
    start = time.time()
    V1, V2, V3 = approx3(graph)
    end = time.time()

    print("\nInstance name =", Instance_Name)
    print("Time taken =", end-start, "seconds")
    print("V1 weight =", V1.weight())
    print("V2 weight =", V2.weight())
    print("V3 weight =", V3.weight())

    # print(graph)