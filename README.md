# a-star-visualization
Project that shows execution paths for A-star search and compares with Greedy BFS and Djikstra

Usage:

	./run [name_of_graph_file] [init_node] [term_node]

Graph input format:

each line contains edges in the format:
x1,y1 x2,y2 edgeWt

where x1 and x2 are x- coordinates of nodes and y1 and y2 are y-coordinates
      edgeWt is the weight of the edge between them.
and all values are restricted to integers.

Note: Negative egdeWt not allowed.