import simpy
import numpy as np
from random import randint
from copy import copy

import matplotlib.pyplot as plt


# Dati Osservati
from RisoluzioneAnalitica import Tempo_Attesa_Medio


# Dati Simulazione




def createResource(env,nNormali,m):
    lista = []
    for i in range(nNormali):
        lista.append(simpy.Resource(env, capacity=1))

    lista.append(simpy.Resource(env, capacity=m))

    return lista

def createListaTempi(nNormali):
    res = []
    for i in range(nNormali + 1):
        res.append([])

    return res



def Casse(env,tipo,t_a,PROB_NORMALE,LAMBDA_TS_NORMALE,LAMBDA_TS_SALVA_TEMPO,Tempi_Attesa,Tempi_Servizio,Tempi_Arrivo):
    numeroCasse = len(tipo) - 1

    i = 0
    while(True):
        perc = randint(0,100)
        t = np.random.exponential(t_a, size=None)  #Tempo di Arrivo
        Tempi_Arrivo.append(t)
        if (perc <= PROB_NORMALE):
            n = randint(0,numeroCasse-1)
            c = cliente(env, 'Cliente Cassa Normale ' + str(i) + ' Cassa ' + str(n),tipo[n], LAMBDA_TS_NORMALE,Tempi_Attesa,Tempi_Servizio)
            env.process(c)
            yield env.timeout(t)  # e' praticamente ogni quanto arrivano
        else:
            c = cliente(env, 'Cliente Cassa Speciale ' + str(i),tipo[-1], LAMBDA_TS_SALVA_TEMPO,Tempi_Attesa,Tempi_Servizio)
            env.process(c)
            yield env.timeout(t)  # e' praticamente ogni quanto arrivano

        i+= 1

            


def cliente(env, name, tipo, lamdaTS,Tempi_Attesa,Tempi_Servizio):
    """Customer arrives, is served and leaves."""
    arrive = env.now
    #print('%7.4f %s: Here I am' % (arrive, name))

    with tipo.request() as req:
        # Wait for the counter or abort at the end of our tether
        yield req
        wait = env.now - arrive
        # We got to the counter
        #print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))
        tib = np.random.exponential(lamdaTS, size=None)
        #print("tempo di servizio %s" % tib)
        yield env.timeout(tib)
        #print('%7.4f %s: Finished' % (env.now, name))

        Tempi_Attesa.append(wait)
        Tempi_Servizio.append(tib)




def roundedValue(lista,value):
    intervallo = (value * 1)/100
    for i in lista:
        if not((i <= value + intervallo) and (i>= value - intervallo)):
            return False
    return True


def SimulatoreBase(env,t_a_tot,PROB_NORMALE,LAMBDA_TS_NORMALE,LAMBDA_TS_SALVA_TEMPO,N_casse,m,Teorica,N_persone = 0,TempoSimulazione = 0):

    #print "############ Simulazione ############"
    #print "t_a_tot = " + str(t_a_tot)
    #print "LAMBDA_TS_NORMALE = " +  str(LAMBDA_TS_NORMALE)
    #print "LAMBDA_TS_SALVA_TEMPO = " +  str(LAMBDA_TS_SALVA_TEMPO)
    Tempi_Attesa = []
    Tempi_Servizio = []
    Tempi_Arrivo = []

    ListaCasse = createResource(env,N_casse,m)
    env.process(Casse(env,ListaCasse,t_a_tot,PROB_NORMALE,LAMBDA_TS_NORMALE,LAMBDA_TS_SALVA_TEMPO,Tempi_Attesa,Tempi_Servizio,Tempi_Arrivo))

    N = 0
    go = True

    while (go):
        #print "gff", len(Tempi_Attesa)
        if (len(Tempi_Attesa) >= N_persone and env.now >= TempoSimulazione):

            print "############## Simulazione ##############"
            print "Tempo di Simulazione = " + str(int(env.now))
            print "Numero Casse Normali Aperte = " + str(N_casse)
            print "Numero Casse \"Fai da te\" Aperte = " + str(m)
            print "Numero clienti serviti = " + str(len(Tempi_Attesa))
            print "Numero clienti in coda = " + str(len(Tempi_Arrivo) - len(Tempi_Attesa))
            print "Tempo di Attesa Medio = " + str(np.average(Tempi_Attesa))
            print "Tempo di Servizio Medio = " + str(np.average(Tempi_Servizio))
            print "Tempo di Arrivo Medio = " + str(np.average(Tempi_Arrivo))


            print "#########################################"


            go = False

        else:
            N += 1
            env.step()



