import json
import pandas as pd
import numpy as np
from statsmodels.tsa import tsatools
import statsmodels.formula.api as smf
from statsmodels.tsa import tsatools
import statsmodels.tsa.seasonal as sts
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from BD import BD





def listes_valeurs_minimums_maximums_datetimes_idlieux(liste):
    valeurs=[]
    minimums=[]
    maximums=[]
    datetimes=[]
    idlieux=[]
    for valeur,maximum,minimum,datetime,idlieu in liste:
        valeurs.append(valeur)
        minimums.append(minimum)
        maximums.append(maximum)
        datetimes.append(datetime)
        idlieux.append(idlieu)
    return valeurs,minimums,maximums,datetimes,idlieux

def creer_dataframe(colonne1,colonne2,colonne3,colonne4,colonne5):
    dico={
        'temps':colonne4,
        "moyenne":colonne1,
        "minimum":colonne2,
        'maximum':colonne3,
        'idlieux':colonne5


    }

    retour=pd.DataFrame(dico)

    retour.set_index('temps',inplace=True)
    return retour

def renvoie_dataframe(typecapteur):
    colonne1,colonne2,colonne3,colonne4,colonne5=listes_valeurs_minimums_maximums_datetimes_idlieux(typecapteur)
    retour=creer_dataframe(colonne1,colonne2,colonne3,colonne4,colonne5)
    return retour

def description_donnees(donnees):
    for type,dataframes in donnees.items():
        print(f'{type} a les statistiques suivantes \n {dataframes.describe()}')
def boxplots_donnees(donnees):
    for type,dataframes in donnees.items():
        print(f"boite à moustaches du dataframe de {type}")
        dataframes.boxplot(column=['moyenne','maximum','minimum'])
        plt.title(f'boxplot de {type}')
        plt.show()
def tracer_stationnarite(donnees):
    for type,dataframe in donnees.items():
        if type!="CO2": #le CO2 est constant et ça fait crash
            print(f"series temporelles de {type}")
            liste_données=["moyenne","minimum","maximum"]
            for i in liste_données:
                test_stationarity(dataframe,i)

def tracer_series(donnees):
    for type,dataframe in donnees.items():

        print(f"series temporelles de {type}")
        liste_données=["moyenne","minimum","maximum"]
        for i in liste_données:
            plt.plot(dataframe[i])
            plt.title(f"serie temporelle {i} de {type}")
            plt.show()


def test_stationarity(timeseries,i):
    """test la stationnarité d'une série"""
    #Determing rolling statistics
    rolmean = timeseries.rolling(window=12).mean()
    rolstd = timeseries.rolling(window=12).std()

    #Plot rolling statistics:
    orig = plt.plot(timeseries, color="blue", label="Original")
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()

    #Perform Dickey-Fuller test:
    print ('Results of Dickey-Fuller Test:')
    print(timeseries[i])
    dftest = adfuller(timeseries[i], autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print (dfoutput)


instance_prod = BD()
instance_prod.connexion_bd()
temperatures=instance_prod.get_Mesure_Type("Temperature")
sons=instance_prod.get_Mesure_Type("Son")
CO2=instance_prod.get_Mesure_Type("Gaz:CO2")
NO2=instance_prod.get_Mesure_Type("Gaz:NO2")
CO=instance_prod.get_Mesure_Type("Gaz:CO")
COV=instance_prod.get_Mesure_Type("Gaz:COV")
CO2=renvoie_dataframe(CO2)
ethanol=instance_prod.get_Mesure_Type("Gaz:ethanol")
NO2=renvoie_dataframe(NO2)
CO=renvoie_dataframe(CO)
COV=renvoie_dataframe(COV)
ethanol=renvoie_dataframe(ethanol)
temperatures=renvoie_dataframe(temperatures)
temperature_test=renvoie_dataframe(instance_prod.mesures_d_une_arduino_par_type("eui-a8610a3231278105","Temperature"))[['moyenne']]
temperature_test.rename(columns={"moyenne": "Temperature"})
temperature_test=temperature_test.rename(columns={"moyenne": "Temperature"})
co2_test=renvoie_dataframe(instance_prod.mesures_d_une_arduino_par_type("eui-a8610a3231278105","Gaz:CO2"))[['moyenne']]
co2_test=co2_test.rename(columns={"moyenne": "CO2"})
out = pd.concat([temperature_test, co2_test], axis=1)
print(out)