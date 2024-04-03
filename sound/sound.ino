#include <typecheck.h>
#include <lut.h>

#define micPin  A0
#define splR     10


unsigned int adc2db(unsigned int adc) {
    return dbLUT[adc];
}

unsigned int spl_cache;
bool spl_read;

void handleSpl(unsigned int spl) {
    spl_cache = spl;
    spl_read = true;
}

void setup() {
    pinMode(micPin, INPUT);
}

unsigned long tmr = millis();
unsigned int _max = 0;
unsigned int buff = 0;

void loop() {
    if (millis() > tmr) {
        tmr = millis() + 1000 / splR;

        // Echantillonage 
        buff = analogRead(micPin);

        if (buff > _max) {
            // On considere adc2db st croissante
            // buff > max <=> buff_db > max_db

            handleSpl(adc2db(buff));
            _max = buff;
        }
    }
}