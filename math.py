import numpy as np;import math

#ERO
#LSS
mat=np.array(((3,11),(1,13),(7,5),(10,10)))
vec=np.array((7,2,3,1))
ran=np.linalg.matrix_rank(mat)
np.dot(np.linalg.inv(np.dot(mat.transpose(),mat)),np.dot(mat.transpose(),vec))

#norm,dist
a=np.array((1,2,3,4,100))
b=np.array((1,5,3,6,200))
x=np.float16(math.sqrt(sum((a-b)**2 for a,b in zip(a,b))))

def dp_strange(a,b):
    if not a.shape[1]==b.shape[0]:
        raise ValueError
    else:
        c=np.zeros((b.shape),dtype=np.uint8)
        for x in range(len(a)):
            for w in range(len(b)):
                c[x][w]=a[x][w]*b[x][w]
                return c

mat.dot()
dp(mat,mat)

#GDA

