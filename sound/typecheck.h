#ifndef pinMode 
    // pas de arduino.h, on remplit par des valeurs random pour la completion auto

    #define INPUT 1
    #define OUTPUT 1

    #define A0  0
    #define A1  1

    void pinMode(int pin, int state);
    unsigned int analogRead(int pin);
    unsigned long millis();
#endif