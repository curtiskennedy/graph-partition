# Curtis Kennedy, Terence Pun
# ckennedy@ualberta.ca


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
    v2 = V2.getHeaviestNode()
    # v2 = H2.slash(H1).getHeaviestNode()
    # v2Check = V2.getHeaviestNode()
    # if v2 != v2Check:
    #     raise Exception("ERROR")
    while (V2.weight() > (1/2) * graphWeight):
        applicable, u = V2.pull2(V1, graphWeight, v2)

        if not applicable:
            # print("pull 2 ran until not applicable")
            break

    
    # Step 6
    # print("Terminated in step 6")
    return V.createView([u]), V1.union(H1), V2.slash([u])
