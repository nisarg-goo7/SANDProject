#!/usr/bin/env python

# Copyright (c) 2017 Maen Artimy
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# This file is part of the SAND library
 

import networkx as nx
import matplotlib.pyplot as plt

# print cost list of network produced by MENTOR algorithm
def printCost(out, cost, labels):   
    backbone = out["backbone"]
    mesh = out["mesh"]
    chlist = out["channels"]
    
    total = 0
    print('%4s%4s%4s%8s' % ('From','To','Ch','Cost($)'))
    print(('=' * 24))
    for i in range(len(mesh)):
        x, y = mesh[i]
        total += cost[x][y]*chlist[i]
        print('%4s%4s%4d%8d' % (labels[x], labels[y], chlist[i], cost[x][y]*chlist[i]))
    print(('=' * 24))
    print('%12s%8d' % ('Total cost',total))


def dispReq(G, pos, req):
    n = len(req)
    reqEdges = {(i,j):str(req[i][j]) for i in range(n) for j in range(n) if req[i][j] != 0}
    labels = {i:str(i) for i in range(n)}
    nx.draw_networkx_edges(G,pos,reqEdges.keys(),alpha=0.2)    
    nx.draw_networkx_nodes(G,pos,node_size=10, alpha=0.5)   # draw all nodes
    nx.draw_networkx_edge_labels(G,pos,reqEdges,font_size=12,font_color="red")   
    nx.draw_networkx_labels(G,pos,labels,font_size=14,font_color="black")

    mx = max(pos.values())
    mn = min(pos.values())    
    #plt.figure(figsize=(6,6))
    plt.xlim(mn[0]-1,mx[0]+2)
    plt.ylim(mn[1]-1,mx[1]+2)
    plt.axis('off')
    plt.savefig('MENTOR_Orig.png')
    plt.show()
    
# Plot topology produced by MENTOR algorithm
def plotNetwork(out, pos, labels=[], filename="figure.png", title='MENTOR Algorithm'):
    numNodes = len(pos)
    mesh = out["mesh"]
    ch = out["channels"]   
    backbone = out["backbone"]
    median = out["median"]
    tree = out["tree"]

    plt.figure(figsize=(6,6))
    G=nx.path_graph(numNodes)

    #nx.draw_networkx_edges(G,pos,alpha=0.1)
    #nx.draw_networkx_edges(G,pos,edgelist=edges,alpha=0.2)    
    nx.draw_networkx_edges(G, pos, mesh, alpha=0.3, edge_color="blue")
    nx.draw_networkx_edges(G, pos, edgelist=tree, width=2, edge_color="blue")
    
    # Draw all nodes 
    nx.draw_networkx_nodes(G, pos, node_size=10, node_color="green", alpha=0.5)
    nx.draw_networkx_nodes(G, pos, nodelist=[median], node_size=150, node_color="black")
    nx.draw_networkx_nodes(G, pos, nodelist=backbone, node_size=50, node_color="red")

    # Draw node and edge labels       
    elabels = {e:ch[mesh.index(e)] for e in mesh}
    nx.draw_networkx_edge_labels(G, pos, elabels, edgelist=mesh, font_size=10, font_color="grey")
    if labels:
        nLabel = {n:labels[n] for n in backbone}
        npos = {n:(pos[n][0], pos[n][1]+0.03) for n in pos}
        nx.draw_networkx_labels(G, npos, nLabel, nodelist=backbone, font_size=10, font_color="black")

    plt.xlim(-0.05,1.05)
    plt.ylim(-0.05,1.05)
    plt.axis('off')
    plt.title(title)
    plt.savefig(filename)
    plt.show()

