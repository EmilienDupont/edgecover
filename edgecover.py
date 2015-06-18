#!/usr/bin/python

from gurobipy import *

vertices  = range(5)
edges     = [(0, 1), (1, 2), (3, 4), (0, 2), (1, 3)]


def optimize(vertices, edges):
    m = Model()
    vertexVars = {}

    for v in vertices:
        vertexVars[v] = m.addVar(vtype=GRB.BINARY,obj=1.0, name="x%d" % v)

    m.update()

    for edge in edges:
        u = edge[0]
        v = edge[1]
        xu = vertexVars[u]
        xv = vertexVars[v]
        m.addConstr(xu + xv >= 1, name="e%d-%d" % (u, v))

    m.update()
    m.write('test.lp')
    m.optimize()

    cover = []

    for v in vertices:
        if vertexVars[v].X > 0.5: # if value more than 1/2 must be 1 since binary
            print 'Vertex', v, 'is in the cover'
            cover.append(v)

    for edge in edges:
        u = edge[0]
        v = edge[1]
        print 'Edge (%d, %d)' % (u, v), vertexVars[u].X, vertexVars[v].X

    return cover

if __name__ == '__main__':
    cover = optimize(vertices, edges)
