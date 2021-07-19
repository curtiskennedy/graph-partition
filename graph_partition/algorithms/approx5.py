# Curtis Kennedy
# ckennedy@ualberta.ca

from graph_partition.algorithms.approx3 import approx3
from graph_partition.algorithms.approx4 import approx4

from itertools import combinations


def approx5(V):
    count = 0
    
    bestV1P1 = None
    bestV2P1 = None
    bestV3P1 = None
    maxP1Weight = float('inf')

    bestV1P2 = None
    bestV2P2 = None
    bestV3P2 = None   
    maxP2Weight = float('inf')
    # Note: using MIN-MAX to evaluate best partition
    
    compList = V.getBicomponents()
    cutVerticies = V.cutVerticies()
    graphWeight = V.weight() # testing
    bicomps = len(compList)
    goal = .5 * bicomps * (bicomps+1)
    updateEveryXIterations = int(goal/100)
    if updateEveryXIterations == 0:
        updateEveryXIterations = 1

    # Note the weights of cut vertices before we change them
    oldWeights = {}
    for cutVertex in cutVerticies:
        oldWeights[cutVertex] = V[cutVertex]['weight']


    # * PART 1
    print("starting part 1 (approx-3 on each bicomponent)")
    for component in compList:
        count+=1
        if not count % updateEveryXIterations:
            percent = count/goal
            print("iteration {}/{} = {:.0%}".format(count, goal, percent))
        if len(component.nodes) < 3:
            continue
        # modify weight and call approx3 on each comp

        # change the weights of the cut vertices in this component
        # this essentially collapses other components into the cut vertices
        for cutVertex in cutVerticies:
            if cutVertex in component:
                toCollapse = V.slash(component.slash([cutVertex])).findConnectedComponent(cutVertex)
                # print("converting vertex", cutVertex, "into", toCollapse)
                newWeight = toCollapse.weight()
                component[cutVertex]['weight'] = newWeight

        # print("\nCALLING APPROX-3 ON COMPONENT =", component)
        V1, V2, V3 = approx3(component)
        # print("\nV1 =", V1)
        # print("\nV2 =", V2)
        # print("\nV3 =", V3)

        # change cut vertex weights back and add the remaining nodes to the partitions
        for cutVertex in cutVerticies:
            if cutVertex in component:
                V[cutVertex]['weight'] = oldWeights[cutVertex] # change weight back

                # un-collapse other components
                graphToAdd = V.slash(component.slash([cutVertex])).findConnectedComponent(cutVertex)
                if cutVertex in V1:
                    V1 = V1.union(graphToAdd)
                elif cutVertex in V2:
                    V2 = V2.union(graphToAdd)
                elif cutVertex in V3:
                    V3 = V3.union(graphToAdd)

        # evaluate the partition

        # v1w, v2w, v3w = V1.weight(), V2.weight(), V3.weight()
        # tot = v1w + v2w + v3w
        # print("approx-3 results {} + {} + {} = {}".format(v1w, v2w, v3w, tot))

        result = max(V1.weight(), V2.weight(), V3.weight())
        if result < maxP1Weight:
            bestV1P1 = V1
            bestV2P1 = V2
            bestV3P1 = V3
            maxP1Weight = result

            
    
    # * PART 2
    # find all pairs of 2-connected components that share one cut vertex
    print("starting part 2 (approx-4 on each pair of bicomponents)")
    for combo in combinations(compList, 2):
        comp1, comp2 = combo[0], combo[1]
        # print("------------------------------------------------------------")
        count+=1
        if not count % updateEveryXIterations:
            percent = count/goal
            print("iteration {}/{} = {:.0%}".format(count, goal, percent))
        # print("found two non-equal components, their weights are {} and {}".format(comp1.weight(), comp2.weight()))
        # print("comp1 nodes =", comp1.nodeView())
        # print("comp2 nodes =", comp2.nodeView())

        union = comp1.union(comp2)
        # print("combined them together, the weight is now", union.weight())

        # modify the input graph to remove all non-cut verticies in the union and all edges in the union
        modifiedV = V.slash(union.slash(cutVerticies))
        removedEdges = V.removeUnionEdges(comp1, comp2) # this is destructive, V is repaired using V.reAddEdges(removedEdges)

        collapsedOn = {}
        for cutVertex in cutVerticies:
            if cutVertex in union:
                toCollapse = modifiedV.findConnectedComponent(cutVertex)
                collapsedOn[cutVertex] = toCollapse.nodeView()

        # print(removedEdges)
        V.reAddEdges(removedEdges)

        # * Build the graph to call approx-4 on
        # figure out if overlap is required, and what it should be
        # print("need to collapse:", collapsedOn)
        requiredOverlap = set()
        for collapsedOnNode in collapsedOn:
            if requiredOverlap != set():
                break
            for otherCON in collapsedOn:
                if (collapsedOnNode != otherCON) and collapsedOn[collapsedOnNode] == collapsedOn[otherCON]:
                    # overlap is required
                    # print("collapsing {} onto {}".format(collapsedOn[collapsedOnNode], collapsedOnNode))
                    # print("overlap {} on {}".format(collapsedOnNode, otherCON))
                    V.nodes[collapsedOnNode]['weight'] = V.createView(collapsedOn[collapsedOnNode]).weight()
                    union, addedEdges = union.overLayVertex(collapsedOnNode, otherCON) # this is destructive
                    requiredOverlap.add(collapsedOnNode)
                    requiredOverlap.add(otherCON)
                    break

        for node in collapsedOn:
            if node not in requiredOverlap:
                # print("collapsing {} onto {}".format(collapsedOn[node], node))
                V.nodes[node]['weight'] = V.createView(collapsedOn[node]).weight()

        # print("\nCALLING APPROX-4 ON UNION WEIGHT = {}".format(union.weight()))
        if union.weight() != graphWeight:
            raise Exception("error in collapsing")

        V1, V2, V3 = approx4(union)
        # print("\nV1 = {} weight = {}".format(V1.nodeView(), V1.weight()))
        # print("\nV2 = {} weight = {}".format(V2.nodeView(), V2.weight()))
        # print("\nV3 = {} weight = {}".format(V3.nodeView(), V3.weight()))

        # repair overlap
        if requiredOverlap != set():
            V.delEdges(addedEdges)

        # change cut vertex weights back and add the remaining nodes to the partitions
        for cutVertex in cutVerticies:
            if cutVertex in union:
                V[cutVertex]['weight'] = oldWeights[cutVertex] # change weight back

        # un-collapse
        for vert in collapsedOn:
            if vert in V1:
                # print("uncollapsing {} and adding to partition 1".format(collapsedOn[vert]))
                V1 = V1.union(V.createView(collapsedOn[vert]))
            elif vert in V2:
                # print("uncollapsing {} and adding to partition 2".format(collapsedOn[vert]))
                V2 = V2.union(V.createView(collapsedOn[vert]))
            else:
                # print("uncollapsing {} and adding to partition 3".format(collapsedOn[vert]))
                V3 = V3.union(V.createView(collapsedOn[vert]))
            
        # print("\nV1 = {} weight = {}".format(V1.nodeView(), V1.weight()))
        # print("\nV2 = {} weight = {}".format(V2.nodeView(), V2.weight()))
        # print("\nV3 = {} weight = {}".format(V3.nodeView(), V3.weight()))

        # evaluate the partition
        # v1w, v2w, v3w = V1.weight(), V2.weight(), V3.weight()
        # tot = v1w + v2w + v3w
        # print("approx-4 results {} + {} + {} = {}".format(v1w, v2w, v3w, tot))
        result = max(V1.weight(), V2.weight(), V3.weight())
        if result < maxP2Weight:
            bestV1P2 = V1
            bestV2P2 = V2
            bestV3P2 = V3
            maxP2Weight = result
                
        
    # return the best MIN-MAX
    if maxP1Weight < maxP2Weight:
        # Part 1 is better
        print("Using part 1 (approx-3) result")
        V1 = bestV1P1
        V2 = bestV2P1
        V3 = bestV3P1
    else:
        # Part 2 is better or same result
        print("Using part 2 (approx-4) result")
        V1 = bestV1P2
        V2 = bestV2P2
        V3 = bestV3P2

    if count != goal:
        raise Exception("didn't run correct # of iterations")
    # print("ran {} iterations".format(count))

    return V1, V2, V3


