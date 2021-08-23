# Curtis Kennedy, Terence Pun
# ckennedy@ualberta.ca

import pprint
from itertools import chain, combinations


class Graph:
    '''
    Represents an undirected graph using the following format:

    {0: {'edges': [5, 1], 'weight': 16},
     1: {'edges': [6, 2, 0], 'weight': 30}}

    '''
    def __init__(self, graphData={}) -> None:
        self.nodes = graphData

    def __str__(self) -> str:
        return ("\n" + pprint.pformat(self.nodes, sort_dicts=True, width=70) 
        + "\n" + "Graph weight = " + str(self.weight()) 
        + "\nIs connected? " + str(self.isConnected()) 
        + "\nIs 2-connected? " + str(self.is2Connected()))
        # return ("\nNodes = {}\nWeight = {}\nis connected = {}\nis 2-connected = {}"
        # .format(self.nodeView(), self.weight(), self.isConnected(), self.is2Connected()))

    def __repr__(self) -> str:
        return str(self.nodes.keys())

    def __iter__(self) -> None:
        '''
        Allows iteration over graph object, for example:
        instead of "for nodeID in graph.nodes:"
        we can use "for nodeID in graph:"
        '''
        # ? is this slower than using Graph.nodes?
        return iter(self.nodes)

    def __getitem__(self, key) -> None:
        '''
        Allows for retriving a node using graph[nodeID]
        instead of graph.nodes[nodeID]
        '''
        # ? is this slower than using Graph.nodes?
        return self.nodes[key]

    def __setitem__(self, key, val) -> None:
        '''
        Similar to __getitem__()
        '''
        # ? is this slower than using Graph.nodes?
        self.nodes[key] = val

    def __eq__(self, o: object) -> bool:
        '''
        Used to compare graphs:
        "graph1 == graph2"
        returns true if both graphs have same size and nodeID's
        '''
        return self.isEqualTo(o)

    def createView(self, nodes):
        result = Graph({})
        for node in nodes:
            result.nodes[node] = self.nodes[node]
        return result

    ############################################################################
    # GRAPH-BUILDING METHODS

    def addEdge(self, v1, v2):
        if v1 in self.nodes:
            self.nodes[v1]['edges'].append(v2)

    def addVertex(self, vertexID, edges, weight):
        self.nodes[vertexID] = {'weight': weight, 'edges': edges}

    ############################################################################
    # GRAPH OPERATIONS


    def union(self, rightGraph):
        '''
        graph1.union(graph2) => graph1 U graph2

        Returns a graph representing the union of self and rightGraph
        '''
        leftGraph = self
        union = Graph({})
        for node in leftGraph.nodes:
            if node not in union.nodes:
                union.nodes[node] = leftGraph.nodes[node]
        for node in rightGraph.nodes:
            if node not in union.nodes:
                union.nodes[node] = rightGraph.nodes[node]
        return union


    def intersection(self, rightGraph):
        '''
        graph1.intersection(graph2) => graph1 ∩ graph2

        Returns a graph representing the union of self and rightGraph
        '''
        leftGraph = self
        intersection = Graph({})
        for node in leftGraph.nodes:
            if node in rightGraph.nodes:
                intersection.nodes[node] = leftGraph.nodes[node]
        return intersection

    
    def slash(self, rightGraph):
        # ! requires __iter__ and __getitem__ and __setitem__ to work (since rightGraph can be passed in as a list of nodes or a Graph object)
        # TODO: add list compatibility without above requirement
        leftGraph = self
        graph = Graph({})
        for node in leftGraph:
            if node not in rightGraph:
                graph[node] = leftGraph[node]
        return graph


    def isSubsetOf(self, rightGraph):
        leftGraph = self
        for node in leftGraph.nodes:
            if node not in rightGraph.nodes:
                return False
        return True


    def isEqualTo(self, rightGraph):
        leftGraph = self
        if len(leftGraph.nodes) != len(rightGraph.nodes):
            return False
        for node in leftGraph.nodes:
            if node not in rightGraph.nodes:
                return False
        return True

    ############################################################################
    # WEIGHT


    def weight(self):
        '''
        Returns the total weight of the graph
        '''
        weight = 0
        for node in self.nodes:
            weight += self.nodes[node]['weight']
        return weight

    def nodeWeight(self, nodeID):
        return self.nodes[nodeID]['weight']


    def getLightestNode(self, ignoreList=set()):
        '''
        Returns the id and weight of the lightest node
        '''
        lightNode = "not set"
        lightWeight = float('inf')
        for node in self.nodes:
            if (self.nodes[node]['weight'] < lightWeight) and (node not in ignoreList):
                lightWeight = self.nodes[node]['weight']
                lightNode = node
        if lightNode == "not set":
            return lightNode, False
        return lightNode, lightWeight




    ############################################################################
    # PARTITIONING


    def pullTo(self, graph2, nodeID):
        '''
        Removes nodeID from self and adds it to graph2
        '''
        d = self.nodes[nodeID]
        del self.nodes[nodeID]
        graph2.nodes[nodeID] = d
        return


    # def anyBipartition(self):
    #     # ! need to change to increase possible partition size
        
    #     for node in list(self.nodes.keys()):
    #         if self.canDelNode(node):
    #             result1 = self.slash([node])
    #             result2 = self.createView([node])
    #             return result1, result2
    #     print(self)
    #     raise Exception("No bipartition can be made")


    def anyBipartition(self):
        if self.isConnected():
            # print("calling anyBipartition on a connected graph")
            # naive approach, trying all possible combinations
            size = 1
            while size <= (1/2) * len(self.nodes):
                for partition in combinations(self.nodes.keys(), size):
                    result1 = self.slash(partition)
                    result2 = self.createView(partition)
                    # print(result1)
                    # print(result2)
                    if result1.isConnected() and result2.isConnected():
                        # print("done")
                        return result1, result2
                size += 1

        else:
            # print("calling anyBipartition on an unconnected graph")
            # find two connected components that form a feasible bipartition
            # ? Can be improved by assuming only 2 components exist ?
            goalWeight = self.weight()
            components = self.findAllConnectedComponents()
            for comp in components:
                for othercomp in components:
                    if (comp != othercomp) and (comp.weight() + othercomp.weight() == goalWeight):
                        # print("done")
                        return comp, othercomp
                

        print(self)
        raise Exception("Can't find any feasible bipartition")





    def pull1(self, V1, graphWeight):
        '''
        PULL-1
        '''
        V1Weight = V1.weight()
        if (V1Weight < (3/8) * graphWeight):
            V2 = self
            ignoreList = set()
            while 1:
                u, uWeight = V2.getLightestNode(ignoreList)
                if u == "not set":
                    return False
                if (V1Weight + uWeight < V2.weight()) and V2.isFeasible(u, V1):
                    V2.pullTo(V1, u)
                    return True
                else:
                    ignoreList.add(u)


    def pull2(self, V1, graphWeight, v2):
        '''
        PULL-2
        '''
        V2 = self
        if (V2.weight() > (1/2) * graphWeight):
            sortedList = list(sorted(self.nodes.keys(), reverse=False))
            for u in sortedList: # ? Changing order of nodes affects final partition
                if (u != v2) and V2.isFeasible(u, V1):
                    uWeight = V2.nodes[u]['weight']
                    if (V1.weight() + uWeight <= V2.weight() - uWeight):
                        V2.pullTo(V1, u)
                        return True, u
                    else:
                        lastcheckedU = u
            return False, lastcheckedU





    ############################################################################
    # CONNECTIVITY


    def isConnected(self):
        '''
        Returns true or false, uses a non-recursive dfs
        '''
        goal = len(self.nodes)
        firstNode = next(iter(self.nodes))
        visited = set()
        g = set(self.nodes.keys())
        self.dfsNonRecursive(visited, firstNode, g)
        if (len(visited) == goal):
            return True
        return False


    def isFeasible(self, u, V1):
        '''
        Returns true/false whether the partition V1 + u, V2 - u is feasible
        '''
        V2 = self
        return (V2.canAddNode(u, V1) and V2.canDelNode(u))


    def canAddNode(self, node, graph):
        '''
        Returns true or false if a node can be added to a graph while maintaining connectivity
        '''
        # * Built to reduce need for dfs connectivity check
        for neighbour in self.nodes[node]['edges']:
            if neighbour in graph.nodes:
                return True
        return False


    def canDelNode(self, node):
        d = self.nodes[node]
        del self.nodes[node]
        if self.isConnected():
            result = True
        else:
            result = False
        self.nodes[node] = d
        return result


    def dfsNonRecursive(self, visited, node, g):
        '''
        Non-recursive depth first search
        '''
        if node not in visited and node in g:
            toVisit = set()
            toVisit.add(node)
            visited.add(node)
 
            while (toVisit):
                n = toVisit.pop()
    
                if (n not in visited):
                    visited.add(n)
    
                for neighbour in self.nodes[n]['edges']:
                    if (neighbour in g and neighbour not in visited):
                        toVisit.add(neighbour) 


    def findConnectedComponent(self, start):
        '''
        Uses dfs to return a new graph of nodes that can be reached from the start node
        '''
        visited = set()
        component = Graph({start: self.nodes[start]})
        self.dfsComponent(start, visited, component)
        return component


    def dfsComponent(self, node, visited, component):
        toVisit = set()
        toVisit.add(node)
        while (toVisit):
            n = toVisit.pop()

            if (n not in visited):
                visited.add(n)
                component.nodes[n] = self.nodes[n]

            for neighbour in self.nodes[n]['edges']:
                if (neighbour in self.nodes and neighbour not in visited):
                    toVisit.add(neighbour)


    ############################################################################
    # BI-CONNECTIVITY


    def is2Connected(self):
        # adapted from python package 'networkx'
        bcc = self.getBicomponents()
        if len(bcc) == 1:
            return len(bcc[0].nodes) == len(self.nodes)
        return False


    def getBicomponents(self):
        # adapted from python package 'networkx'
        components = []
        for comp in self.biconnectedDfs(components=True):
            component = Graph({})
            for node in set(chain.from_iterable(comp)):
                try:
                    component[node] = self.nodes[node]
                except:
                    pass
            components.append(component)
        return components


    def cutVerticies(self):
        # adapted from python package 'networkx'
        seen = set()
        for articulation in self.biconnectedDfs(components=False):
            if articulation not in seen:
                seen.add(articulation)
                # print(articulation)
        return seen


    def biconnectedDfs(self, components=True):
        # adapted from python package 'networkx'
        visited = set()
        for start in self.nodes:
            if start in visited:
                continue
            discovery = {start: 0}  # time of first discovery of node during search
            low = {start: 0}
            root_children = 0
            visited.add(start)
            edge_stack = []
            stack = [(start, start, iter(self.nodes[start]['edges']))]
            while stack:
                grandparent, parent, children = stack[-1]
                try:
                    child = next(children)
                    if grandparent == child:
                        continue
                    if child in visited:
                        # This try/except was added by me, TESTING RESULTS?
                        try: 
                            if discovery[child] <= discovery[parent]:  # back edge
                                low[parent] = min(low[parent], discovery[child])
                                if components:
                                    edge_stack.append((parent, child))
                        except:
                            pass
                    else:
                        low[child] = discovery[child] = len(discovery)
                        visited.add(child)
                        try:
                            stack.append((parent, child, iter(self.nodes[child]['edges'])))
                        except:
                            pass
                        if components:
                            edge_stack.append((parent, child))
                except StopIteration:
                    stack.pop()
                    if len(stack) > 1:
                        if low[parent] >= discovery[grandparent]:
                            if components:
                                ind = edge_stack.index((grandparent, parent))
                                yield edge_stack[ind:]
                                edge_stack = edge_stack[:ind]
                            else:
                                yield grandparent
                        low[grandparent] = min(low[parent], low[grandparent])
                    elif stack:  # length 1 so grandparent is root
                        root_children += 1
                        if components:
                            ind = edge_stack.index((grandparent, parent))
                            yield edge_stack[ind:]
            if not components:
                # root node is articulation point if it has more than 1 child
                if root_children > 1:
                    yield start


    ############################################################################
    # NOT IN USE


    # def anyBipartition(self):
    #     '''
    #     Attempts to make any feasible bipartition
    #     Returns V1 (containing a single node) and V2
    #     '''
    #     for node in self.nodes:
    #         u = self.newPartition(node)
    #         if u:
    #             return u 
    #     raise Exception("No bipartition can be made")


    # def newPartition(self, nodeID, dontDelete=False):
    #     '''
    #     Removes nodeID from current graph and returns a new graph with the single node
    #     '''
    #     if dontDelete:
    #         d = self.nodes[nodeID]
    #         return Graph({nodeID:d})

    #     success, d = self.delNode(nodeID)
    #     if success:
    #         return Graph({nodeID: d})
    #     else:
    #         return False


    # def isFeasible(self, u, V1):
    #     '''
    #     Returns true/false whether the partition V1 + u, V2 - u is feasible
    #     '''
    #     V2 = self
    #     success, d = V2.delNode(u)
    #     if success:
    #         # undo it
    #         V2.nodes[u] = d
    #         if V2.canAddNode(u, V1):
    #             return True
    #     return False


    # def delNode(self, nodeID):
    #     '''
    #     Removes a node from the graph, only if the resulting graph is connected
    #     Returns:
    #         1. True/False if operation succeeded
    #         2. the dict entry of the removed node
    #     '''
    #     d = self.nodes[nodeID]
    #     del self.nodes[nodeID]
    #     # ? is it possible to check if a node can be removed without dfs?
    #     if self.isConnected():
    #         return True, d
    #     else:
    #         self.nodes[nodeID] = d
    #         return False, d

    ############################################################################
    # work in progress / currently testing:
    # NOTES:
    # - 

    def findAllConnectedComponents(self):
        compList = []
        visited = set()
        for vertex in self.nodes:
            if vertex not in visited:
                component = Graph({vertex: self.nodes[vertex]})
                self.dfsComponent(vertex, visited, component)
                compList.append(component)
        return compList


    def getBicomponentsNodes(self):
        # adapted from python package 'networkx'
        components = []
        for comp in self.biconnectedDfs(components=True):
            components.append(set(chain.from_iterable(comp)))
        return components


    def nodeView(self):
        result = set()
        for node in self.nodes:
            result.add(node)
        return result


    def getHeaviestNode(self, ignoreList=set()):
        '''
        Returns the id of the heaviest node
        '''
        heavyWeight = -1
        for node in self.nodes:
            if (self.nodes[node]['weight'] > heavyWeight) and (node not in ignoreList):
                heavyWeight = self.nodes[node]['weight']
                heavyNode = node
        return heavyNode


    def removeUnionEdges(self, comp1, comp2):
        '''
        Removes all the edges in union, returns them as a set of tuples?
        '''
        toRemove = set()
        for node in comp1.nodes:
            for edge in comp1.nodes[node]['edges']:
                if edge in comp1.nodes:
                    toRemove.add((node, edge))

        for node in comp2.nodes:
            for edge in comp2.nodes[node]['edges']:
                if edge in comp2.nodes:
                    toRemove.add((node, edge))

        for tup in toRemove:
            self.nodes[tup[0]]['edges'].remove(tup[1])

        return toRemove


    def delEdges(self, edgesToDel):
        for tup in edgesToDel:
            if tup[0] in self.nodes:
                if tup[1] in self.nodes[tup[0]]['edges']:
                    self.nodes[tup[0]]['edges'].remove(tup[1])


    def reAddEdges(self, edgesToAdd):
        for tup in edgesToAdd:
            if tup[0] in self.nodes:
                if tup[1] not in self.nodes[tup[0]]['edges']:
                    self.addEdge(tup[0], tup[1])


    def overLayVertex(self, vert1, vert2):
        '''
        overlaps vert1 onto vert2
        '''
        # ignore the weight of vert2 because it should already have been added to vert1


        vert2Edges = set(self.nodes[vert2]['edges'])
        if vert1 in vert2Edges:
            vert2Edges.remove(vert1)
        vert1Edges = set(self.nodes[vert1]['edges'])
        newGraph = self.slash([vert2])

        newEdges = vert1Edges.union(vert2Edges)


        self.nodes[vert1]['edges'] = list(newEdges)




        addedEdges = set()
        for edge in vert2Edges.difference(vert1Edges):
            addedEdges.add((vert1,edge))


        for node in newGraph.nodes:
            edgeSet = set(newGraph.nodes[node]['edges'])
            if vert2 in edgeSet and node not in vert1Edges and node != vert1:
                edgeSet.add(vert1)
                self.nodes[node]['edges'] = list(edgeSet)
                addedEdges.add((node, vert1))

        return newGraph, addedEdges
        # all thats left to repair the graph is to remove all edges from v1 that occur in v2


    def pull3(self, V2):
        V3 = self

        if V3.weight() > ((1/2) * V3.union(V2).weight()):
            ignoreList = set()
            while 1:
                u, uWeight = V3.getLightestNode(ignoreList)
                if u == "not set":
                    return False, V2, V3

                if V3.createView([u]).isAdjacentTo(V2):
                    # found u
                    if V3.slash([u]).isConnected():
                        U = V3.createView([u])
                    else:
                        count, compList = V3.slash([u]).countAdjacentComps(V2)
                        if count == 0:
                            U_prime = V3.slash([u]).heaviestComp()
                            U = V3.slash(U_prime)
                        elif count == 1:
                            U_prime = compList.pop()
                            if U_prime.weight() < V3.slash(U_prime).weight():
                                U = U_prime
                            else:
                                U = V3.slash(U_prime)
                        elif count > 1:
                            weight = float('inf')
                            for comp in compList:
                                if comp.weight() < weight:
                                    weight = comp.weight()
                                    U = comp
                            if U.weight() > (1/2) * V3.weight():
                                raise Exception("Error here")
                        
                    if V2.weight() + U.weight() <= V3.weight():
                        # Pull happens here
                        V2 = V2.union(U)
                        V3 = V3.slash(U)
                        return True, V2, V3
                    else:
                        return False, V2, V3

                else:
                    ignoreList.add(u)
        else:
            return False, V2, V3




    def isAdjacentTo(self, rightGraph):
        leftGraph = self
        for node in leftGraph:
            for edge in leftGraph.nodes[node]['edges']:
                if edge in rightGraph:
                    return True
        return False

    def countAdjacentComps(self, rightGraph):
        # returns an int of the number of components in self that are adjacent to rightGraph
        count = 0
        compList = []
        for comp in self.findAllConnectedComponents():
            if comp.isAdjacentTo(rightGraph):
                count += 1
                compList.append(comp)
        return count, compList


    def heaviestComp(self):
        weight = -1
        result = None
        for comp in self.findAllConnectedComponents():
            if comp.weight() > weight:
                weight = comp.weight()
                result = comp
        return result

    def lightestComp(self):
        weight = float('inf')
        result = None
        for comp in self.findAllConnectedComponents():
            if comp.weight() < weight:
                weight = comp.weight()
                result = comp
        return result


    def pull2NEW(self, V1, graphWeight, v2):
        '''
        PULL-2
        '''
        V2 = self
        if (V2.weight() > (4/5) * graphWeight):
            sortedList = list(sorted(self.nodes.keys(), reverse=False))
            for u in sortedList: # ? Changing order of nodes affects final partition
                if (u != v2) and V2.isFeasible(u, V1):
                    uWeight = V2.nodes[u]['weight']
                    if (V1.weight() + uWeight <= V2.weight() - uWeight):
                        V2.pullTo(V1, u)
                        return True, u
                    else:
                        lastcheckedU = u
            return False, lastcheckedU



    def bfs(self, v1, v2, v3):
        V1 = Graph({})
        V2 = Graph({})
        V3 = Graph({})
        queue = []
        queue.append(v1)
        visited = set()
        visited.add(v1)
        parent = {v1:v1}
        while queue != []:
            node = queue.pop(0)
            if node == v1:
                V1.addVertex(node, self.nodes[node]['edges'], self.nodes[node]['weight'])
            elif node == v2:
                V2.addVertex(node, self.nodes[node]['edges'], self.nodes[node]['weight'])
            elif node == v3:
                V3.addVertex(node, self.nodes[node]['edges'], self.nodes[node]['weight'])
            else:
                if parent[node] in V1.nodes:
                    V1.addVertex(node, self.nodes[node]['edges'], self.nodes[node]['weight'])
                elif parent[node] in V2.nodes:
                    V2.addVertex(node, self.nodes[node]['edges'], self.nodes[node]['weight'])
                else:
                    V3.addVertex(node, self.nodes[node]['edges'], self.nodes[node]['weight'])
                                                
            for edge in self.nodes[node]['edges']:
                if edge not in visited and edge in self.nodes:
                    visited.add(edge)
                    queue.append(edge)
                    parent[edge] = node
        return V1, V2, V3
    ############################################################################


