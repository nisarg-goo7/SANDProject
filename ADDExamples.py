from sand.add import ADD 
import logging, csv

def method0():
    print("=======================================")
    cost = [[2,1,2,4],
            [1,0,1,2],
            [4,1,2,2],
            [1,2,1,2],
            [2,3,2,0],
            [4,4,3,2]]
    Ccost = [0,2,2,2]
    weight = [1] * 6
    algo = ADD(cost, Ccost, weight, Wlimit=3)
    assoc = algo.run()
    print(assoc)

    
def method1():
    print("======= Book example pp 230 =========")
    csvfile = open('cost_matrix.txt', 'r')
    data = csv.reader(csvfile, delimiter=' ')
    cost = []
    for row in data:
        nums = []
        for n in row:
            nums.append(eval(n))
        cost.append(nums)

    nt = len(cost)
    nc = len(cost[0])
    center = 0
    Wlimit = 3
    th_move = 0
    weight = [1] * nt
    Ccost = [line[0] for line in cost]
    Ccost.insert(0,0)
    print(Ccost)
    algo = ADD(cost, Ccost, weight, Wlimit=3)
    assoc = algo.run()
    print(assoc)

def method2():        
    print("=======================================")
    csvfile = open('cost_mat.txt', 'r')
    data = csv.reader(csvfile, delimiter=' ')
    cost = []
    for row in data:
        nums = []
        for n in row:
            nums.append(eval(n))
        cost.append(nums)

    nt = len(cost)
    nc = len(cost[0])
    weight = [1] * nt
    Ccost = [50] * (nc + 1)
    Ccost[0] = 0
    print(Ccost)
    algo = ADD(cost, Ccost, weight)
    assoc = algo.run()
    print(assoc)

def method3():
    import math
    import networkx as nx
    import matplotlib.pyplot as plt

    print("======= Simulating PON ================")  
    numHouses = 256
    housePerRow = 16
    splitterSize = 16
    houseSpacing = 50
    dMax = splitterSize * houseSpacing
    
    # ############ create house positions
    pos = {}
    for i in range(numHouses):
        pos[i] = ((i % housePerRow), (i // housePerRow))

    # ############ initialize a cost matrix
    cost = [[0 for i in range(numHouses)] for i in range(numHouses)]
    for i in range(numHouses):
        for j in range(i, numHouses):
            r1, c1 = pos[i]
            r2, c2 = pos[j]
            #d = round(math.sqrt(((r1-r2)*houseSpacing)**2 + ((c1-c2)*houseSpacing)**2))
            d = abs(r1-r2)*houseSpacing + abs(c1-c2)*houseSpacing
            if(d > dMax): # cost prohibitive
                d = 2**32-1
            cost[i][j] = cost[j][i] = d

    # ############ add the cost of connecting directly to centre 
    pos[numHouses]= (housePerRow*houseSpacing/2, housePerRow*houseSpacing/2)
    for row in cost:
        row.append(2*dMax)
        #row.insert(0, 2*dMax)
    weight = [1] * numHouses
    Ccost = [2*dMax] * (numHouses + 1)

    # ############ run the algorithm
    algo = ADD(cost, Ccost, weight, center=numHouses, Wlimit=splitterSize)
    out = algo.run()
    splitterSet = set(out["assoc"])
    numSplitter = len(splitterSet)
    houseAssoc = [out["assoc"].count(i) for i in splitterSet] 
    print("Number of splitters =", numSplitter)
    print("Number of houses per splitter =", houseAssoc)
    print("Cost =", out["cost"])

    # ############ create graph
    G=nx.Graph()
    G.add_nodes_from(range(numHouses))
    edges = [(k, out["assoc"][k]) for k in range(numHouses)]
    G.add_edges_from(edges)

    # ##### Plot graph
    plt.figure(figsize=(6, 6))
    nx.draw_networkx_nodes(G,pos, node_size=10)
    nx.draw_networkx_nodes(G,pos,nodelist=splitterSet,node_size=60,alpha=0.4, node_color="green")    
    nx.draw_networkx_edges(G,pos,nodelist=splitterSet,alpha=0.2, node_color="black")
    
#    plt.xlim(-1,housePerRow)
#    plt.ylim(-1,numHouses // housePerRow)
    plt.title("PON Design")
    plt.axis('off')
    plt.show()

def method4():
    import math, random
    import networkx as nx
    import matplotlib.pyplot as plt

    print("======= Random Graph ================")  
    numNodes = 250

    G=nx.Graph()
    G.add_nodes_from(range(numNodes))
    pos = {}
    for i in range(numNodes):
        pos[i] = (random.random() , random.random())

    # ############ initialize a cost matrix
    cost = [[2**16-1 for i in range(numNodes)] for i in range(numNodes)]
    for i in range(numNodes):
        for j in range(i, numNodes):
            r1, c1 = pos[i]
            r2, c2 = pos[j]
            d = round(math.sqrt(abs(r1-r2) + abs(c1-c2)) * 1000)
            cost[i][j] = cost[j][i] = d

    # find node near center (0.5,0.5)
    dmin=1
    ncenter=0
    for n in pos:
        x,y=pos[n]
        d=(x-0.5)**2+(y-0.5)**2
        if d<dmin:
            ncenter=n
            dmin=d

    print("Centre =",ncenter)
    # ############ run the algorithm
    Ccost = [0] * numNodes
    for i in range(numNodes):
        Ccost[i] = cost[i][ncenter] + 100
    Ccost[ncenter] = 0
    weight = [1] * numNodes

    algo = ADD(cost, Ccost, weight, center=ncenter)
    out = algo.run()
    concSet = set(out["assoc"])
    numConc = len(concSet)
    nodeAssoc = [out["assoc"].count(i) for i in concSet] 
    print("Number of concentrators =", numConc)
    print("Number of nodes per concentrators =", nodeAssoc)
    print("Cost =", out["cost"])

    edges = [(k, out["assoc"][k]) for k in range(numNodes)]
    # color by path length from node near center
    p=nx.single_source_shortest_path_length(G,ncenter)

    plt.figure(figsize=(6,6))
    nx.draw_networkx_edges(G,pos,alpha=0.1)
    nx.draw_networkx_edges(G,pos,edgelist=edges,alpha=0.5)
    nx.draw_networkx_nodes(G,pos,nodelist=[ncenter],node_size=100, node_color="blue")
    nx.draw_networkx_nodes(G,pos,nodelist=concSet,node_size=50, node_color="green", alpha=0.4)
    nx.draw_networkx_nodes(G,pos,node_size=10)

    plt.xlim(-0.05,1.05)
    plt.ylim(-0.05,1.05)
    plt.axis('off')
    plt.savefig('ADD_in_Random_Graph.png')
    plt.show()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    #method0()
    #method1()   
    #method2()
    #method3()  #PON
    method4()
