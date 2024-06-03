
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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


def creer_graph_cor_CO2_Temp(lis_timeseries):
    corelation_temp_CO2 = pd.concat(lis_timeseries, axis=1)
    sns.lmplot(x="Temperature", y="CO2", data=corelation_temp_CO2);
    plt.show()
def creer_matrice_cor(lis_timeseries):
    corelation_gaz = pd.concat(lis_timeseries, axis=1)
    cormat = corelation_gaz.corr()
    sns.heatmap(cormat)
    plt.show()

def detect_outliers(timeseries):
    mediane = timeseries.mean()
    deviation_standard = timeseries.std()
    z_scores = (timeseries - mediane) / deviation_standard
    outliers = timeseries[z_scores**2 > 4]
    return outliers.dropna()

def creer_graph_outliers(timeseries,var):
    plt.scatter(timeseries.index, timeseries[[var]],label='Valeur cohérente (z²<4)')
    plt.scatter(detect_outliers(timeseries).index,detect_outliers(timeseries)[[var]],c="#CF2093",label='Valeur incohérente (z²>4)')
    plt.legend()
    plt.title(f"serie temporelle de {var}")
    plt.show()
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
no2_test=renvoie_dataframe(instance_prod.mesures_d_une_arduino_par_type("eui-a8610a3231278105","Gaz:NO2"))[['moyenne']]
no2_test=no2_test.rename(columns={"moyenne": "NO2"})
ethanol_test=renvoie_dataframe(instance_prod.mesures_d_une_arduino_par_type("eui-a8610a3231278105","Gaz:ethanol"))[['moyenne']]
ethanol_test=ethanol_test.rename(columns={"moyenne": "Ethanol"})
Cov_test=renvoie_dataframe(instance_prod.mesures_d_une_arduino_par_type("eui-a8610a3231278105","Gaz:COV"))[['moyenne']]
Cov_test=Cov_test.rename(columns={"moyenne": "COV"})
Co_test=renvoie_dataframe(instance_prod.mesures_d_une_arduino_par_type("eui-a8610a3231278105","Gaz:CO"))[['moyenne']]
Co_test=Co_test.rename(columns={"moyenne": "CO"})

creer_graph_cor_CO2_Temp([temperature_test, co2_test])
creer_matrice_cor([co2_test, no2_test, ethanol_test, Cov_test, Co_test])
creer_graph_outliers(temperature_test,"Temperature")
