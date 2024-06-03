#include <Multichannel_Gas_GMXXX.h>
#include <Wire.h>
#include <Arduino.h>
#include <MKRWAN.h>

typedef struct {
    uint16_t temperature;// °C
    uint16_t CO2; // ppm
    uint16_t NO2; //ppm
    uint16_t C2H5OH; //ppm
    uint16_t COV; //ppm
    uint16_t CO; //ppm
    uint16_t son; //dB
} Trame_t;

Trame_t ma_trame;
LoRaModem modem;

//son
int analogPin = A4;
float val;
float dif_db65;
float db;
//fin son

GAS_GMXXX<TwoWire> gas;
int entreeT = A1;
float VoutT =0;

int compteur=1;
float cCO2;// les valeurs moyennes des gaz
float cNO2;
float cC2H5OH;
float cCO;
float cCOV;

//réseau
#define SECRET_APP_EUI ""
#define SECRET_APP_KEY ""

//capteurs
#define         MG_PIN                       (A2)     //define which analog input channel you are going to use
#define         DC_GAIN                      (8.5)   //define the DC gain of amplifier

/***********************Software Related Macros************************************/
#define         READ_SAMPLE_INTERVAL         (50)    //define how many samples you are going to take in normal operation
#define         READ_SAMPLE_TIMES            (5)     //define the time interval(in milisecond) between each samples in
                                                     //normal operation
//These two values differ from sensor to sensor. user should derermine this value.
#define         ZERO_POINT_VOLTAGE           (0.176) //define the output of the sensor in volts when the concentration of CO2 is 400PPM
#define         REACTION_VOLTGAE             (0.030) //define the voltage drop of the sensor when move the sensor from air into 1000ppm CO2

/*****************************Globals***********************************************/
float           CO2Curve[3]  =  {2.602,ZERO_POINT_VOLTAGE,(REACTION_VOLTGAE/(2.602-3))};
                                                     //two points are taken from the curve.
                                                     //with these two points, a line is formed which is
                                                     //"approximately equivalent" to the original curve.
                                                     //data format:{ x, y, slope}; point1: (lg400, 0.324), point2: (lg4000, 0.280)
                                                     //slope = ( reaction voltage ) / (log400 –log1000)

float mdb;

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
    Serial.print("Mon device EUI est: ");
    Serial.println(modem.deviceEUI());
    Serial.flush();

    bool connected_to_lorawan = modem.joinOTAA(SECRET_APP_EUI, SECRET_APP_KEY);

    if (connected_to_lorawan)
	Serial.println(F("Connexion au réseau LoRaWAN ... Ok"));
    else
	Serial.println(F("Connexion au réseau LoRaWAN ...Echec"));

    Serial.println(F("Mon DevAddr est :"));
    Serial.println(modem.getDevAddr());

    //partie capteur
    Serial.begin(9600);
    gas.begin(Wire, 0x08); // use the hardware I2C

    //moyennes
    cCO2=0;
    cNO2=0;
    cC2H5OH=0;
    cCOV=0;
    cCO=0;
    mdb=0;
}

void loop() {
    compteur += 1;

    // main code 4 gaz:

    // GM102B NO2 sensor
    float valNO2 = gas.getGM102B();

    if (valNO2 > 999) 
	valNO2 = 999.0;
    
    cNO2 = cNO2 + float(valNO2) / 60.0;
  
    // GM302B C2H5CH sensor
    float valC2H5CH = gas.getGM302B();

    if (valC2H5CH > 999)
	valC2H5CH = 999.0;

    cC2H5OH = cC2H5OH + float(valC2H5CH) / 60.0;

    // GM502B VOC sensor
    float valVOC = gas.getGM502B();
    if (valVOC > 999) 
	valVOC = 999.0;

    cCOV = cCOV + float(valVOC) / 60.0;

    // GM702B CO sensor
    float valCO = gas.getGM702B();
    if (valCO > 999)
	valCO = 999.0;

    cCO = cCO + float(valCO) / 60.0;

    // Print the readings to the console
    Serial.print("NO2: ");
    Serial.print(valNO2);
    Serial.println("ppm");

    Serial.print("C2H5CH: ");
    Serial.print(valC2H5CH);
    Serial.println("ppm");

    Serial.print("VOC: ");
    Serial.print(valVOC);
    Serial.println("ppm");

    Serial.print("CO: ");
    Serial.print(valCO);
    Serial.println("ppm");

    //main code Thermistance :
    VoutT = (analogRead(entreeT) / 1023.0) * 3.3;

    // main code CO2
    float percentage;
    float volts;
    volts = MGRead(MG_PIN);

    percentage = MGGetPercentage(volts,CO2Curve);
    Serial.print("CO2: ");
    if (percentage == -1) {
	Serial.print( "<400" );
	cCO2 = cCO2 + 399.0 / 60.0;
    } else {
	Serial.print(percentage);
	cCO2 = cCO2 + float(percentage) / 60.0;
    }

    Serial.print( "ppm" );
    Serial.print("\n");

    // boucle son + délai
    for (int i=0; i<10; i=i+1) { 
	mdb = mdb + (75 + (20 * log((3.3 * analogRead(analogPin) / 1023.0) / 0.50))) / 600.0;
	delay(100);
    }



    Serial.print("\n");
    if (compteur==60){ //au bout de 60 secondes on envoit les données 
	ma_trame.NO2=uint16_t(cNO2);
	ma_trame.C2H5OH=uint16_t(cC2H5OH);
	ma_trame.COV=uint16_t(cCOV);
	ma_trame.CO=uint16_t(cCO);
	ma_trame.CO2=uint16_t(cCO2);
	ma_trame.temperature= uint16_t(10 * (VoutT * 13.2 - 2.25))  ;
	ma_trame.son=uint16_t(mdb);
	modem.beginPacket();
	modem.write((byte*) &ma_trame, sizeof(ma_trame)) ;
	compteur=1;
	cCO2=0;
	cNO2=0;
	cC2H5OH=0;
	cCOV=0;
	cCO=0;
	mdb=0;
	int err = modem.endPacket();

	if (err > 0) {
	    Serial.println("Message envoyé correctement");
	} else {
	    Serial.println("Erreur d'envoi :(");
	}
    }
    // on attends une seconde avant de prendre les prochaines mesures 
}


// fin code CO2
float MGRead(int mg_pin)
{
    int i;
    float v=0;

    for (i=0;i<READ_SAMPLE_TIMES;i++) {
	v += analogRead(mg_pin);
	delay(READ_SAMPLE_INTERVAL);
    }

    v = (v / READ_SAMPLE_TIMES) * 5.0 / 1024.0 ;
    return v;
}

/*****************************  MQGetPercentage **********************************
Input:   volts   - SEN-000007 output measured in volts
     pcurve  - pointer to the curve of the target gas
Output:  ppm of the target gas
Remarks: By using the slope and a point of the line. The x(logarithmic value of ppm)
     of the line could be derived if y(MG-811 output) is provided. As it is a
     logarithmic coordinate, power of 10 is used to convert the result to non-logarithmic
     value.
************************************************************************************/
int MGGetPercentage(float volts, float *pcurve)
{
    if ((volts / DC_GAIN) >= ZERO_POINT_VOLTAGE) {
	return -1;
    } else {
	return pow(10, ((volts / DC_GAIN) - pcurve[1]) / pcurve[2] + pcurve[0]);
    }
}