def SimulatoreStable(env,t_a_tot,PROB_NORMALE,LAMBDA_TS_NORMALE,LAMBDA_TS_SALVA_TEMPO,N_casse,m,Teorica,valore_stazionario,N_persone=100):
    Tempi_Attesa = []
    Tempi_Servizio = []
    Tempi_Arrivo = []
    Tempi_Attesa_medi = []

    ListaCasse = createResource(env,N_casse,m)
    env.process(Casse(env,ListaCasse,t_a_tot,PROB_NORMALE,LAMBDA_TS_NORMALE,LAMBDA_TS_SALVA_TEMPO,Tempi_Attesa,Tempi_Servizio,Tempi_Arrivo))

    t_inizio = 0
    p = 0
    go = True
    stable = False
    n = randint(50,100)
    n_esp = 0

    while (go):
        if not stable:
            if (len(Tempi_Attesa) == n):
                Tempi_Attesa_medi.append(np.average(Tempi_Attesa))
                n = randint(50,100)
                del Tempi_Attesa[:]
                del Tempi_Arrivo[:]
                del Tempi_Servizio[:]
                p += 1
                if p == valore_stazionario:
                    stable = True
                    t_inizio = int(env.now())
        else:

            if (len(Tempi_Attesa) >= N_persone):
                Tempi_Attesa_medi.append(np.average(Tempi_Attesa))
                n_esp += 1

                if n_esp == 100:

                    p10 = np.percentile(Tempi_Attesa_medi[0:len(Tempi_Attesa_medi)-100],10)
                    p90 = np.percentile(Tempi_Attesa_medi[0:len(Tempi_Attesa_medi)-100],90)

                    counter = 0
                    for i in Tempi_Attesa_medi[len(Tempi_Attesa_medi)-100:len(Tempi_Attesa_medi)]:
                        if (i>=p10 and i<=p90):
                            counter += 1

                    perc = float(counter)/N_persone*100

                    print "############## Simulazione ##############"
                    print "Tempo totale Simulazione = " + str(int(env.now))
                    print "Tempo di Simulazione = " + str(int(env.now) - t_inizio)
                    print "Numero Casse Normali Aperte = " + str(N_casse)
                    print "Numero Casse \"Fai da te\" Aperte = " + str(m)
                    print "Numero clienti = " + str(len(Tempi_Attesa)*n_esp)
                    print "Numero clienti in coda = " + str(len(Tempi_Attesa)*n_esp - len(Tempi_Attesa))
                    print "Tempo di Attesa Medio = " + str(np.average(Tempi_Attesa_medi[len(Tempi_Attesa_medi)-100:len(Tempi_Attesa_medi)]))
                    print "Tempo di Servizio Medio = " + str(np.average(Tempi_Servizio))
                    print "Tempo di Arrivo Medio = " + str(np.average(Tempi_Arrivo))
                    print "p10 = " + str(p10)
                    print "p90 = " + str(p90)
                    print "Percentuale = " + str(perc)
                    print "#########################################"


                    go = False

                del Tempi_Attesa[:]


        env.step()


    plt.plot(range(0,100),Tempi_Attesa_medi[len(Tempi_Attesa_medi)-100:len(Tempi_Attesa_medi)] , 'ro')
    l1, = plt.plot([0, 100], [p10,p10], lw=2, label='p10')
    l2, = plt.plot([0, 100], [p90,p90], lw=2, label='p90')
    l3, = plt.plot([0, 100], [Teorica,Teorica], lw=2, label='Media Teorica')
    plt.legend(handles=[l1,l2,l3])
    plt.show()





