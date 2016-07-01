__author__ = 'matteo'

import numpy as np

def rho_MM1(lambdA,mhu):
    res = float(lambdA/mhu)
    return res

def rho_MMm(lambdA,mhu,m):
    res = float(lambdA/(mhu*m))
    return res

def Tempo_Attesa_MM1(rho,mhu):
    return float(rho/mhu)/(1-rho)

def Tempo_Attesa_MMm(rho,mhu,m):
    sum = 0.0
    for k in range(m-1):
        sum += ((m*rho)**k)/(np.math.factorial(k))

    sum += ((m*rho)**m)/(np.math.factorial(m))*(1/(1-rho))
    pi_0 = sum**(-1)
    pi_m = (((m*rho)**m)/np.math.factorial(m))*pi_0

    T_w = pi_m/(m*mhu*((1-rho)**2))

    return T_w

def Tempo_Attesa_Medio(lambdA_mm1,mhu_mm1,lambdA_mmm,mhu_mmm,m,prob_N,prob_S,N_Casse_Aperte):
    print "#########################################"
    print "############# Dati Teorici ##############"

    rho_mm1 = rho_MM1(lambdA_mm1,mhu_mm1)
    rho_mmm = rho_MMm(lambdA_mmm,mhu_mmm,m)

    T_w_mm1 = Tempo_Attesa_MM1(rho_mm1,mhu_mm1)
    T_w_mmm = Tempo_Attesa_MMm(rho_mmm,mhu_mmm,m)

    res = (T_w_mm1*prob_N + T_w_mmm*prob_S)

    print "lambdA = " + str(lambdA_mm1*N_Casse_Aperte + lambdA_mmm)
    print "lambdA_mm1 = " + str(lambdA_mm1)
    print "lambdA_mmm = " + str(lambdA_mmm)
    print "mu_MM1 = " +str(mhu_mm1)
    print "mu_MMm = " +str(mhu_mmm)
    print "rho_MM1 = " +str(rho_mm1)
    print "rho_MMm = " +str(rho_mmm)
    print "T_W_MM1 = " + str(T_w_mm1)
    print "T_W_MMm = " + str(T_w_mmm)
    print "T_W_tot = " + str(res)
    print "n = " + str(N_Casse_Aperte)
    print "m = " + str(m)

    print "#########################################"

    return res





