# Curtis Kennedy, Terence Pun
# ckennedy@ualberta.ca

from graph_partition.algorithms.check_instance import approx1Check


def approx1(V):

    graphWeight = V.weight()

    # Step 1
    V1 = V.createView([V.getHeaviestNode()])
    V2 = V.slash(V1)

    # Step 2
    if (V1.weight() >= (1/2) * graphWeight):
        return V1, V2
    
    # Step 3
    while (V1.weight() < (3/8) * graphWeight): #* Note: try adjusting stop condition -> 1/2 and last iteration had improvement
        applicable = V2.pull1(V1, graphWeight)

        if not applicable:
            break

    # Step 4
    return V1, V2
    
    

if __name__ == "__main__":
    from graph_partition.classes.instanceManager import readInstance
    from graph_partition.algorithms.check_instance import approx1Check
    import time

    ##################################
    Instance_Name = "gg_05_05_a_1"
    #################################

    Folder_Name = "test-instances"
    File_Extension = ".in"
    path = '../{}/{}{}'.format(Folder_Name, Instance_Name, File_Extension)
    graph = readInstance(path)
    approx1Check(graph)

    # print(graph)
    
    start = time.time()
    V1, V2 = approx1(graph)
    end = time.time()

    print("\nInstance name =", Instance_Name)
    print("Time taken =", end-start, "seconds")
    print("V1 weight =", V1.weight())
    print("V2 weight =", V2.weight())
