
def Dist(A):
    import numpy as np

    N=len(A)
    S=np.zeros((N,1))
    for i in range(N):
        S[i]=A[i,:].sum()-A[i,i]

    z=[i-0.5 for i in range(int(S.min()-1),int(S.max()+2))]

    h=np.histogram(S,z)
    n=len(h[0])
    L=np.zeros((n,2))

    for i in range(n):
        L[i,0]=(h[1][i]+h[1][i+1])/2
        L[i,1]=h[0][i]/float(N)


    Lx=L[:,0]
    Ly=L[:,1]

    Z=np.where(Ly<10**(-10))
    Z=np.array(Z)
    Lx1=np.delete(Lx,Z[0])
    Ly1=np.delete(Ly,Z[0])

    LL=np.column_stack((Lx1,Ly1))

    return LL

def DistV(K):
    import numpy as np

    N=len(K)

    z=[i-0.5 for i in range(int(min(K)-1),int(max(K)+2))]

    h=np.histogram(K,z)
    n=len(h[0])
    L=np.zeros((n,2))

    for i in range(n):
        L[i,0]=(h[1][i]+h[1][i+1])/2
        L[i,1]=h[0][i]/float(N)


    Lx=L[:,0]
    Ly=L[:,1]

    Z=np.where(Ly<10**(-10))
    Z=np.array(Z)
    Lx1=np.delete(Lx,Z[0])
    Ly1=np.delete(Ly,Z[0])

    LL=np.column_stack((Lx1,Ly1))

    return LL



