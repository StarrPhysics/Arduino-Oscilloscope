#include <Arduino.h>

#ifndef ARDUINO_OSCILLOSCOPE_H
#define ARDUINO_OSCILLOSCOPE_H

class ArduinoOscilloscope {
    public:
        ArduinoOscilloscope(int pin, String pinName, int baud);
        void establishConnection();
        void sendPinData();
    private:
        int _pin;
        String _pinName;
        int _baud;
        bool _test_connection();
};

#endif // ARDUINO_OSCILLOSCOPE_H