if __name__ == "__main__":
    from graph_partition.classes.instanceManager import readInstance
    from graph_partition.algorithms.check_instance import approx5Check
    import time

    ##################################
    Instance_Name = "unicamp_624_901"
    #################################

    Folder_Name = "test-instances"
    File_Extension = ".in"
    path = '../{}/{}{}'.format(Folder_Name, Instance_Name, File_Extension)
    graph = readInstance(path)
    approx5Check(graph)

    # print("initial graph =", graph)
    print("\n+++++++++++++++++++++++++++++++++++++++++++")
    bicomps = len(graph.getBicomponents())
    print("how many bicomponents are there?", bicomps)
    print("initial weight =", graph.weight())
    goal = .5 * bicomps * (bicomps+1)
    print("there should be {} iterations".format(goal))
    
    start = time.time()
    V1, V2, V3 = approx5(graph)
    end = time.time()

    print("+++++++++++++++++++++++++++++++++++++++++++")
    print("Instance name =", Instance_Name)
    print("Time taken =", end-start, "seconds")
    print("V1 weight =", V1.weight())
    print("V2 weight =", V2.weight())
    print("V3 weight =", V3.weight())
    print("+++++++++++++++++++++++++++++++++++++++++++")

    # print("\nResulting partition:")
    # print("V1=",V1)
    # print("\nV2=",V2)
    # print("\nV3=",V3, "\n")

    # print("graph weight after approx5 =", graph.weight())
    # print(graph)