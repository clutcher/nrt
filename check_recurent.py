x = 1
y = 2
def numberOfEdgesAndNodes(n):
    numberOfEdges = []
    numberOfEdges.append(1)

    if (x+y) == 3:
        for i in xrange(1, n):
            numberOfEdges.append(numberOfEdges[-1]*(x+y))
    else:
        for i in xrange(1, n):
            numberOfEdges.append(numberOfEdges[-1]*(x+y))

    numberOfNodes = []
    numberOfNodes.append(2)
    for i in xrange(1,n):
        numberOfNodes.append(numberOfNodes[-1] + numberOfEdges[i-1]*(x+y-2))
    return numberOfNodes, numberOfEdges

def numberOfEdgesAndNodesRozenfeld(n):
    numberOfEdges = []
    numberOfEdges.append(1)

    for i in xrange(1, n):
        numberOfEdges.append((x+y)**i)

    numberOfNodes = []
    numberOfNodes.append(2)
    for i in xrange(1,n):
        numberOfNodes.append((x+y)*numberOfNodes[-1] - (x+y))
    return numberOfNodes, numberOfEdges

print numberOfEdgesAndNodes(15)
print numberOfEdgesAndNodesRozenfeld(15)