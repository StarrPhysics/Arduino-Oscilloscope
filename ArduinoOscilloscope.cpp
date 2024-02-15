#include "Arduino.h"
#include "ArduinoOscilloscope.h"

ArduinoOscilloscope::ArduinoOscilloscope(int pin, String pinName, int baud) {
    _pin = pin;
    _pinName = pinName;
    _baud = baud;
}

void ArduinoOscilloscope::establishConnection() {
    Serial.begin(_baud); // https://www.arduino.cc/reference/en/language/functions/communication/serial/
    pinMode(LED_BUILTIN, OUTPUT);

    while (true) {
        if (_test_connection() == true) { return; }
        delay(100);
    } 
        
}

bool ArduinoOscilloscope::_test_connection() {
    // Serial.println('Test');
    while (true) {
        //if (Serial.available() > 0) {
            digitalWrite(LED_BUILTIN, HIGH);
            //int message = Serial.read();
            Serial.write(49);
            Serial.write(10);
            Serial.write(50);
            Serial.write(10);
            Serial.write(51);
            Serial.write(10);
            delay(1000);
        //}
        digitalWrite(LED_BUILTIN, LOW);
        continue;
        

        //Serial.print("I received: ");
        //Serial.println(byte, DEC);
    }

    //Serial.read(); //https://www.arduino.cc/reference/en/language/functions/communication/serial/
}


void ArduinoOscilloscope::sendPinData() {

}

