from graph_partition import Graph, algorithms, readInstance
import time

# For a simple, command-line interface, install the package using pip and run the command "partition" in a terminal.

# Can create a graph like this:
testGraph = Graph()
testGraph.addVertex(1, [2,3], 98)
testGraph.addVertex(2, [1,3], 98)
testGraph.addVertex(3, [1,2], 97)

# Or read a graph instance like this:
##################################
path = "graph_partition/test-instances/gg_05_05_a_1.in"
#################################
graph = readInstance(path)


# Running and timing an algorithm:
start = time.time()
V1, V2 = algorithms.approx1(testGraph)
end = time.time()

# Printing results
print("Time taken =", end-start, "seconds")
print("V1 weight =", V1.weight())
print("V2 weight =", V2.weight())
