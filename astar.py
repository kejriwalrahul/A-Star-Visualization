# Usage: ./run [name_of_graph_file] [init_node] [term_node]
# You can use gen_graph.py with a parameter n to create an n*n grid graph

import graphviz
import math
import heapq
import sys
from vis_framework import Graph
import subprocess

def readGraph(fname):
    gv = open(fname)

    g = Graph("Haha", "neato")

    for line in gv:
        vals = line.split()
        if vals[0] not in g.nodes:
            g.node(vals[0], pos=vals[0], shape="circle", width="0.3", label="")
        if vals[1] not in g.nodes:
            g.node(vals[1], pos=vals[1], shape="circle", width="0.3", label="")
        g.edge(g[vals[0]], g[vals[1]], vals[2], label=str(vals[2]))

    return g

def hxy(p1,p2):
    # print p1.val
    # print p2.val
    x,y = p1.val.split(',')
    x2,y2 = p2.val.split(',')

    x,y,x2,y2 = int(x),int(y),int(x2),int(y2)
    # print x,x2,y,y2

    return 3*(math.fabs(x-x2) + math.fabs(y-y2))
    # return 4 *math.sqrt((x-x2)**2 + (y-y2)**2)

def print_path(parent,t,node_list):
    if t != None:
        print_path(parent,parent[t],node_list)
        print t.val
        node_list.append(t.val)
    else:
        return

def astar(graph,start,dest):
    graph.start=start
    graph.dest=dest
    graph.dir = 'astar/'
    print "\nA*:"
    count = 0
    graph.show([],[])
    s,t = graph[start],graph[dest]

    toexplore = []
    n = len(graph.nodes)
    heapq.heappush(toexplore,(0,n,s))

    parent = {}
    costCurrent = {}
    parent[s] = None
    costCurrent[s] = 0
    known = []
    while toexplore:
        count += 1
        _,_,current = heapq.heappop(toexplore)
        known.append(current)
        if current == t:
            node_list = []
            print_path(parent,t,node_list)
            graph.display_path(node_list)
            break

        for e in current.adjList:
            adj = e.neighbour(current)
            wt = e.wt
            newCost = costCurrent[current] + int(wt)

            if adj not in costCurrent or newCost < costCurrent[adj]:
                costCurrent[adj] = newCost
                parent[adj] = current
                priority = newCost + hxy(t,adj)
                heapq.heappush(toexplore,(priority,n-count,adj))

        partial = []
        for _,_,temp in toexplore:
            partial.append(temp)
        graph.show(known, partial)

    print "Count %d"%count
    return count


def djikstra(graph,start,dest):
    print "\nDjikstra:"
    graph.dir = 'djikstra/'
    count = 0
    graph.start=start
    graph.dest=dest
    s,t = graph[start],graph[dest]

    toexplore = []
    heapq.heappush(toexplore,(0,s))

    parent = {}
    costCurrent = {}
    parent[s] = None
    costCurrent[s] = 0
    known = []
    while toexplore:
        count += 1
        _,current = heapq.heappop(toexplore)
        known.append(current)
        if current == t:
            node_list = []
            print_path(parent,t,node_list)
            graph.display_path(node_list)
            break

        for e in current.adjList:
            adj = e.neighbour(current)
            wt = e.wt
            newCost = costCurrent[current] + int(wt)

            if adj not in costCurrent or newCost < costCurrent[adj]:
                costCurrent[adj] = newCost
                parent[adj] = current
                priority = newCost #+ hxy(t,adj)
                heapq.heappush(toexplore,(priority,adj))

        partial = []
        for _,temp in toexplore:
            partial.append(temp)
        graph.show(known, partial)
    # graph.makeGif('djikstra.gif')
    print "Count %d"%count
    return count

def greedybfs(graph,start,dest):
    print "\nGreedy BFS"
    graph.dir = 'bfs/'
    count = 0
    graph.start=start
    graph.dest=dest
    s,t = graph[start],graph[dest]

    toexplore = []
    heapq.heappush(toexplore,(0,s))

    parent = {}
    parent[s] = None
    known = []
    while toexplore:
        count += 1
        _,current = heapq.heappop(toexplore)
        known.append(current)
        if current == t:
            node_list = []
            print_path(parent,t,node_list)
            graph.display_path(node_list)
            break

        for e in current.adjList:
            adj = e.neighbour(current)
            wt = e.wt
            if adj not in parent:
                parent[adj] = current
                priority = hxy(t,adj)
                heapq.heappush(toexplore,(priority,adj))

        partial = []
        for _,temp in toexplore:
            partial.append(temp)
        graph.show(known, partial)
    # graph.makeGif('bfs.gif')
    print "Count %d"%count
    return count
try:
    g1 = readGraph(sys.argv[1])
    c1 = astar(g1,sys.argv[2],sys.argv[3])

    g2 = readGraph(sys.argv[1])
    c2 = djikstra(g2,sys.argv[2],sys.argv[3])

    g3 = readGraph(sys.argv[1])
    c3 = greedybfs(g3,sys.argv[2],sys.argv[3])
except Exception:
    sys.exit("Error: Incorrect usage \nUsage: ./run [name_of_graph_file] [init_node] [term_node]")

g1.makeGif('gifs/astar.gif', max(c1,c2,c3)-c1)
g2.makeGif('gifs/djikstra.gif', max(c1,c2,c3)-c2)
g3.makeGif('gifs/greedybfs.gif', max(c1,c2,c3)-c3)

subprocess.call('google-chrome ./output/view.html', shell=True)
