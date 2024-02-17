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
    // Sends post-acknowledgment confirmation.
    // Program is ready to begin.    
}


void ArduinoOscilloscope::sendPinData() {
    // Function must be recursivly called in loop.
    for (int i = 0; i < sizeof(_pins); i++) {
        if (_pins[i] != 0) {
            Serial.write(analogRead(_pins[i]));
            Serial.write(10);
        }
    }
}

template<typename T, typename... Rest>
void ArduinoOscilloscope::processArgs(int i, T arg, Rest... rest) {
    _pins[i] = arg;
    processArgs(i++, rest...);
};

void ArduinoOscilloscope::processArgs() {};