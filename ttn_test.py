# Requirement: package paho-mqtt // Terminal >> pip install paho-mqtt


# ATTENTION , POUR ENVOYER DES DONNEES SUR LA BD, ETRE CONNECTE AU VPN MERCI
from ttn_client import TTNClient
import time
from BD import BD
from datetime import datetime


#fonction pour garder les 3 dernières valeurs d'une liste, connaissant la clé du dictionnaire:
def garder(dictionnaire,device_id):
    return dictionnaire[device_id][len(dictionnaire[device_id])-2:]
    




def moyenne(dictionnaire,device_id:str,clé:str):
    """
    prend un dictionnaire en paramètre, l'ID de l'appareil et la clé   
    renvoie (moyenne,min,max) s'il n'y a aucun problème dans les données,
    s'il y a un None dans une donnée, erreur et renvoie (None,None,None), erreur traitée dans le programme principal
    """
    liste=[]
    nonepresent=False       #variable qui indique s'il y a une None
    for mesures in dictionnaire[device_id]:
        valeur=mesures[clé]
        liste.append(valeur)
        if valeur==None:
            nonepresent=True

    
    if nonepresent:
        return None,None,None
    else:
        return sum(liste)/len(liste),min(liste),max(liste) #on fait la moyenne, le min et le max
    
def date_est_dans_donnees(donnees,device_id,date): # sert à vérifier qu'on ajoute pas de doublon
    
    
    for i in donnees[device_id]:
        if i["date"]==date:
            return False
    return True



# Classe TTNDataHandler qui doit avoir une méthode on_ttn_message
class TTNDataHandler:

    # Constructeur : attributs et paramètres à adapter aux besoins de votre projet (connexion BD, etc.)
    def __init__(self, parameter1, parameter2):
        self.parameter1 = parameter1
        self.parameter2 = parameter2

    # Méthode appelée lorsque le client TTN reçoit un message
    def on_ttn_message(self, message):
        print(f"[TTNDataHandler] Données reçues par le Handler avec les paramètres '{self.parameter1}', '{self.parameter2}'")
        self.my_method()
        device_id = message['device_id']
        message_date = message['date']
        message_json = message['json']
        # print(message_date)
        aff_message_date = message_date.strftime("%d/%m/%Y %H:%M:%S (%Z%z)")
        print(f"[TTNDataHandler] {aff_message_date}: Message de {device_id} => " + str(message_json))

    # Méthode(s) à adapter aux besoins de votre projet (requêtes SQL, etc.)
    def my_method(self):
        print(f"[TTNDataHandler] Méthode du TTNDataHandler... ['{self.parameter1}', '{self.parameter2}']")
ttn_application_id = "projet-2024-221b"
ttn_api_key_secret = "NNSXS.JRF5PYXOB57BFEYTPMSOUFOPIMV2UB4YTPWJWSY.XAV5PNFB6OMPO5NFJAYOYUPQZPWUJSTXJYCF7U4IGSRWIGZCHBUQ"
    
ttn_data_handler = TTNDataHandler('P2i-2 Test Value', 1742)

print("** Début du script **")
ttn = TTNClient(
        "eu1.cloud.thethings.network",
        ttn_application_id,
        ttn_api_key_secret,
        ttn_data_handler
    )
# ** Information de connexion à adapter à votre projet **





