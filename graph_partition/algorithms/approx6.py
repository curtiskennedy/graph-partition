# Curtis Kennedy, Terence Pun
# ckennedy@ualberta.ca

from graph_partition import Graph


def approx6(V):

    V_Weight = V.weight()               # total weight
    v1 = V.getHeaviestNode()            # heaviest node
    v1_weight = V.nodeWeight(v1)        # heaviest node weight
    v2 = V.getHeaviestNode({v1})        # second heaviest node
    v2_weight = V.nodeWeight(v2)        # second heaviest node weight
    v3 = V.getHeaviestNode({v1, v2})    # third heaviest node
    v3_weight = V.nodeWeight(v3)        # third heaviest node weight

    # Step 1
    if v1_weight >= v2_weight >= v3_weight >= ((1/5) * V_Weight):
        print("Step 1 further testing needed")
        #!testing needed
        return V.bfs(v1,v2,v3)

    # Step 2
    if v1_weight >= ((1/5) * V_Weight) > v3_weight:
        print("Step 2")

        # 2a
        for u in V.slash([v1]):
            print("u =", u)
            found = True
            heaviestCompWeight = -1
            heaviestComp = None
            for component in V.slash([v1, u]).findAllConnectedComponents():
                if component.weight() > heaviestCompWeight:
                    heaviestCompWeight = component.weight()
                    heaviestComp = component
                if component.weight() > ((1/2) * (V_Weight - v1_weight)):
                    found = False
                    break
            if found:
                print("2a Found u =", u)
                return V.createView([v1]), V.slash(heaviestComp.union(V.createView([v1]))), heaviestComp

        # 2b
        heaviestCompWeight = -1
        heaviestComp = None
        for component in V.slash([v1, v3]).findAllConnectedComponents():
            if component.weight() > heaviestCompWeight:
                heaviestCompWeight = component.weight()
                heaviestComp = component
        V3 = heaviestComp
        V2 = V.slash(V3.union(V.createView([v1])))
        # Pull-3
        applicable = True
        while V3.weight() > ((1/2) * V2.union(V3).weight()) and applicable:
            applicable, V2, V3 = V3.pull3(V2)
        print("2b")
        return V.createView([v1]), V2, V3


    # Step 3
    if ((1/5) * V_Weight) > v1_weight:
        print("Step 3")
        V1 = V.createView([v1])
        V2 = V.slash(V1)

        applicable = True
        uList = [v1]
        while (V2.weight() > (4/5) * V_Weight) and applicable:
            applicable, u = V2.pull2NEW(V1, V_Weight, v2)
            if applicable:
                uList.append(u)

        # V1 is initialized
        # try to find a 'u'
        U = None
        for u in V.slash(V1).cutVerticies():
            # print("u =", u)
            found = True
            heaviestCompWeight = -1
            heaviestComp = None
            for component in V.slash(V1.union(V.createView([u]))).findAllConnectedComponents():
                if component.weight() > heaviestCompWeight:
                    heaviestCompWeight = component.weight()
                    heaviestComp = component
                if component.weight() > ((2/3) * (V_Weight - V1.weight())):
                    found = False
                    break
            if found:
                print("Found u =", u)
                U = heaviestComp
                break

        try:
            # 3a
            # print("U =", U)
            if U.weight() >= ((1/5) * V_Weight):
                print("3a")
                return V1, V.slash(V1.union(U)), U
            
            # 3b
            # else
            if U.weight() < ((1/5) * V_Weight):
                print("3b")
                compList = V.slash(V1.union(V.createView([u]))).findAllConnectedComponents()
                if len(compList) < 3:
                    raise Exception("ERROR HERE")
                #!testing needed
                for j in range(len(uList)-1, 0, -1):
                    uj = uList[j]
                    totalWeight = 0
                    adjCompList = []
                    for comp in compList:
                        # if comp.isAdjacentTo(V1.createView([uj])):
                        if comp.isAdjacentTo(V1.createView([uj])) and not comp.isAdjacentTo(V1.slash([uj])):
                            """
                            When the total weight of the components among G[Ui]’s that are adjacent to only
                            the vertex uj from V1 is greater than...
                            """
                            # ? which above 'if' statement is correct, given the word 'only'?
                            totalWeight += comp.weight()
                            adjCompList.append(comp)
                    # evaluate totalWeight to decide case
                    if totalWeight < (((1/5)*V_Weight) - V1.nodeWeight(uj)):
                        # pull uj out of V1 and continues in the for loop
                        print("3b.1 further testing needed")
                        V1 = V1.slash([uj])
                        newComp = Graph({})
                        for adjComp in adjCompList:
                            compList.remove(adjComp)
                            newComp = newComp.union(adjComp)
                        newComp.addVertex(uj, V.nodes[uj]['edges'], V.nodes[uj]['weight'])
                        compList.append(newComp)

                    elif totalWeight > (((4/5)*V_Weight) - V.nodeWeight(uj) - V.nodeWeight(u)):
                        print("3b.2 further testing needed")
                        #returns
                        GU = V.slash([uj,u]).heaviestComp()
                        V2 = V.createView([uj])
                        while V2.weight() < ((1/5)*V_Weight):
                            compToAdd = compList.pop(0)
                            if compToAdd != GU and compToAdd.isAdjacentTo(V2):
                                V2 = V2.union(compToAdd)
                            else:
                                compList.append(compToAdd)
                        return U, V2, V.slash(U.union(V2))

                    else:
                        print("3b.3 further testing needed")
                        #returns
                        V2 = V.createView([uj])
                        while V2.weight() < ((1/5)*V_Weight):
                            compToAdd = compList.pop(0)
                            if compToAdd.isAdjacentTo(V2):
                                V2 = V2.union(compToAdd)
                            else:
                                compList.append(compToAdd)
                        V1 = V1.slash([uj])
                        while V1.weight() < ((1/5)*V_Weight):
                            compToAdd = compList.pop(0)
                            if compToAdd.isAdjacentTo(V1):
                                V1 = V1.union(compToAdd)
                            else:
                                compList.append(compToAdd)
                        V3 = V.createView([u])
                        for comp in compList:
                            V3 = V3.union(comp)
                        return V1, V2, V3

        except AttributeError:
            # 3c
            # u not found
            print("3c")
            V3 = V.slash(V1.union(V.createView([v2]))).heaviestComp()
            V2 = V.slash(V1.union(V3))
            # Pull-3
            applicable = True
            while V3.weight() > ((1/2) * V2.union(V3).weight()) and applicable:
                applicable, V2, V3 = V3.pull3(V2)
            return V1, V2, V3
