/*
  Documentation Suggests the Following:
  - 5 Volts Operating VOltage
  - A0 to A14
  - 10 bits
*/

#include "./ArduinoOscilloscope.h"

/*
  seralDataReponse if setAnalogPins = {A0}:
*/


void setup() {
  ArduinoOscilloscope instance = StartAnalogPinOsilloscope(A0, 9600);

  instance.establishConnection();

  // put your setup code here, to run once:
  // Serial.begin(9600);
}

void loop()
{
  /*
  
  String serialResponse = "{";


  for (int i = 0; i < numAnalogPins; i++) {
    uint8_t pin = setAnalogPins[i];
    // JsonFormatting my Data
    serialResponse += ("\"" + String("A") + String(pin - 54) + "\": " + String(float(analogRead(pin)) * 5.0 / 1023.0)) + ((i < sizeof(setAnalogPins) / sizeof(uint8_t) - 1)? "," : "}");
  }
  
  Serial.println(serialResponse);
  */
  
}
