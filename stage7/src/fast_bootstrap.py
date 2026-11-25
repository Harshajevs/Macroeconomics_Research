"""Vectorised version of the documented fixed-design block-wild Wald test.

This changes computation speed, not the conditional bootstrap estimand.
The independent recursive simulations deliberately use different error processes.
"""
import numpy as np

class Design:
    def __init__(self,X,R,lag=6):
        self.X=np.asarray(X,float);self.R=np.asarray(R,float);self.lag=lag
        self.n,self.k=self.X.shape
        self.bread=np.linalg.inv(self.X.T@self.X)
        self.project=self.bread@self.X.T
        self.z=self.X@self.bread@self.R.T

    def statistics(self,Y,kind='HAC'):
        Y=np.asarray(Y,float)
        if Y.ndim==1:Y=Y[:,None]
        b=self.project@Y;e=Y-self.X@b;delta=(self.R@b).T
        if kind=='HC3':
            h=np.sum(self.X*(self.X@self.bread),axis=1)
            e=e/(1-h)[:,None]
        V=np.einsum('ti,tb,tj->bij',self.z,e*e,self.z,optimize=True)
        if kind=='HAC':
            for lag in range(1,self.lag+1):
                cross=np.einsum('ti,tb,tj->bij',self.z[lag:],e[lag:]*e[:-lag],self.z[:-lag],optimize=True)
                V+=(1-lag/(self.lag+1))*(cross+cross.transpose(0,2,1))
            V*=self.n/(self.n-self.k)
        stat=np.einsum('bi,bij,bj->b',delta,np.linalg.pinv(V),delta,optimize=True)
        return stat,b,V

    def bootstrap(self,y,tested_indices,reps=999,seed=1,legacy_rng=True):
        y=np.asarray(y,float);x0=np.delete(self.X,tested_indices,axis=1)
        fitted=x0@np.linalg.lstsq(x0,y,rcond=None)[0];resid=y-fitted
        rng=np.random.default_rng(seed);exceed=0
        observed=self.statistics(y)[0][0]
        for first in range(0,reps,500):
            count=min(500,reps-first);signs=np.ones((self.n,count))
            if legacy_rng:
                for j in range(count):
                    offset=int(rng.integers(0,self.lag))
                    for start in range(-offset,self.n,self.lag):
                        signs[max(0,start):min(self.n,start+self.lag),j]=rng.choice([-1.,1.])
            else:
                # Same multiplier distribution, different recorded RNG stream.
                offsets=rng.integers(0,self.lag,size=count)
                pool=rng.choice([-1.,1.],size=(int(np.ceil(self.n/self.lag))+1,count))
                grid=(np.arange(self.n)[:,None]+offsets[None,:])//self.lag
                signs=np.take_along_axis(pool,grid,axis=0)
            star=fitted[:,None]+resid[:,None]*signs
            exceed+=int(np.sum(self.statistics(star)[0]>=observed))
        return (1+exceed)/(reps+1)
