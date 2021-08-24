# Curtis Kennedy, Terence Pun
# ckennedy@ualberta.ca

from graph_partition.algorithms.approx3 import approx3
from graph_partition.algorithms.approx4 import approx4

from itertools import combinations


def approx5(V):

    count = 0
    
    bestV1P1 = bestV2P1 = bestV3P1 = None
    maxP1Weight = float('inf')

    bestV1P2 = bestV2P2 = bestV3P2 = None  
    maxP2Weight = float('inf')

    compList = V.getBicomponents()
    cutVerticies = V.cutVerticies()
    bicomps = len(compList)
    goal = .5 * bicomps * (bicomps+1)
    updateEveryXIterations = int(goal/100) + 1

    # Note the weights of cut vertices before we change them
    oldWeights = {}
    for cutVertex in cutVerticies:
        oldWeights[cutVertex] = V[cutVertex]['weight']



    # * PART 1
    ###########################################################################
    print("starting part 1 (approx-3 on each bicomponent)")
    for component in compList:
        count+=1
        if not count % updateEveryXIterations:
            percent = count/goal
            print("iteration {}/{} = {:.0%}".format(count, goal, percent))
        if len(component.nodes) < 3:
            continue

        # change the weights of the cut vertices in this component
        # this essentially collapses other components into the cut vertices
        for cutVertex in cutVerticies:
            if cutVertex in component:
                toCollapse = V.slash(component.slash([cutVertex])).findConnectedComponent(cutVertex)
                # converting vertex "cutVertex" into "toCollapse"
                newWeight = toCollapse.weight()
                component[cutVertex]['weight'] = newWeight

        # call approx3 on component
        V1, V2, V3 = approx3(component)

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
        result = max(V1.weight(), V2.weight(), V3.weight())
        if result < maxP1Weight:
            bestV1P1, bestV2P1, bestV3P1 = V1, V2, V3
            maxP1Weight = result

            
    
    # * PART 2
    ###########################################################################
    print("starting part 2 (approx-4 on each pair of bicomponents)")
    # for each pair of bicomponents
    for combo in combinations(compList, 2):
        comp1, comp2 = combo[0], combo[1]
        count+=1
        if not count % updateEveryXIterations:
            percent = count/goal
            print("iteration {}/{} = {:.0%}".format(count, goal, percent))

        union = comp1.union(comp2)

        # modify the input graph to remove all non-cut verticies in the union and all edges in the union
        modifiedV = V.slash(union.slash(cutVerticies))
        removedEdges = V.removeUnionEdges(comp1, comp2) # this is destructive, V is repaired using V.reAddEdges(removedEdges)

        # collapse components on vertices
        collapsedOn = {}
        for cutVertex in cutVerticies:
            if cutVertex in union:
                toCollapse = modifiedV.findConnectedComponent(cutVertex)
                collapsedOn[cutVertex] = toCollapse.nodeView()

        V.reAddEdges(removedEdges)

        # Build the graph to call approx-4 on
        # Determine any required overlaps
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

        # call approx4
        V1, V2, V3 = approx4(union)

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
                V1 = V1.union(V.createView(collapsedOn[vert]))
            elif vert in V2:
                V2 = V2.union(V.createView(collapsedOn[vert]))
            else:
                V3 = V3.union(V.createView(collapsedOn[vert]))

        # evaluate the partition
        result = max(V1.weight(), V2.weight(), V3.weight())
        if result < maxP2Weight:
            bestV1P2, bestV2P2, bestV3P2 = V1, V2, V3
            maxP2Weight = result
                
    ###########################################################################

    # return the best MIN-MAX
    if maxP1Weight < maxP2Weight:
        # Part 1 is better
        print("Using part 1 (approx-3) result")
        return bestV1P1, bestV2P1, bestV3P1

    else:
        # Part 2 is better or same result
        print("Using part 2 (approx-4) result")
        return bestV1P2, bestV2P2, bestV3P2
