import numpy as np

def tof2eV(t,V0,alpha,t0):
    return V0+alpha/((t-t0)**2)

def eV2TOF_Jac(E,alpha,V0):
    return 0.5*(np.sqrt(np.abs((E - V0)/alpha)))