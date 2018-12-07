{% highlight python %}
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from scipy.optimize import fsolve,root


def pij_wij(x,y,t):
    eps=1E-16
    xij = np.outer(x,x)
    yij = np.outer(y,y)
    pij = xij*((yij)**t)/(1.0+xij*(yij**t) - (yij**t))
    wij = (t*(xij-1.0)*(yij**t))/((1.0 + xij*(yij**t) - (yij**t) )) - 1.0/(np.log(np.abs(eps+yij)))
    return pij,wij

def eq(z, t, ki, si):
    nz = len(z)
    n = nz//2
    pij,wij = pij_wij(z[0:n],z[n:],t) # x is first half, y is second half
    #print(pij.shape,wij.shape,ki.shape,si.shape)
    np.fill_diagonal(pij,0)
    np.fill_diagonal(wij,0)
    
    delta_pij = np.sum(pij,axis=0) - ki
    delta_wij = np.sum(wij,axis=0) - si
    return np.concatenate([delta_pij, delta_wij])


#A = np.random.exponential(0.5,size=(n,n))
#A*=A>0.2
#np.fill_diagonal(A,0)
import bct
A=np.loadtxt('/home/carlo/workspace/communityalg/data/GroupAverage_rsfMRI_unthr.adj')
np.fill_diagonal(A,0)

A=A[0:50,0:50]
t=0.2
A=bct.threshold_absolute(A,t)

n=len(A)

k = (A>0).sum(axis=0)
s = A.sum(axis=0)
eps = np.finfo(float).eps
sol = root(lambda v: eq(v,t,k,s), 
           x0=np.random.random(len(k)+len(s)),
           method='lm',
           options={'xtol':1E-16,'gtol':1E-16,'ftol':1E-16})

x = sol['x'][0:n]
y = sol['x'][n:]
pij,wij = pij_wij(x,y,t) # compute the output from the optimization result
plt.figure(figsize=(12,8))
plt.subplot(2,3,1)
im = plt.imshow(pij)
plt.colorbar(im,fraction=0.046, pad=0.04)
plt.grid(False)
plt.title('$p_{ij}$')

plt.subplot(2,3,2)
im = plt.imshow(wij)
plt.clim([A.min(),A.max()])
plt.colorbar(im,fraction=0.046, pad=0.04)
plt.grid(False)
plt.title('$q_{ij}$')

plt.subplot(2,3,3)
im = plt.imshow(A)
plt.colorbar(im,fraction=0.046, pad=0.04)
plt.grid(False)
plt.title('A')

#plt.subplot(2,3,4)
#im = plt.imshow(sol['fjac'])
#plt.colorbar(im,fraction=0.046, pad=0.04)
#plt.grid(False)
#plt.title('Jacobian')

plt.subplot(2,3,4)
plt.plot((A>0).sum(axis=0),pij.sum(axis=0), 'b.')
plt.plot(np.linspace(0,pij.sum(axis=0).max()),np.linspace(0,pij.sum(axis=0).max()),'r-')
plt.grid(True)
plt.axis('equal')
plt.title('$k_i - <k_i>$')
plt.ylabel('model')
plt.xlabel('empirical')
plt.xlim([0,min((A>0).sum(axis=0).max(),pij.sum(axis=0).max())])
plt.ylim([0,min((A>0).sum(axis=0).max(),pij.sum(axis=0).max())])

plt.subplot(2,3,5)
plt.plot(A.sum(axis=0),wij.sum(axis=0), 'b.')
plt.plot(np.linspace(0,wij.sum(axis=0).max()),np.linspace(0,wij.sum(axis=0).max()),'r-')
plt.title('$ s_i - <s_i>$')
plt.axis('equal')
plt.xlim([0,wij.sum(axis=0).max()])
plt.ylim([0,wij.sum(axis=0).max()])
plt.grid(True)
plt.ylabel('model')
plt.xlabel('empirical')


plt.tight_layout()
{% endhighlight %}