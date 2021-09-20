import numpy as np
from numpy.random import normal as gran

def velocityVerlet(dat) : 
    # Methods for a specific approach
    Uqm = dat.Uqm
    force = dat.force

    par =  dat.param
    v = dat.P/par.M
    EStep = int(par.dtN/par.dtE)
    dtE = par.dtN/EStep
    
    # half-step mapping
    for t in range(int(np.floor(EStep/2))):
        dat = Uqm(dat, dtE)
    # ======= Nuclear Block ==================================
    F1    =  dat.F1 #force(dat) # force with {qF(t+dt/2)} * dH(R(t))
    dat.R += v * par.dtN + 0.5 * F1 * par.dtN ** 2 / par.M
    
    #------ Do QM ----------------
    dat.Hij  = par.Hel(dat.R)
    dat.dHij = par.dHel(dat.R)
    dat.dH0  = par.dHel0(dat.R)
    #-----------------------------
    F2 = force(dat) # force with {qF(t+dt/2)} * dH(R(t+ dt))
    v += 0.5 * (F1 + F2) * par.dtN / par.M

    dat.P = v * par.M
    # =======================================================
    
    # half-step mapping
    dat.Hij = par.Hel(dat.R) # do QM
    for t in range(int(np.ceil(EStep/2))):
        dat = Uqm(dat,dtE)
    dat.F1 = F2
    return dat

def velocityVerletLangevin(dat) : 
    # Methods for a specific approach
    Uqm = dat.Uqm
    force = dat.force
    ndof = len(dat.P)
    par =  dat.param
    # Langevin specific Quantity
    β  = par.β
    λ = par.λ #/ par.m
    σ = (2.0 * λ/(β * par.M )) ** 0.5
    ξ = gran(0, 1, ndof)   
    θ = gran(0, 1, ndof)  
    A = (0.5 * dt**2) * (f1/par.M - λ * v) + (σ * dt**(3.0/2.0)) * (0.5 * ξ + c * θ) 
    
    v = dat.P/par.M
    EStep = int(par.dtN/par.dtE)
    dtE = par.dtN/EStep
    
    # half-step mapping
    for t in range(int(np.floor(EStep/2))):
        dat = Uqm(dat, dtE)
    # ======= Nuclear Block ==================================
    F1    =  force(dat) # force with {qF(t+dt/2)} * dH(R(t))
    dat.R += v * par.dtN + 0.5 * F1 * par.dtN ** 2 / par.M
    
    #------ Do QM ----------------
    dat.Hij  = par.Hel(dat.R)
    dat.dHij = par.dHel(dat.R)
    dat.dH0  = par.dHel0(dat.R)
    #-----------------------------
    F2 = force(dat) # force with {qF(t+dt/2)} * dH(R(t+ dt))
    v += 0.5 * (F1 + F2) * par.dtN / par.M

    dat.P = v * par.M
    # =======================================================
    
    # half-step mapping
    dat.Hij = par.Hel(dat.R) # do QM
    for t in range(int(np.ceil(EStep/2))):
        dat = Uqm(dat,dtE)
    
    return dat