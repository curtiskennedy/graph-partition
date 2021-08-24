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
        return V1, V2, v1
    
    # Step 2
    V1 = v1
    V2 = V.slash(v1)

    # Step 3
    while (V2.weight() > (1/2) * graphWeight):
        applicable, u = V2.pull2(V1, graphWeight, v2)

        if not applicable:
            return V2.createView([u]), V1, V2.slash([u])

    # Step 4
    return V1.createView([u]), V1.slash([u]), V2
