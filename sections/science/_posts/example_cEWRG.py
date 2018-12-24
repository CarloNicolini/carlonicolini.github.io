import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import root
import bct
eps = np.finfo(float).eps

def pij_wij(x,y,t):
    xij = np.outer(x,x)
    yij = np.outer(y,y)
    pij = xij*((yij)**t)/(1.0+xij*(yij**t) - (yij**t))
    wij = (t*(xij-1.0)*(yij**t))/((1.0 + xij*(yij**t) - (yij**t) )) - 1.0/(np.log(np.abs(yij+eps)))
    return pij,wij

def eq(z, t, ki, si):
    nz = len(z)
    n = nz//2
    pij,wij = pij_wij(z[0:n],z[n:],t) # x is first half, y is second half
    #print(pij.shape,wij.shape,ki.shape,si.shape)
    #pij -= pij.di
    np.fill_diagonal(pij,0)
    np.fill_diagonal(wij,0)
    delta_pij = np.sum(pij,axis=0) - ki
    delta_wij = np.sum(wij,axis=0) - si
    return np.concatenate([delta_pij, delta_wij])

def factor_model(ci,T,eta,mu, correlation=False):
    N = len(ci) # number of nodes, length of membership vector,
    # Initialize the observations vector a TxN matrix of NaNs,
    Y = np.ones([T,N])*np.nan
    
    # Fill the identical observations in the maximally correlated subsets,
    for c in np.unique(ci):
        i = np.where(ci==c)[0]
        Y[:,i] = np.kron(np.ones((1,(ci==c).sum())),np.random.randn(T,1))

    # Add local noise beta on each time-series,
    Y += eta*np.random.randn(T,N)
    # Add global signal mu that correlates globally each time series,
    Y += mu*np.kron(np.ones((1,N)),np.random.randn(T,1))

    from scipy.stats import zscore
    Y = zscore(Y)
    if correlation:
        C = np.corrcoef(Y.T)
        np.fill_diagonal(C,0)
    else:
        C = np.cov(Y.T)
    return C


def inference_cEWRGt(W, thresh):
    
    k = (W>0).sum(axis=0) # degrees
    s = W.sum(axis=0) # strength

    #from scipy.optimize import root
    from scipy.optimize import least_squares

    x0=np.concatenate([k,s])*1E-4 # initial solution
    
    # Initialize least squares from previous solution
    sollm = least_squares(lambda v: eq(v,thresh,k,s),
                          x0=x0,
                          bounds= (0,np.inf),
                          method='trf',
                          ftol=1E-8,
                          xtol=1E-8,
                          verbose=1)

    sollm = root(lambda z: eq(z,thresh,k,s),
                 x0=x0,
                 method='lm',
                 options={'xtol':1E-30,'gtol':1E-30,'ftol':1E-30},
                 tol=1E-6)
    
    
    #print('Final cost', sollm['cost'])
    sollm = sollm['x']
    n2 = int(len(sollm)//2)
    x,y = sollm[0:n2],sollm[n2:]
    return x, y

def plot_results(W,x,y,thresh):
    pij,wij = pij_wij(x,y,thresh) # compute the output from the optimization result
    plt.figure(figsize=(12,8))
    plt.subplot(2,3,1)
    im = plt.imshow(pij)
    plt.colorbar(im,fraction=0.046, pad=0.04)
    plt.grid(False)
    plt.title('$p_{ij}$')

    plt.subplot(2,3,2)
    im = plt.imshow(wij)
    plt.colorbar(im,fraction=0.046, pad=0.04)
    plt.grid(False)
    plt.title('$<w_{ij}>$')

    plt.subplot(2,3,3)
    im = plt.imshow(W)
    plt.colorbar(im,fraction=0.046, pad=0.04)
    plt.grid(False)
    plt.title('empirical matrix')

    plt.subplot(2,3,4)
    plt.plot((W>0).sum(axis=0),pij.sum(axis=0), 'b.')
    plt.plot(np.linspace(0,pij.sum(axis=0).max()),np.linspace(0,pij.sum(axis=0).max()),'r-')
    plt.grid(True)
    plt.axis('equal')
    plt.title('$k_i - <k_i>$')
    plt.ylabel('model')
    plt.xlabel('empirical')
    #plt.xlim([0,min((W>0).sum(axis=0).max(),pij.sum(axis=0).max())])
    #plt.ylim([0,min((W>0).sum(axis=0).max(),pij.sum(axis=0).max())])

    plt.subplot(2,3,5)
    plt.plot(W.sum(axis=0),wij.sum(axis=0), 'b.')
    plt.plot(np.linspace(0,wij.sum(axis=0).max()),np.linspace(0,wij.sum(axis=0).max()),'r-')
    plt.title('$ s_i - <s_i>$')
    plt.axis('equal')
    #plt.xlim([0,wij.sum(axis=0).max()])
    #plt.ylim([0,wij.sum(axis=0).max()])
    plt.grid(True)
    plt.ylabel('model')
    plt.xlabel('empirical')

    plt.tight_layout()
    plt.show()

if __name__=='__main__':

    thresh = 0.2 # threshold
    T = 200 # number of time points to sample
    eta = 3.0 # localnoise
    mu = 1.0 # globalnoise
    C = np.arctanh(factor_model([1]*40 + [2]*40 + [3]*30, T, eta, mu, True))
    At = bct.threshold_absolute(C, thresh)
    n=len(At)
    k = (At>0).sum(axis=0)
    s = At.sum(axis=0)

    x,y = inference_cEWRGt(At, thresh)
    plot_results(At, x, y, thresh)