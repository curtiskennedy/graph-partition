# Curtis Kennedy, Terence Pun
# ckennedy@ualberta.ca

from graph_partition.algorithms.approx1 import approx1


def approx7(V):

    graphWeight = V.weight()
    # Find H1 and H2
    compList = V.getBicomponents()
    H1 = compList[0]
    H2 = compList[1]
    v0 = V.cutVerticies().pop()

    # Step 1
    if V.nodeWeight(v0) >= min((1/5)*graphWeight,H1.slash([v0]).weight(),H2.slash([v0]).weight()):
        # print("Step 1")
        # ? does this case not guarantee a 5/3 approximation?
        return H1.slash([v0]), V.createView([v0]), H2.slash([v0])

    # Step 2
    v1 = H1.getHeaviestNode() #? what if v0 is the heaviest node?
    v2 = H2.getHeaviestNode() #? what if v0 is the heaviest node?
    V1 = V3 = None
    if V.nodeWeight(v1) >= (1/5)*graphWeight:
        V1 = V.createView([v1])
    if V.nodeWeight(v2) >= (1/5)*graphWeight:
        V3 = V.createView([v2])
    # a)
    if V1 and V3:
        print("Step 2a")
        return V1, V.slash(V1.union(V3)), V3
    # b)
    if V1:
        V1, V3 = V3, V1
        H1, H2 = H2, H1
        v1, v2 = v2, v1
    if V3:
        oldv0 = V.nodeWeight(v0)
        V.nodes[v0]['weight'] = H2.slash([v2]).weight()
        if V.nodeWeight(v0) >= min((1/5)*graphWeight,H1.slash([v0]).weight()):
            print("Step 2b.1")
            return H1.slash([v0]), H2.slash([v2]), V.createView([v2])
        # Approx-1
        V1, V2 = approx1(H1)
        if v0 in V1.nodes:
            V1, V2 = V2, V1
        V.nodes[v0]['weight'] = oldv0
        print("Step 2b.2")
        return V1, V2.union(H2.slash([v2])), V.createView([v2])
    # c)
    V1 = H1.slash([v0])
    V2 = V.createView([v0])
    V3 = H2.slash([v0])
    while V1.weight() >= (2/5)*graphWeight:
        applicable = V1.pull1(V2, graphWeight)
        if not applicable:
            break
    while V3.weight() >= (2/5)*graphWeight:
        applicable = V3.pull1(V2, graphWeight)
        if not applicable:
            break
    print("Step 2c")
    return V1, V2, V3
