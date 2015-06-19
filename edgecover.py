#!/usr/bin/python

from gurobipy import *

vertices  = range(5)
edges     = [(0, 1), (1, 2), (3, 4), (0, 2), (1, 3)]

def optimize(vertices, edges):
    m = Model()
    edgeIn   = { v:[] for v in vertices }
    edgeOut  = { v:[] for v in vertices }
    edgeVars = {}

    edges = [ tuple(e) for e in edges ]
    print 'edges', edges

    for edge in edges:
        u = edge[0]
        v = edge[1]
        xe  = m.addVar(vtype=GRB.BINARY,obj=1.0, name="x_%d_%d" % (u,v))
        edgeVars[edge] = xe
        edgeOut[u] = edgeOut[u] + [xe]
        edgeIn[v] = edgeIn[v] + [xe]

    m.update()

    for v in vertices:
        m.addConstr(quicksum(edgeOut[v]) + quicksum(edgeIn[v]) >= 1, name="v%d" % v)

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
