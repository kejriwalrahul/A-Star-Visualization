import graphviz
import time, os, sys
from images2gif import writeGif
from PIL import Image
from datetime import datetime
from stat import S_ISREG, ST_CTIME, ST_MODE

class Graph(graphviz.Graph):

    def __init__(self, comment, engine, display_delay=0.5):
        super(Graph, self).__init__(comment=comment, engine=engine, format="gif")
        self.nodes = {}
        self.display_delay = display_delay

    def node(self, val, **kwargs):
        super(Graph, self).node(val, **kwargs)
        Node(val, self)

    def edge(self, n1, n2, wt, **kwargs):
        super(Graph, self).edge(n1.val, n2.val, **kwargs)
        Edge(n1,n2,wt)

    def show(self, known, toexplore):

        for n in toexplore:
            super(Graph, self).node(n.val, style="filled", fillcolor="blue", pos=str(n.val), shape="circle", width="0.3", label="")

        for n in known:
            super(Graph, self).node(n.val, style="filled", fillcolor="red", pos=str(n.val), shape="circle", width="0.3", label="")

        super(Graph, self).node(self.start, pos=self.start, style="filled", fillcolor="green", shape="circle", width="0.3", label="")
        super(Graph, self).node(self.dest, pos=self.dest, style="filled", fillcolor="green", shape="circle", width="0.3", label="")

        super(Graph, self).render(self.dir+str(datetime.now()))
        # time.sleep(self.display_delay)

    def display_path(self, node_list):
        for n in node_list:
            super(Graph, self).node(n, style="filled", fillcolor="green", pos=n, shape="circle", width="0.3", label="")

        super(Graph, self).render(self.dir+str(datetime.now()))

    def makeGif(self, filename, padding):
    	entries = (os.path.join(self.dir,fn) for fn in os.listdir(self.dir) if fn.endswith('.gif'))
        entries = sorted(entries)
    	images  = [Image.open(fn) for fn in entries]
        for i in range(padding):
            images.append(Image.open(entries[-1]))
    	writeGif(filename, images, duration=self.display_delay, repeat=True)

    def __getitem__(self,val):
		return self.nodes[val]

class Node:
    def __init__(self,val,graph):
    	self.val = val
    	self.adjList = []
    	graph.nodes[val] = self

class Edge:
    def __init__(self,n1,n2,wt):
        self.node1 = n1
        self.node2 = n2
        self.wt = wt
        self.displayed = False
        n1.adjList.append(self)
        n2.adjList.append(self)

    def neighbour(self,n):
        if self.node1 == n:
            return self.node2
        return self.node1