if __name__ == "__main__":
    from graph_partition.classes.instanceManager import readInstance
    import time

    ##################################
    Instance_Name = "bfscheck"
    #################################

    Folder_Name = "all-instances/local_testing"
    File_Extension = ".in"
    path = '../{}/{}{}'.format(Folder_Name, Instance_Name, File_Extension)
    graph = readInstance(path)

    print(graph.nodeView())
    V1, V2, V3 = graph.bfs(1,0,6)
    print("V1 =", V1.nodeView())
    print("V2 =", V2.nodeView())
    print("V3 =", V3.nodeView())



    # print(len(graph.findAllConnectedComponents()))
    # for comp in graph.findAllConnectedComponents():
    #     print(comp)



    # bicomps = len(graph.getBicomponents())
    # print("how many bicomponents are there?", bicomps)
    # print(len(graph.getBicomponents()))
    # for comp in graph.getBicomponentsNodes():
    #     print(comp)

    # newgraph, oldEdges = graph.overLayVertex(4, 5)
    # graph.repairGraph(oldEdges)
    # print(graph)
    # new = graph.slash([1])
    # print("new =", new)
    # print("graph =", graph)

    # new.addVertex(10, [8], 5)
    # new.addEdge(8,10)
    # print("new =", new)
    # print("graph =", graph)
    # edges = graph.removeEdges()
    # print(edges)
    # print(graph)
    # print("repairing")
    # graph.repairEdges(edges)
    # print(graph)

    # newgraph = Graph()
    # newgraph.addVertex(1, [2,3], 98)
    # newgraph.addVertex(2, [1,3], 98)
    # newgraph.addVertex(3, [1,2], 97)

    # print("\n")
    # print(newgraph.getHeaviestNode([newgraph.getHeaviestNode()]))