#include "./ArduinoOscilloscope.h"

ArduinoOscilloscope instance = InitalizeArduinoOscilloscope(9600,A1,A2,A3,A4);

void setup() {
  instance.establishConnection();
}

void loop()
{
  instance.sendPinData();
}
