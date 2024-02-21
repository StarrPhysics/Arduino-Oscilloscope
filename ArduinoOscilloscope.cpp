#include "Arduino.h"
#include "ArduinoOscilloscope.h"

// This function establishes a connection between the Arduino and the client-python program.
void ArduinoOscilloscope::establishConnection() {
    Serial.begin(_baud); // https://www.arduino.cc/reference/en/language/functions/communication/serial/

    for (int i = 0; i < _iterator + 1; i++) {
        pinMode(_pinNumberArray[i], INPUT);
    }

    while (true) {
        // Calls out for handshake response
        Serial.println("Arduino;ArduinoOscilloscope_Handshake;" + _pinNames);

        delay(500);

        if (Serial.available() > 0) {
            if (Serial.readString().startsWith("Client;ArduinoOscilloscope_Handshake")) break; // Breaks if handshake response is acknowledged.
        }
    }

    Serial.println("Arduino;Confirmed"); // Sends post-acknowledgment confirmation. Although the client dosn't acknowledge this message.

    _connected = true;
    
    // Following the execution of this function, the program is ready to begin.    
}

// This function (indened to be called in the Ardueno's loop function) records, packs, and sends the data from the analog pins to the client-python program.
void ArduinoOscilloscope::sendPinData() {
    /*
        -> All values sent through the serial bus must be shifted by 128 in order to avoid standard ASCII characters.
        -> Serial bus size it 8-bits.
        -> The values of the analog pins are 10-bit, ranging from 0 to 1023.

        In order to adhere to these constraints, the 10 byte value is split into two seperate 8-bit values:
        -> The first 7 bits are sent as the first byte.
        -> The leading 3 bits are sent as the second byte.
        -> The bytes are then shifted by 128 in order to avoid standard ASCII characters.
        
        These steps are done in reverse in the python program.
    */

    if (!_connected) return;
    
    for (int i = 0; i < _iterator + 1; i++) {
        int pinValue = analogRead(_pinNumberArray[i]); // Pontains the value on the analog pin ranging from 0 (corresponding to 0 volts) to 1023 (corresponding to 5 volts).

        int first7bits = _bitmask & pinValue;
        int leading3bits = ((~ _bitmask) & pinValue) >> 7;
        
        Serial.write(i + 128);              // The current pin number is sent as the first byte.
        Serial.write(first7bits + 128);     // The first 7 bits of the pinValue are sent as the second byte.
        Serial.write(leading3bits + 128);   // The leading 3 bits of the pinValue are sent as the third byte; though they are stored in the first 3 bits of the byte.
        Serial.write(10);                   // Newline character, which completes the data packet.
    }
}