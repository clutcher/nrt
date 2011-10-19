
import time

def SF(Niter,c, Nrealization):
    import numpy as np
    import random

    a=1
    tcut=25
    m0=20

    c=float(c)


    for j in range(Nrealization):

        K=[0]*(m0+Niter+1)
        N=m0
        for t in range(tcut):
            X=[0]*N
            X[0]=K[0]+a

            for i in range(1,N):
                X[i]=X[i-1]+K[i]+a
            print X
            print K
            pp=random.randint(0,int(X[len(X)-1]))
            i=np.where(np.array(X)>=pp)[0][0]
            K[N]=1
            K[i]=K[i]+1
            N=N+1

        Ksum=float(sum(K))
        print Ksum
        for t in range(tcut,Niter+1):

            X=[0]*N
            X[0]=K[0]+a
            for i in range(1,N):
                X[i]=X[i-1]+K[i]+a

            pp=random.randint(0,int(X[len(X)-1]))
            i=np.where(np.array(X)>=pp)[0][0]
#            print (X[len(X)-1])
#            print X
            if ((K[i]/Ksum)>(c/N)):
                bablo=random.randint(1,3)
                K[N]=bablo
                K[i]=K[i]+bablo
                N=N+1
                Ksum=Ksum+2*bablo

    np.savetxt('Fig1a_K'+'_t='+str(t)+'_c='+str(c)+'.txt', K[0:N+m0], fmt='%1.5f', delimiter='  ')
##    S=db.DistV(K[1:N])
##    np.savetxt('Fig1b_S'+'_t='+str(t)+'_c='+str(c)+'.txt', S[1:N], fmt='%1.5f', delimiter='  ')


    return K

t1=time.time()

K=SF(200,0.0,1)

t2=time.time()-t1
print t2
