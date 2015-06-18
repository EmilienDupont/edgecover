#!/usr/bin/python

from gurobipy import *

vertices  = range(5)
edges     = [(0, 1), (1, 2), (3, 4), (0, 2), (1, 3)] # Maybe better to write this as list of lists (as this is what you will get from d3...)

def optimize(vertices, edges):
    m = Model()
    vertexIndicator = {}
    edgeVars = {}
    
    # The input you get from the jsdict is a list of lists and not tuples
    for i in range(0,len(edges)):
        edges[i] = tuple(edges[i])
    
    print edges
        
    for edge in edges:
        edgeVars[edge] = m.addVar(vtype=GRB.BINARY,obj=1.0)
    
    # Check if v is in edge e
    for v in vertices:
        for e in edges:
            if e[0] == v or e[1] == v:
                vertexIndicator[(e,v)] = 1
            else:
                vertexIndicator[(e,v)] = 0

    m.update()
    
    m.setObjective(quicksum(edgeVars[edge] for edge in edges))

    for v in vertices:
        m.addConstr(quicksum(vertexIndicator[(e,v)]*edgeVars[e] for e in edges) >= 1)

    m.update()
    m.write('test.lp')
    m.optimize()

    cover = []

    for edge in edges:
        if edgeVars[edge].X > 0.5:
            print 'Edge', edge, 'is in the cover'
            cover.append(edge)

    return cover

if __name__ == '__main__':
    cover = optimize(vertices, edges)
