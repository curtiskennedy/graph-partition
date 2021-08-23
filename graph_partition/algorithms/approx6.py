# Curtis Kennedy, Terence Pun
# ckennedy@ualberta.ca

from graph_partition.algorithms.check_instance import approx6Check
from graph_partition import Graph


def approx6(V:Graph):

    V_Weight = V.weight()
    v1 = V.getHeaviestNode()
    v1_weight = V.nodeWeight(v1)
    v2 = V.getHeaviestNode({v1})
    v2_weight = V.nodeWeight(v2)
    v3 = V.getHeaviestNode({v1, v2})
    v3_weight = V.nodeWeight(v3)

    # Step 1
    if v1_weight >= v2_weight >= v3_weight >= ((1/5) * V_Weight):
        print("Step 1 TEST")
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
                print("3b TEST")
                compList = V.slash(V1.union(V.createView([u]))).findAllConnectedComponents()
                if len(compList) < 3:
                    raise Exception("ERROR HERE")
                #!testing needed
                for j in range(len(uList)-1, 0, -1):
                    uj = uList[j]
                    totalWeight = 0
                    adjCompList = []
                    for comp in compList:
                        if comp.isAdjacentTo(V1.createView([uj])):
                            totalWeight += comp.weight()
                            adjCompList.append(comp)
                    # evaluate totalWeight to decide case
                    if totalWeight < (((1/5)*V_Weight) - V1.nodeWeight(uj)):
                        # pull uj out of V1 and continues in the for loop
                        print("3b.1 TEST")
                        V1 = V1.slash([uj])
                        newComp = Graph({})
                        for adjComp in adjCompList:
                            compList.remove(adjComp)
                            newComp = newComp.union(adjComp)
                        newComp.addVertex(uj, V.nodes[uj]['edges'], V.nodes[uj]['weight'])
                        compList.append(newComp)

                        
                    elif totalWeight > (((4/5)*V_Weight) - V.nodeWeight(uj) - V.nodeWeight(u)):
                        print("3b.2 TEST")
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
                        print("3b.3 TEST")
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

    
    

if __name__ == "__main__":
    from graph_partition.classes.instanceManager import readInstance
    from graph_partition.algorithms.check_instance import approx6Check
    import time

    ##################################
    Instance_Name = "ap6test"
    #################################

    Folder_Name = "all-instances/local_testing"
    File_Extension = ".in"
    path = '../{}/{}{}'.format(Folder_Name, Instance_Name, File_Extension)
    graph = readInstance(path)
    approx6Check(graph)

    # print(graph)
    
    start = time.time()
    V1, V2, V3 = approx6(graph)
    # approx6(graph)
    end = time.time()

    print(graph.weight())
    print("\nInstance name =", Instance_Name)
    print("Time taken =", end-start, "seconds")
    print("V1 weight =", V1.weight())
    print("V2 weight =", V2.weight())
    print("V3 weight =", V3.weight())
    print(graph.weight())
    print(V1.weight()+V2.weight()+V3.weight())

    # print(V1)
    # print(V2)
    # print(V3)