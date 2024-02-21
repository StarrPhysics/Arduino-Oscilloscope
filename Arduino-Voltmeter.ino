#include "./ArduinoOscilloscope.h"

ArduinoOscilloscope instance = InitalizeArduinoOscilloscope(9600,A14);

void setup() {
  instance.establishConnection();
}

void loop()
{
  instance.sendPinData();
}
