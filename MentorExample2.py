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


# This is an example of using the MENTOR Algorithm in designing a backbone
# network.

  
from sand.mentor import *
import math, random

numNodes = 14
# Node labels:
labels = range(numNodes)

# Node positions:
pos = {}
pos[0] = (0,0) #A
pos[1] = (5,0) #B
pos[2] = (13,0) #C
pos[3] = (2,4) #D
pos[4] = (7,3) #E
pos[5] = (12,4) #F
pos[6] = (2,7) #G    
pos[7] = (8,7) #H
pos[8] = (13,7) #I
pos[9] = (4,9) #J
pos[10] = (0,11) #K
pos[11] = (8,11) #L
pos[12] = (13,10) #M
pos[13] = (10,1) #N
for p in pos:
    pos[p] = (pos[p][0]/13, pos[p][1]/13)

# Set cost matrix:
cost = [[2**16-1 for j in range(numNodes)] for i in range(numNodes)]
for i in range(numNodes):
    for j in range(i, numNodes):
        r1, c1 = pos[i]
        r2, c2 = pos[j]
        d = round(math.sqrt((r1-r2)**2 + (c1-c2)**2) * 100) # in dollars
        cost[i][j] = cost[j][i] = d

# Set traffic requirements matrix:
req = [[0 for j in range(numNodes)] for i in range(numNodes)]
req[0][1] = req[1][0] = 5       #A,B
req[0][3] = req[3][0] = 2       #A,D
req[0][10] = req[10][0] = 5     #A,K
req[1][13] = req[13][1] = 5     #B,N   
req[2][5] = req[5][2] = 2       #C,F
req[2][13] = req[13][2] = 2     #C,N
req[3][4] = req[4][3] = 10      #D,E
req[3][6] = req[6][3] = 10      #D,G
req[3][7] = req[7][3] = 2       #D,H
req[4][7] = req[7][4] = 10      #E,H
req[4][13] = req[13][4] = 2     #E,N    
req[5][7] = req[7][5] = 2       #F,H
req[5][8] = req[8][5] = 5       #F,I
req[5][13] = req[13][5] = 5     #F,N
req[6][9] = req[9][6] = 10      #G,J
req[7][8] = req[8][7] = 10      #H,I
req[7][9] = req[9][7] = 2       #H,J
req[8][11] = req[11][8] = 10    #I,L
req[8][12] = req[12][8] = 5     #I,M
req[9][10] = req[10][9] = 2     #J,K
req[9][11] = req[11][9] = 10    #J,L
req[10][11] = req[11][10] = 5   #K,L
req[11][12] = req[12][11] = 5   #L,M

# Call MENTOR algorithm:
algo = MENTOR()
out = algo.run(cost, req, wparm=0, rparm=1, alpha=0, cap=10, slack=0.2)

# Print results:
printCost(out, cost, labels)
plotNetwork(out, pos, labels, title="MENTOR Algorthim - Example #2")
    

