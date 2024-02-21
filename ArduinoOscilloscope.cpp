#include "Arduino.h"
#include "ArduinoOscilloscope.h"

void ArduinoOscilloscope::establishConnection() {
    Serial.begin(_baud); // https://www.arduino.cc/reference/en/language/functions/communication/serial/
    pinMode(13, INPUT);

    for (int i = 0; i < sizeof(_pins); i++) {
        if (_pins[i] != 0)
        pinMode(_pins[i], INPUT);
    }

    while (true) {
        // Calls out for handshake response
        Serial.println("Arduino;ArduinoOscilloscope_Handshake;" + _pinNames);

        delay(500);

        if (Serial.available() > 0) {
            
            String str = Serial.readString();

            // Breaks if handshake response is acknowledged.
            if (str.startsWith("Client;ArduinoOscilloscope_Handshake")) break;
        }
    }

    Serial.println("Arduino;Confirmed");

    _connected = true;
    // Sends post-acknowledgment confirmation.
    // Program is ready to begin.    
}


void ArduinoOscilloscope::sendPinData() {
    // Function must be recursivly called in loop.
    if (!_connected) return;

    int bitfilter = 0b0001111111;
    
    //for (int i = 0; i < sizeof(_pins); i++) {
        /*
            -> All values must be Shifted by 128 in order to avoid standard ASCII characters.
            -> In addition, serial bus limitations are 8-bit.
            -> The analog pins return values of byte size 10.

            In essence, I must communicate a byte range of 0 to 1023
            exclusivly between the values of range of 127 to 255. Note that the cardinality
            of such a bit-space is equivolent to 7 bit numbers. Hence, 
            by imagining I am working in 7 bit, I can ensure that adding 
            127 for the values is not exceeding the 8-bit limit.

            To do so, I will send the first 3 bits of the pinValue, followd by the remaining 7 bits. 
            These values will be converted to integers, incremented by 128, and sent to the serial bus.
        */

        uint8_t pinNumber = _pins[0]; // The integer which corresponds to the pin.

        int pinValue = analogRead(pinNumber); // Pontains the value on the analog pin ranging from 0 (corresponding to 0 volts) to 1023 (corresponding to 5 volts).

        int first7bits = bitfilter & pinValue; // Contains the first 7 bits of the pinValue.
        int leading3bits = ((~ bitfilter) & pinValue) >> 7; // Contains the leading 3 bits of the pinValue, shifted rightwise by 7.
        
        Serial.write(first7bits + 128);
        Serial.write(leading3bits + 128);

        Serial.write(10);
}