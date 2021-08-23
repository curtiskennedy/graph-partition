# Curtis Kennedy, Terence Pun
# ckennedy@ualberta.ca


def approx1(V):

    graphWeight = V.weight()

    # Step 1
    V1 = V.createView([V.getHeaviestNode()])
    V2 = V.slash(V1)

    # Step 2
    if (V1.weight() >= (1/2) * graphWeight):
        return V1, V2
    
    # Step 3
    while (V1.weight() < (3/8) * graphWeight):
        applicable = V2.pull1(V1, graphWeight)

        if not applicable:
            break

    # Step 4
    return V1, V2
