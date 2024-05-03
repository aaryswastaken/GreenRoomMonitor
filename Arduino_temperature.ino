#include <Multichannel_Gas_GMXXX.h>
#include <Wire.h>
#include <Arduino.h>
#include <MKRWAN.h>

typedef struct
{
uint16_t temperature; // °C 

} Trame_t ;

LoRaModem modem;
Trame_t ma_trame;

GAS_GMXXX<TwoWire> gas;
int entreeT = A1;
float VoutT =0;


//réseau
#define SECRET_APP_EUI "àremplir"
#define SECRET_APP_KEY "àremplir"

//capteurs
#define         MG_PIN                       (A2)     //define which analog input channel you are going to use
#define         BOOL_PIN                     (2)
#define         DC_GAIN                      (8.5)   //define the DC gain of amplifier


//These two values differ from sensor to sensor. user should derermine this value.

/*****************************Globals***********************************************/



void setup() {
  //connexion à lora
  Serial.begin(9600);
  delay(3000);
  bool lora_on = modem.begin(EU868);
  if (lora_on)
    Serial.println("Démarrage du module LoRaWAN ... OK");
  else
    Serial.println("Démarrage du module LoRaWAN ...Echec");

  delay(3000);

  Serial.flush();

  bool connected_to_lorawan = modem.joinOTAA(SECRET_APP_EUI, SECRET_APP_KEY);

  if (connected_to_lorawan)
    Serial.println(F("Connexion au réseau LoRaWAN ... Ok"));
  else
    Serial.println(F("Connexion au réseau LoRaWAN ...Echec"));



  //partie capteur
  Serial.begin(9600);
  pinMode(BOOL_PIN, INPUT);                        //set pin to input
  digitalWrite(BOOL_PIN, HIGH);                    //turn on pullup resistors
}
 
void loop() {
  
  //main code Thermistance :
  VoutT = (analogRead(entreeT)/1023.0)*3.3;

  
  //envoie des données

  ma_trame.temperature= int(10*(VoutT*13.2-2.25))  ;
  modem.beginPacket();
  modem.write( (byte* )& ma_trame, sizeof(ma_trame) ) ;
  int err = modem.endPacket();
  if (err > 0) {
    Serial.println("Message envoyé correctement");
  } else {
    Serial.println("Erreur d'envoi :(");
  }
  Serial.print("Thermistance :" + String(VoutT) + "  T = " + String(VoutT*13.2-2.25) + "\n");

  

  if (digitalRead(BOOL_PIN) ){
      Serial.print( "=====BOOL is HIGH======" );
  } else {
      Serial.print( "=====BOOL is LOW======" );
  }

  Serial.print("\n");


  delay(60000);
 
}


