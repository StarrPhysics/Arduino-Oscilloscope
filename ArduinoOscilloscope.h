#include <Arduino.h>

#ifndef ARDUINO_OSCILLOSCOPE_H
#define ARDUINO_OSCILLOSCOPE_H
#define MAX_PINS 10 // Just because I can't dynamically allocate memory in C++. Absolute W
#define InitalizeArduinoOscilloscope(baud, ...) ArduinoOscilloscope(baud, #__VA_ARGS__, __VA_ARGS__)

class ArduinoOscilloscope {
    public:
        template <typename... Args>
        ArduinoOscilloscope(int baud, const char* pinNames, Args... args): _baud(baud), _pinNames(String(pinNames)) {
            processArgs(args...);
        };
        
        void establishConnection();
        void sendPinData();

    private:
        int _pins[MAX_PINS];
        bool _connected = false;
        String _pinNames = "";
        int _baud;
        int _iterator = 0;

        template<typename T, typename... Rest>
        void processArgs(T arg, Rest... rest) {
            _pins[_iterator] = arg;
            _iterator += 1;
            processArgs(rest...);
        };
        void processArgs() {};

};

#endif // ARDUINO_OSCILLOSCOPE_H