def ProveRipetute(env,t_a,PROB_NORMALE,LAMBDA_TS_NORMALE,LAMBDA_TS_SALVA_TEMPO,N_casse,m,Teorica):
    #print "t_a = " + str(t_a)
    #print "LAMBDA_TS_NORMALE = " +  str(LAMBDA_TS_NORMALE)
    #print "LAMBDA_TS_SALVA_TEMPO = " +  str(LAMBDA_TS_SALVA_TEMPO)
    Tempi_Attesa = []
    Tempi_Servizio = []
    Tempi_Arrivo = []
    Tempi_Attesa_medi = []
    N_utenti_serviti = 0
    N_utenti_entrati = 0
    t_inizio = 0

    ListaCasse = createResource(env,N_casse,m)
    env.process(Casse(env,ListaCasse,t_a,PROB_NORMALE,LAMBDA_TS_NORMALE,LAMBDA_TS_SALVA_TEMPO,Tempi_Attesa,Tempi_Servizio,Tempi_Arrivo))

    go = True
    campionamento = False

    matriceEsperimenti = []
    media_medie = []
    media_varianze = []
    result = []

    n = randint(50,100)
    while (go):

        if (len(Tempi_Attesa) == n):

            matriceEsperimenti.append(copy(Tempi_Attesa))
            Tempi_Attesa_medi.append(np.average(Tempi_Attesa))
            if campionamento:
                n = 100
                result.append(np.average(Tempi_Attesa))
                if len(result) == 100:
                    go = False

            else:
                n = randint(50,100)

            N_utenti_serviti += len(Tempi_Attesa)
            N_utenti_entrati += len(Tempi_Arrivo)
            del Tempi_Attesa[:]
            del Tempi_Arrivo[:]

            if len(Tempi_Attesa_medi) > 1:
                media_medie.append(np.average(Tempi_Attesa_medi))
                if len(media_medie) > 1:
                    media_varianze.append(np.var(media_medie,ddof = 1))
                if len(media_medie) > 100 and roundedValue(media_medie[len(media_medie)-100:len(media_medie)-1],media_medie[-1]):
                #if len(media_medie) > 30 and roundedValue(media_medie[len(media_medie)-30:len(media_medie)-1],Teorica):
                    campionamento = True
                    t_inizio = int(env.now)

        else:
            env.step()


    p10 = np.percentile(Tempi_Attesa_medi[0:len(Tempi_Attesa_medi)-100],10)
    p90 = np.percentile(Tempi_Attesa_medi[0:len(Tempi_Attesa_medi)-100],90)

    #print "p10 = " + str(p10) +  " p90 = " + str(p90)

    counter = 0
    for i in result:
        if (i>=p10 and i<=p90):
            counter += 1

    #print counter

    print "############# Prove Ripetute ############"
    print "Tempo totale Simulazione = " + str(int(env.now))
    print "Tempo di Simulazione = " + str(int(env.now) - t_inizio)
    print "Numero Casse Normali Aperte = " + str(N_casse)
    print "Numero Casse \"Fai da te\" Aperte = " + str(m)
    print "Numero clienti = " + str(N_utenti_serviti)
    print "Numero clienti in coda = " + str(N_utenti_entrati - N_utenti_serviti)
    print "Esecuzioni totali = " + str(len(Tempi_Attesa_medi))
    print "Numero esecuzioni p per la stazionarieta' del sistema = " + str(len(Tempi_Attesa_medi) - 100)
    print "Valore Stazionario = " + str(media_medie[-1])
    print "Tempo di Attesa medio = " + str(np.average(media_medie))
    print "p10 = " + str(p10)
    print "p90 = " + str(p90)
    print "Percentuale = "  + str(counter)



    print "#########################################"


    #print len(media_medie)
    #print media_medie[len(media_medie)-6:len(media_medie)]
    #print len(Tempi_Attesa)
    #print matriceEsperimenti
    #print len(Tempi_Attesa_medi)
    #print len(media_medie)
    #print media_medie[-1]
    #print media_varianze

    #print result



    plt.figure(1)
    plt.plot(range(0,100),Tempi_Attesa_medi[len(Tempi_Attesa_medi)-100:len(Tempi_Attesa_medi)] , 'ro')
    l1, = plt.plot([0, 100], [p10,p10], lw=2, label='p10')
    l2, = plt.plot([0, 100], [p90,p90], lw=2, label='p90')
    l3, = plt.plot([0, 100], [Teorica,Teorica], lw=2, label='Media Teorica')
    plt.legend(handles=[l2,l3,l1])
    plt.legend(loc='lower right', shadow=True)


    plt.figure(2)
    l1, = plt.plot(range(0,len(media_medie)),media_medie , lw=1)
    l2, = plt.plot(range(0,len(media_medie)),media_medie , 'ro')
    l3, = plt.plot([0, len(media_medie)], [media_medie[-1],media_medie[-1]], lw=2, label="Media delle medie")
    #l3, = plt.plot([0, len(media_medie)], [Teorica,Teorica], lw=2, label="media teorica")
    plt.legend(handles=[l3])
    plt.legend(loc='lower right', shadow=True)
    plt.show()

    return (len(Tempi_Attesa_medi) - 100)