données={}        #de la forme device id:{[liste des valeursde la forme temp: ... , date:..., etc]}
données_simplifiees={}
print("** Connexion à MQTT @ TTN")
ttn.mqtt_connect()  # Connect to TTN
ttn.mqtt_register_devices(['node8', 'node7']) 
i=0
bd=BD()
i=0
dates=[]   
while True:
    start_time = time.time()
    
    # print()
    # print("** Envoi d'un message ???")
    # ttn.webhook_send_downlink('cmu-p32', 'node7')
    #
    # exit()
    
    print()
    print("** Récupération des messages stockés")
    current_time = time.time()
    
    ttn.storage_retrieve_messages(hours=0, minutes=2, seconds = 15)
    time.sleep(74-(current_time-start_time))    #on temporise

    payloads=ttn.device_payload      #payload de la forme {"device id: ....", "date":...,json":{"temp":...,"Co":... etc} etc}
    if payloads!=[]:
        for payload in payloads:
            données[payload["device_id"]]=données.get(payload["device_id"],[])
            if len(données[payload["device_id"]])==0:           #données[payload["device_id"]][-1]["date"]!=payload["date"]:
                
                données[payload["device_id"]]=[]
            
            if payload["isodate"] not in dates:
                données[payload["device_id"]]+=[{'temp': payload["json"].get("temp"), 'date': payload.get("date"), 'CO2': payload["json"].get("co2"), 'NO2': payload["json"].get("no2"),       
                                                'ethanol': payload["json"].get("ethanol"), 'COV': payload["json"].get("cov"), 'CO': payload["json"].get("co"), 'son': payload["json"].get("db")
                                                }]
                dates.append(payload["isodate"])
                i+=1
                print("donnée ajoutée")
        #on commence à mettre en forme les données avant d'effectuer les moyennes
    current_time2=time.time()
    print(f"il y a {i} données dans le dictionnaire")
    if i==15: #si cela fait 15 minutes qu'on récupère des données: (au bout de 15 données récupérées)
        i=0
        ttn.device_payload =[]
        k=0
        #dicgardé={} #on garde un dictionnaire pour éviter de faire des doublons
        #on fait maintenant les moyennes et on les met dans un dictionnaire puis on va les upload dans la BD
        for device_id in données.keys():  #on crée un dictionnaire ordonné pour chaque appareil
            k+=1
            dic2={}
            #dicgardé[device_id]=garder(données,device_id)
            if len(données[device_id])>0:
                for clé in données[device_id][0].keys():
                    if clé!="date": #on veut pas faire de moyenne sur la date
                        
                        moyen,minimum,maximum=moyenne(données,device_id,clé)
                        print(moyen,minimum,maximum)
                        if (moyen,minimum,maximum)!=(None,None,None):       #si les valeurs correspondants à la clé recherchée sont différentes de None 
                            #=>(si l'arduino possède un capteur correspondant) car si l'arduino n'a pas le capteur, la valeur sera None
                            dic3={"moyenne": moyen,"minimum": minimum,"maximum":maximum}
                            dic2[clé]=dic3
                            print(dic3)
                            print(dic2)
                #moyen,minimum,maximum=moyenne(données,device_id,"date")
            
                    données_simplifiees[device_id]=dic2
        données={} #on réinitialise le dictionnaire données après la dernière utilisation de la période de 15 minutes

        #données simplifiées de la forme {device_id:{temp   :{moyenne,minimum,maximum}, CO2: .......}}
        for dev_id in données_simplifiees.keys():
            idarduino=dev_id
            print("données simplifiées",données_simplifiees)
            for type,valeurs in données_simplifiees[dev_id].items(): #on met en forme les données avec les bonnes clés pour insérer sur la BD
                print("on rentre dans la boucle type valeur")
                if type=="temp":
                    typedecapteur="Temperature"
                    valeur,minimum,maximum=valeurs.values() #valeurs était un dictionnaire avec en clé moyenne, minimum, maximum et en valeurs les données
                    valeur=valeur/10
                    minimum=minimum/10
                    maximum=maximum/10      #les valeurs étaient multipliées par 10 pour envoyer des int avec l'arduino 

                    #pour réduire la taille de données à envoyer
                    
                elif type=="son":
                    typedecapteur="Son"
                    valeur,minimum,maximum=valeurs.values()
                else:
                    typedecapteur="Gaz:"+type
                    valeur,minimum,maximum=valeurs.values()
                date=datetime.now()
                datetemps=date #on récupère et on met en forme la date pour insertion dans la BD
                print("upload des valeurs sur la BD")
                time.sleep(2)
                bd.connexion_bd() #!!!! penser à être sous le vpn !!!
                bd.ajouter_mesure(idarduino, valeur, maximum, minimum, datetemps, typedecapteur) #on utilise la méthode de la classe BD
                print("données envoyées")
                if len(dates)>20:
                    dates=dates[len(dates)-10:]
        données_simplifiees={} #on réinitialise le dictionnaire après avoir envoyé les données
    print(données, "\n")
    
    #idmesure autoincrement
    #id capteur=requête à partir de device_id pour récupérer le nom du capteur associé dans la base
    #valeur=données_simplifiéees[device_id]["temp"]["moyenne"]
    #minimum=données_simplifiéees[device_id]["temp"]["minimum"]
    #maximum=données_simplifiéees[device_id]["temp"]["maximum"]
    #datetemps= datetime
    # ttn.mqtt_register_device("node16")
    # ttn.mqtt_register_device("node8")
    

