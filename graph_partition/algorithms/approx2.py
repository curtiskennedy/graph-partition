# Curtis Kennedy, Terence Pun
# ckennedy@ualberta.ca

from graph_partition.algorithms.approx1 import approx1


def approx2(V):

    twoConnectedCompList = V.getBicomponents()
    goal = len(twoConnectedCompList)
    updateEveryXIterations = int(goal/100) + 1
    cutVerticies = V.cutVerticies()

    bestV1 = bestV2 = None
    maxMinWeight = -1

    # Note the weights of cut vertices before we change them
    oldWeights = {}
    for cutVertex in cutVerticies:
        oldWeights[cutVertex] = V[cutVertex]['weight']

    # for each 2-connected component
    count = 0
    for component in twoConnectedCompList:
        count += 1
        if not count % updateEveryXIterations:
            percent = count/goal
            print("iteration {}/{} = {:.0%}".format(count, goal, percent))

        # adjust weights of cut verticies in this component
        for cutVertex in cutVerticies:
            if cutVertex in component:

                toCollapse = V.slash(component.slash([cutVertex])).findConnectedComponent(cutVertex)
                newWeight = toCollapse.weight()
                component[cutVertex]['weight'] = newWeight

        V1, V2 = approx1(component) # call approx1 on this component

        # change cut vertex weights back and un-collapse the other components
        for cutVertex in cutVerticies:
            if cutVertex in component:
                V[cutVertex]['weight'] = oldWeights[cutVertex] # change weight back

                # un-collapse other components
                graphToAdd = V.slash(component.slash([cutVertex])).findConnectedComponent(cutVertex)
                if cutVertex in V1:
                    V1 = V1.union(graphToAdd)
                elif cutVertex in V2:
                    V2 = V2.union(graphToAdd)

        # evaluate the partition using MAX-MIN
        minWeight = min(V1.weight(), V2.weight())
        if minWeight > maxMinWeight:
            bestV1 = V1
            bestV2 = V2
            maxMinWeight = minWeight
        
    # return the best
    return bestV1, bestV2



if __name__ == "__main__":
    from graph_partition.classes.instanceManager import readInstance
    from graph_partition.algorithms.check_instance import approx2Check
    import time

    ##################################
    Instance_Name = "barao_1913_2752"
    #################################

    Folder_Name = "all-instances/real"
    File_Extension = ".in"
    path = '../{}/{}{}'.format(Folder_Name, Instance_Name, File_Extension)
    graph = readInstance(path)
    approx2Check(graph)

    # print(graph)
    
    start = time.time()
    V1, V2 = approx2(graph)
    end = time.time()

    print("\nInstance name =", Instance_Name)
    print("Time taken =", end-start, "seconds")
    print("V1 weight =", V1.weight())
    print("V2 weight =", V2.weight())
