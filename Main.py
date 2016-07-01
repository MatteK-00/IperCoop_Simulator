from Simulatore import SimulatoreBase, ProveRipetute, SimulatoreStable

__author__ = 'matteo'

import simpy



from RisoluzioneAnalitica import Tempo_Attesa_Medio, rho_MM1, rho_MMm

#Dati Osservati
LAMBDA_TA_NORMALE = 68.9
LAMBDA_TS_NORMALE = 84.7
LAMBDA_TA_SALVA_TEMPO = 55.0
LAMBDA_TS_SALVA_TEMPO = 43.8
PROB_NORMALE = 83
PROB_S_TEMPO = 17

#Dati Studio Analitico
lambda_TOT = 0.105
p_n = float(PROB_NORMALE)/100
p_s = float(PROB_S_TEMPO)/100
lambda_N = lambda_TOT*p_n
lambda_F = lambda_TOT*p_s
mhu_N = (1/LAMBDA_TS_NORMALE)
mhu_F = (1/LAMBDA_TS_SALVA_TEMPO)




NUMERO_CASSE_APERTE = 8
m = 6
lambda_N_MM1 = lambda_N/NUMERO_CASSE_APERTE

#Eta
Tempo_Medio_Attesa_Teorico = Tempo_Attesa_Medio(lambda_N_MM1,mhu_N,lambda_F,mhu_F,m,p_n,p_s,NUMERO_CASSE_APERTE)



env = simpy.Environment()

#SimulatoreBase(env,(lambda_TOT**(-1)),PROB_NORMALE,LAMBDA_TS_NORMALE,LAMBDA_TS_SALVA_TEMPO,NUMERO_CASSE_APERTE,m,Tempo_Medio_Attesa_Teorico,0,3600)

if (rho_MM1(lambda_N_MM1,mhu_N) > 1 or rho_MMm(lambda_F,mhu_F,m) > 1):
    print "Warning rho > 1 Sistema non stabile"
else:
    #SimulatoreBase(env,(lambda_TOT**(-1)),PROB_NORMALE,LAMBDA_TS_NORMALE,LAMBDA_TS_SALVA_TEMPO,NUMERO_CASSE_APERTE,m,Tempo_Medio_Attesa_Teorico,0,3600)
    stb = ProveRipetute(env,(lambda_TOT**(-1)),PROB_NORMALE,LAMBDA_TS_NORMALE,LAMBDA_TS_SALVA_TEMPO,NUMERO_CASSE_APERTE,m,Tempo_Medio_Attesa_Teorico)
    #SimulatoreStable(env,(lambda_TOT**(-1)),PROB_NORMALE,LAMBDA_TS_NORMALE,LAMBDA_TS_SALVA_TEMPO,NUMERO_CASSE_APERTE,m,Tempo_Medio_Attesa_Teorico,stb,100)
