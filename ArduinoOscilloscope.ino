#include "./ArduinoOscilloscope.h"
/**
 * Serves as an example of how to use the ArduinoOscilloscope class.
*/
ArduinoOscilloscope instance = InitalizeArduinoOscilloscope(9600,A1,A2,A3,A4,A5,A6,A7);

void setup() {
  instance.establishConnection();
}

void loop()
{
  instance.sendPinData();
}
