import random
from datetime import datetime
import mysql.connector as mysql
import json


class BD:

    def __init__(self, ):
        self.connexion_BD = None

    def connexion_bd(self):
        print("")
        print("**************************")
        print("** Se Connecter à la BD **")
        print("**************************")
        print("")
        try:
            # print('MySQL / paramstyle: ' + mysql.paramstyle)
            self.connexion_BD = mysql.connect(
                host='fimi-bd-srv1.insa-lyon.fr',
                port=3306,
                user='G221_B', # a completer
                password='G221_B', # a completer
                database='G221_B_BD3' # a completer
            )
            print("=> Connexion a ... établie...")
        except Exception as e:
            print('MySQL [ERROR]')
            print(e)

    def ajouter_mesure(self, idarduino, valeur, maximum, minimum, datetemps, typedecapteur):
            """
        Méthode qui permet d'ajouter des valeurs à la BD a partir de l'id arduino du capteur et de son type
        :str idarduino: L'id de l'arduino qui a effectuer la valeur
        :float valeur: Valeur moyenne sur 5 min du capteur a ajouter dans la BD
        :float maximum: Valeur maximum renvoyé par l'arduino
        :float minimum: Valeur minimum renvoyé par l'arduino
        :datetime datetemps: Moment de la mesure
        :str typedecapteur: Type de capteur en str, permet de retrouver id capteur avec id arduino
        Ajoute (idCapteur,valeur,maximum, minimum, datetemps) à la BD
            """
            cursor = self.connexion_BD.cursor()
            cursor.execute('INSERT INTO Mesures (idCapteur,valeur,maximum, minimum, datetemps) VALUES ((select idCapteur from Capteur where idArduino = %s and idType=(select idType from TypeCapteur where nom=%s )),%s,%s,%s,%s )', [idarduino,typedecapteur, valeur, maximum,minimum,datetemps ])
            self.connexion_BD.commit()
    def get_Mesure_capteur(self,idCapteur):
        """
         Méthode qui permet de renvoyer toute les mesures faites par un capteur

        :uint idCapteur: L'id du capteur qui a effectuer la mesure
        :return: Renvoye une liste contenenant des tuples (valeur,maximum,minimum,datetemps)
        """
        cursor = self.connexion_BD.cursor()
        cursor.execute('SELECT valeur,maximum, minimum, datetemps FROM Mesures where idCapteur=%s',[idCapteur])
        return cursor.fetchall()
    def get_Capteur_Actif(self):
        """
        Renvoie la liste des capteurs actifs qui ont déjà effectué une mesure
        """
        cursor = self.connexion_BD.cursor()
        cursor.execute('SELECT DISTINCT Mesures.idCapteur FROM Mesures,Capteur, Arduino where Arduino.actif=1  and Capteur.idArduino=Arduino.idArduino and Capteur.idCapteur=Mesures.idCapteur')
        return cursor.fetchall()
    def get_Localisation_Capteur(self,idCapteur):
        """
                Renvoie le tuple (batiment, piece) pour un capteur en particulier
                """
        cursor = self.connexion_BD.cursor()
        cursor.execute('SELECT Localisation.batiment,Localisation.piece FROM Capteur,Arduino,Localisation where idCapteur=%s and Capteur.idArduino=Arduino.idArduino and Arduino.idLieu=Localisation.idLieu ',[idCapteur])
        return cursor.fetchall()
    def get_Arduino_Capteur(self,idCapteur):
        """
                        Renvoie l'arduino qui correspond capteur en particulier
                        """
        cursor = self.connexion_BD.cursor()
        cursor.execute('SELECT Arduino.idArduino FROM Capteur,Arduino where idCapteur=%s and Capteur.idArduino=Arduino.idArduino',[idCapteur])
        return cursor.fetchall()
    def get_Mesure_Piece(self,batiment,piece):
        """
                 Méthode qui permet de renvoyer toute les mesures faites dans une piece ainsi que leur type

                :str batiment:
                :str piece:
                :return: Renvoye une liste contenenant des tuples (valeur,maximum,minimum,datetemps,typeDeMesure)
                """
        cursor = self.connexion_BD.cursor()
        cursor.execute('SELECT valeur,maximum, minimum, datetemps,TypeCapteur.nom FROM Capteur,Arduino,Localisation,TypeCapteur,Mesures where Mesures.idCapteur=Capteur.idCapteur and TypeCapteur.idType=Capteur.idType and Capteur.idArduino=Arduino.idArduino and Arduino.idLieu=Localisation.idLieu and Localisation.piece=%s and Localisation.batiment=%s',[piece,batiment])
        return cursor.fetchall()

    def get_Arduino_Piece(self,batiment,piece):
        cursor = self.connexion_BD.cursor()
        cursor.execute(
            'SELECT Arduino.idArduino FROM Capteur,Arduino,Localisation where Capteur.idArduino=Arduino.idArduino and Arduino.idLieu=Localisation.idLieu and Localisation.piece=%s and Localisation.batiment=%s',
            [piece, batiment])
        return cursor.fetchall()

    def get_Mesure_Type(self,NomtypeCapteur):
        """
                         Méthode qui permet de renvoyer toute les mesures faites par un type de capteur

                        :str NomtypeCapteur, le nom du type de capteur
                        :return: Renvoye une liste contenenant des tuples (valeur,maximum,minimum,datetemps,idLocalisation)
                        """
        cursor = self.connexion_BD.cursor()
        cursor.execute(
                'SELECT valeur,maximum, minimum, datetemps,Localisation.idLieu FROM Capteur,Arduino,Localisation,TypeCapteur,Mesures where Mesures.idCapteur=Capteur.idCapteur and TypeCapteur.idType=Capteur.idType and Capteur.idArduino=Arduino.idArduino and Arduino.idLieu=Localisation.idLieu and TypeCapteur.nom=%s ',[NomtypeCapteur])
        return cursor.fetchall()
    def get_donnee_loc(self):
        """
        Renvoie la liste des pieces qui contiennent au moins un capteur actif
        """
        cursor = self.connexion_BD.cursor()
        cursor.execute(
            'SELECT DISTINCT Localisation.batiment,Localisation.piece, Arduino.idArduino, Localisation.x, Localisation.y FROM Arduino,Localisation where Arduino.idLieu=Localisation.idLieu')
        return cursor.fetchall()
    def get_Piece_Inactive(self):
        """
        Renvoie la liste des pieces qui contiennent au moins un capteur actif
        """
        cursor = self.connexion_BD.cursor()
        cursor.execute('SELECT DISTINCT Localisation.idLieu FROM Arduino,Localisation where Arduino.idLieu=Localisation.idLieu  GROUP BY Localisation.idLieu HAVING SUM(Arduino.actif) = 0')
        return cursor.fetchall()


    def mesures_d_une_arduino_par_type(self,idarduino,typecapteur):
        """ 
        renvoie la liste des mesures correspondant à une arduino
        
        """
        cursor=self.connexion_BD.cursor()
        cursor.execute("select m.valeur,m.maximum, m.minimum, m.datetemps,a.idLieu from Mesures m ,Capteur c,Arduino a,TypeCapteur tc  where c.idCapteur =m.idCapteur and a.idArduino =c.idArduino and tc.idType=c.idType and a.idArduino  =%s and tc.nom=%s",[idarduino,typecapteur])
        return cursor.fetchall()
    def mesures_d_une_arduino_par_type2(self,idarduino,typecapteur):
        """ 
        renvoie la liste des mesures correspondant à une arduino
        
        """
        cursor=self.connexion_BD.cursor()
        cursor.execute("select m.valeur,m.maximum, m.minimum, m.datetemps,a.idLieu from Mesures m ,Capteur c,Arduino a,TypeCapteur tc  where c.idCapteur =m.idCapteur and a.idArduino =c.idArduino and tc.idType=c.idType  and a.idArduino  =%s and tc.nom=%s and m.datetemps in(select datetemps from Mesures m, Capteur c,TypeCapteur tc where m.idCapteur=c.idCapteur and c.idType=tc.idType and tc.nom='Gaz:CO2')",[idarduino,typecapteur])
        return cursor.fetchall()

    def mesure_to_js(self):
            cursor = self.connexion_BD.cursor()
            cursor.execute('SELECT DISTINCT idCapteur FROM Mesures')
            resultat = cursor.fetchall()
            dico_totale={}
            for i in resultat:
                cursor.execute('SELECT TypeCapteur.nom FROM Capteur,TypeCapteur where Capteur.idCapteur=%s and  TypeCapteur.idType=Capteur.idType', [i[0]])
                typecapteur= cursor.fetchall()[0][0]
                if typecapteur.split(":")[0]!="Gaz":
                    if typecapteur not in dico_totale:
                        dico_totale[typecapteur]={}
                    dic_bat = dico_totale[typecapteur]
                    cursor.execute('SELECT Localisation.batiment FROM Capteur,Arduino,Localisation where idCapteur=%s and Capteur.idArduino=Arduino.idArduino and Arduino.idLieu=Localisation.idLieu ',[i[0]])
                    batiment = cursor.fetchall()[0][0]

                    if batiment not in dic_bat:
                        dic_bat[batiment]={}
                    cursor.execute('SELECT Localisation.piece FROM Capteur,Arduino,Localisation where idCapteur=%s and Capteur.idArduino=Arduino.idArduino and Arduino.idLieu=Localisation.idLieu',[i[0]])
                    piece = cursor.fetchall()[0][0]
                    if piece not in dic_bat[batiment]:
                        dic_bat[batiment][piece]={"loc":f"{batiment}/{piece}"}
                    cursor.execute(
                        'SELECT Arduino.idArduino FROM Capteur,Arduino where idCapteur=%s and Capteur.idArduino=Arduino.idArduino',
                        [i[0]])
                    arduino = cursor.fetchall()[0][0]
                    if arduino not in dic_bat[batiment][piece]:
                        dic_bat[batiment][piece][arduino]={"donnees":[]}
                    dic_bat[batiment][piece][arduino]["donnees"].append({})
                    dic=dic_bat[batiment][piece][arduino]["donnees"][-1]
                    dic["idcapteur"] = str(i[0])
                    cursor.execute('SELECT valeur,datetemps FROM Mesures where idCapteur=%s ', [i[0]])
                    dic["data"] = [[datetime.timestamp(y[1])*1000, y[0]] for y in cursor.fetchall()]
                else:
                    if "Gaz" not in dico_totale:
                        dico_totale["Gaz"] = {}
                    dic_bat = dico_totale["Gaz"]
                    cursor.execute(
                        'SELECT Localisation.batiment FROM Capteur,Arduino,Localisation where idCapteur=%s and Capteur.idArduino=Arduino.idArduino and Arduino.idLieu=Localisation.idLieu ',
                        [i[0]])
                    batiment = cursor.fetchall()[0][0]

                    if batiment not in dic_bat:
                        dic_bat[batiment] = {}
                    cursor.execute(
                        'SELECT Localisation.piece FROM Capteur,Arduino,Localisation where idCapteur=%s and Capteur.idArduino=Arduino.idArduino and Arduino.idLieu=Localisation.idLieu',
                        [i[0]])
                    piece = cursor.fetchall()[0][0]
                    if piece not in dic_bat[batiment]:
                        dic_bat[batiment][piece]={"loc":f"{batiment}/{piece}"}
                    cursor.execute(
                        'SELECT Arduino.idArduino FROM Capteur,Arduino where idCapteur=%s and Capteur.idArduino=Arduino.idArduino',
                        [i[0]])
                    arduino = cursor.fetchall()[0][0]
                    if arduino not in dic_bat[batiment][piece]:
                        dic_bat[batiment][piece][arduino] = {"donnees": []}
                    dic_bat[batiment][piece][arduino]["donnees"].append({})
                    dic = dic_bat[batiment][piece][arduino]["donnees"][-1]
                    dic["idcapteur"] = str(i[0])
                    dic["name"] = typecapteur.split(":")[1]
                    cursor.execute('SELECT valeur,datetemps FROM Mesures where idCapteur=%s ', [i[0]])
                    dic["data"] = [[datetime.timestamp(y[1])*1000,y[0] ] for y in cursor.fetchall()]
            for i in dico_totale:
                out_file = open(f"{i}.js", "w")
                out_file.write(f"var {i}_TIME_SERIES = ")
                json.dump(dico_totale[i], out_file, indent=3)
                out_file.close()









                #######################
    def localisation_to_json(self):
        dico_piece={}
        for batiment, piece, id,x, y in self.get_donnee_loc():
            if batiment not in dico_piece:
                dico_piece[batiment]={}
            if piece not in dico_piece[batiment]:
                dico_piece[batiment][piece]=[]
            dico_piece[batiment][piece].append({"id":id,"x":x,"y":y})
        out_file = open(f"loc.js", "w")
        out_file.write(f"var DIC_LOC = ")
        json.dump(dico_piece, out_file, indent=3)
        out_file.close()

# Programme principal #
#######################
if __name__ == "__main__":
    instance_prod = BD() # remlplacer
    instance_prod.connexion_bd()
    #instance_prod.ajouter_mesure("eui-a8610a333937930f",random.randint(0,100),random.randint(0,100),random.randint(0,100),datetime.now(),"Temperature")
    instance_prod.mesure_to_js()
    print(instance_prod.get_Capteur_Actif())
    print(instance_prod.get_Mesure_Piece("Usine","Salle informatique"))
    print(instance_prod.get_Mesure_Type("Temperature"))
    print(instance_prod.get_Piece_Inactive())
    print(instance_prod.localisation_to_json())
    print(instance_prod.get_Arduino_Piece("Usine","Salle informatique"))
# lancer la boucle infinie de production de données
#instance_prod.produire_mesures()

